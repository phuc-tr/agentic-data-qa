# Agent-Assisted Data QA (Human-in-the-Loop)

An agentic pipeline that generates [Great Expectations](https://greatexpectations.io/) data quality suites from [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/) contracts, then opens a draft pull request for human review.

![pipeline](screenshots/architecture.png)

---

## How It Works

The pipeline runs in four stages:

1. **Sample** — connects to MySQL, samples 100 rows per table, and writes Parquet files + column profiles to `artifacts/`.
2. **CLI export (Stage 1)** — uses the `datacontract` CLI to translate schema-level rules (not-null, unique, range, domain, format) into a GX expectation suite.
3. **LLM generation (Stage 3)** — for any rules the CLI could not handle (quality blocks, freshness, missed structural rules), an LLM generates the remaining expectations.
4. **Validate + PR (Stage 4)** — runs GX validation against the sample data, saves the suite JSON and a validation report, then creates a draft pull request on GitHub.

---

## Project Structure

```
.
├── src/qa_agent/               # Python package
│   ├── main.py                 # LangGraph pipeline entrypoint + CLI
│   └── langgraph_src/
│       ├── contract_parser.py  # CLI export, coverage diffing, rule extraction
│       ├── sampler.py          # DB sampling and profiling
│       ├── validator.py        # GX validation runner
│       ├── github_utils.py     # GitHub App helpers (branch, commit, PR)
│       ├── prompt.py           # LLM prompt templates
│       └── utils.py            # Code extraction helpers
├── case_studies/
│   ├── contracts/              # Data contracts (billing, bsadb, raddb)
│   ├── docker-compose.yml      # MySQL + data loader
│   └── database/               # SQL dumps and seed data
├── artifacts/                  # Runtime outputs (gitignored)
│   ├── samples/                # Parquet samples per table
│   ├── profiles/               # Column null-rate / distinct-ratio profiles
│   ├── metadata/               # Declared vs observed schema types
│   ├── failing_examples/       # CSV rows that failed validation
│   └── sandbox/                # Full GX validation reports
├── expectations/               # Generated GX suite JSON files
├── gx/                         # Great Expectations file context (auto-created)
├── pyproject.toml
└── requirement.txt
```

---

## Quick Start

### 1. Install the Package

```bash
pip install -r requirement.txt
pip install -e .
```

Or build a wheel:

```bash
python -m build
pip install ./dist/qa_agent-0.1.0-py3-none-any.whl --force-reinstall
```

---

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# LLM models (any model string accepted by langchain init_chat_model)
CODER_MODEL=gpt-5.2
WRITER_MODEL=gpt-3.5-turbo

# API key for whichever LLM provider you use
OPENAI_API_KEY=

# GitHub App credentials (required for PR creation)
GITHUB_APP_ID=
GITHUB_INSTALLATION_ID=
GITHUB_PRIVATE_KEY_PATH=./private-key.pem
```

#### Creating a GitHub App

1. Go to [https://github.com/settings/apps](https://github.com/settings/apps) and click **New GitHub App**.
2. Set **Permissions**: Contents → Read & Write, Pull requests → Read & Write.
3. After creation, note the **App ID** and generate a **Private Key** (`.pem` file).
4. Install the app on your repository and copy the **Installation ID** from the URL at `https://github.com/settings/installations`.

---

### 3. Start the Database

```bash
cd case_studies
docker compose up -d
```

This starts a MySQL 8.0 container and seeds it with the case study data.

---

### 4. Run the Pipeline

```bash
qa_agent \
  --owner <GITHUB_USERNAME> \
  --repo <GITHUB_REPO> \
  --dataset raddb \
  --output_path expectations/raddb_suite.py \
  --contract case_studies/contracts/contract.raddb.yaml
```

---

## CLI Reference

| Flag | Required | Description |
|---|---|---|
| `--owner` | Yes | GitHub username or organization |
| `--repo` | Yes | Repository name |
| `--dataset` | Yes | Dataset name (`billing`, `bsadb`, `raddb`) |
| `--output_path` | Yes | Path for the generated expectations file |
| `--contract` | Yes | Path to the ODCS data contract YAML |
| `--base_branch` | No | Base branch for the PR (default: `main`) |
| `--run_id` | No | Re-use artifacts from a previous run (skips sampling) |

---

## Data Contracts

Contracts live in `case_studies/contracts/` and follow the Open Data Contract Standard. Database connection details (host, port, credentials) are declared in the `servers.mysql` block of each contract — the sampler reads them directly from there.

Available contracts:

- `contract.billing.yaml`
- `contract.bsadb.yaml`
- `contract.raddb.yaml`

---

## Output

After a successful run:

- `expectations/<dataset>_suite.json` — merged GX expectation suite (CLI + LLM)
- `expectations/<contract>.llm.yaml` — pruned contract fragment sent to the LLM
- `artifacts/sandbox/<dataset>.<run_id>.report.json` — full GX validation report
- `artifacts/failing_examples/<dataset>.<run_id>.csv` — up to 5 rows that failed
- A draft PR is opened on GitHub with an LLM-written summary of the validation results.
