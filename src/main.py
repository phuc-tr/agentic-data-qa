import subprocess
from datetime import datetime
from src import sampler, validator, coverage
from src.proposer import generate_checks
from src.suite_generator import agent
from src.pr import create_pr
from src.gater import gater

def main():
    subprocess.run(["rm", "-r", "gx"])
    run_id = datetime.now().strftime("%Y%m%d%H%M%S")
    print(f"Starting sampling job with run_id: {run_id}")
    sampler.main(run_id=run_id)

    print(f"Starting proposal generation job with run_id: {run_id}")
    generate_checks.main(run_id=run_id)

    print(f"Starting suite generation job with run_id: {run_id}")
    agent.main(run_id=run_id)

    subprocess.run(["python", "expectations/raddb_suite.py"])

    validator.main(run_id=run_id)

    # Coverage
    coverage.main(run_id=run_id)
    # create_pr.main()

    # Gater
    gater.main(run_id=run_id)

    # Re-validate with filtered suite
    print(f"Starting re-validation job with run_id: {run_id}")
    validator.main(run_id=run_id)

if __name__ == "__main__":
    main()
