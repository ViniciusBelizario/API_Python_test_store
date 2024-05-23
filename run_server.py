import os
import subprocess
import uvicorn

def run_server():
    """Run the Uvicorn server."""
    uvicorn.run("store.main:app", host="127.0.0.1", port=8000, reload=True)

def precommit_install():
    """Install pre-commit hooks."""
    # Ensure the pre-commit config file is in place
    precommit_config = """
default_language_version:
    python: python3.11
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: check-added-large-files
    -   id: check-toml
    -   id: check-yaml
        args:
        -   --unsafe
    -   id: end-of-file-fixer
    -   id: trailing-whitespace
-   repo: https://github.com/asottile/pyupgrade
    rev: v3.7.0
    hooks:
    -   id: pyupgrade
        args:
        - --py3-plus
        - --keep-runtime-typing
-   repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.275
    hooks:
    -   id: ruff
        args:
        - --fix
-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
"""
    with open(".pre-commit-config.yaml", "w") as f:
        f.write(precommit_config)

    # Run the pre-commit install command
    subprocess.run(["poetry", "run", "pre-commit", "install"], check=True)

def run_tests():
    """Run tests using pytest."""
    subprocess.run(["poetry", "run", "pytest"], check=True)

def run_tests_matching(pattern):
    """Run tests matching a pattern using pytest."""
    subprocess.run(["poetry", "run", "pytest", "-s", "-rx", "-k", pattern, "--pdb", "store", "./tests/"], check=True)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage project tasks.")
    parser.add_argument("command", type=str, help="Command to run (run, precommit-install, test, test-matching)")
    parser.add_argument("-k", "--keyword", type=str, help="Keyword for test-matching", default="")

    args = parser.parse_args()

    if args.command == "run":
        run_server()
    elif args.command == "precommit-install":
        precommit_install()
    elif args.command == "test":
        run_tests()
    elif args.command == "test-matching":
        if args.keyword:
            run_tests_matching(args.keyword)
        else:
            print("Please provide a keyword for test-matching using the -k option.")
    else:
        print(f"Unknown command: {args.command}")
