# agent-data-qa
Agent-Assisted Data QA (Human-in-the-Loop)​

## Start live data streaming
To stimulate live data streaming:
```
cd database
docker compose up
```

## Get latest 100 rows
```
python sampler.py
```
Output: 
- artifacts/profiles/
- artifacts/metadata/
- artifacts/samples/

## Generate parameterized checks
```
python proposer/generate_checks.py
```
Output:
- artifacts/proposals


## Generate GX suite from parameterized checks
```
python suite_generator/agent.py
```
Output:
- expectations/

## Validate the GX suite
```
python validator.py
```
Output:
- artifacts/sandbox/
- artifacts/failing_examples/
