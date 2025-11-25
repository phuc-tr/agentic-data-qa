import subprocess

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    run("git branch -D test || true")
    run("git checkout -b test")

    filepath = "expectations/raddb_suite.json"

    run(f"git add {filepath}")
    run('git commit -m "Initial commit for test PR"')

    run("git push -u origin test")

    run('gh pr create --base main --head test '
    '--title "Test PR" --body "This is a test PR." --draft')

    run("git checkout main")
