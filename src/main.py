from datetime import datetime
from src import sampler, validator
from src.proposer import generate_checks
from src.suite_generator import agent
from src.pr import create_pr


def main():
    run_id = datetime.now().strftime("%Y%m%d%H%M%S")
    print(f"Starting sampling job with run_id: {run_id}")
    sampler.main(run_id=run_id)

    print(f"Starting proposal generation job with run_id: {run_id}")
    generate_checks.main(run_id=run_id)

    print(f"Starting suite generation job with run_id: {run_id}")
    agent.main(run_id=run_id)

    validator.main(run_id=run_id)

    create_pr.main()


if __name__ == "__main__":
    main()
