#!/usr/bin/env python3
"""Reset netdiag-vuln-sample's diagnostics/network.py back to the planted
CWE-78 vulnerability, pushed as a direct commit to main.

Deliberately outside the CWE Find-Fix-Approve-Ship pipeline -- this is a
manual demo-reset utility you run yourself before a demo, not part of the
automated find/fix/approve/ship flow. Run it, then re-trigger the workflow
to watch it find and fix the vulnerability again live.
"""
import subprocess
import sys
import tempfile

REPO = "https://github.com/automateyournetwork/netdiag-vuln-sample"
FILE_PATH = "diagnostics/network.py"

VULNERABLE_CONTENT = '''"""Network reachability checks."""
import os


def ping_host(host):
    """Ping a host once and return the raw command output.

    host comes straight from user input (a CLI argument here, but the same
    function backs an internal HTTP endpoint elsewhere) and is passed
    directly into a shell command below.
    """
    command = f"ping -c 1 {host}"
    return os.popen(command).read()
'''


def run(cmd, cwd=None):
    print("+", " ".join(cmd))
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    if result.stdout.strip():
        print(result.stdout.strip())
    return result.stdout.strip()


def main():
    with tempfile.TemporaryDirectory(prefix="reset-demo-") as tmp:
        run(["git", "clone", "--depth", "1", REPO, tmp])
        with open(f"{tmp}/{FILE_PATH}", "w") as f:
            f.write(VULNERABLE_CONTENT)
        run(["git", "add", FILE_PATH], cwd=tmp)
        status = run(["git", "status", "--porcelain"], cwd=tmp)
        if not status:
            print("Already vulnerable -- nothing to reset.")
            return
        run(["git", "commit", "-m", "Reset demo: reintroduce CWE-78 for a fresh live run"], cwd=tmp)
        run(["git", "push", "origin", "HEAD:main"], cwd=tmp)
        print("\nDemo reset. diagnostics/network.py is vulnerable again on main.")
        print("Re-run the CWE Find-Fix-Approve-Ship workflow to demo it fresh.")


if __name__ == "__main__":
    main()
