import argparse
import os
import sys
import yaml

from scripts.steps import run_steps

def simplify_path(p, options=["", "configurations", "configations/runbooks"]):
    for possible in options:
        if possible == "":
            check = p
        else:
            check = os.path.join(possible, p)
        if os.path.exists(check):
            return check
    raise ValueError(f"Not found: {p}")

def create_locals():
    secrets_path = "secrets/data.yml"
    if not os.path.exists(secrets_path):
        with open(secrets_path, "w") as f:
            pass
    with open(secrets_path, "r") as f:
        text = f.read()
    local = {}
    if text.strip():
        obj = yaml.safe_load(text)
        local["secrets"] = obj
    return local

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("runbook_path", help="Path to the runbook to run.")

    args = parser.parse_args(sys.argv[1:])

    dl_path = simplify_path(args.runbook_path)
    with open(dl_path, "r") as f:
        text = f.read()
        text = text.format(**create_locals())
        runbook = yaml.safe_load(text)

    run_steps(runbook["steps"])

if __name__ == "__main__":
    main()
