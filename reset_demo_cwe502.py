#!/usr/bin/env python3
"""Reset netdiag-vuln-sample's diagnostics/snapshot.py back to the planted
CWE-502 vulnerability (unconditional pickle.loads on untrusted input),
pushed as a direct commit to main.

Companion to reset_demo.py, which only resets the CWE-78 bug in
diagnostics/network.py -- these are two independent planted vulnerabilities
in the same sample repo. Deliberately outside the CWE Find-Fix-Approve-Ship
pipeline -- run it yourself before a demo, then re-trigger the workflow.
"""
import subprocess
import sys
import tempfile

REPO = "https://github.com/automateyournetwork/netdiag-vuln-sample"
FILE_PATH = "diagnostics/snapshot.py"

# The original planted content, from this file's first commit (ca5bd49).
# Later "fixes" that got merged for this CWE were incomplete (kept calling
# pickle.loads unconditionally, just added a warning comment) -- this is
# the genuine, unmitigated vulnerable baseline.
VULNERABLE_CONTENT = '''"""Diagnostic snapshot import/export."""
import base64
import pickle


def export_snapshot(data):
    """Serialize a diagnostic snapshot dict for later restore."""
    return base64.b64encode(pickle.dumps(data)).decode("ascii")


def load_snapshot(blob):
    """Restore a previously exported diagnostic snapshot.

    blob is meant to be a base64-encoded pickle produced by
    export_snapshot() above, but this is also wired up to an internal
    "import snapshot" HTTP endpoint that accepts whatever a client
    uploads. pickle.loads executes arbitrary code embedded in the byte
    stream during unpickling -- well before any type-checking or
    validation of the resulting object ever happens.
    """
    raw = base64.b64decode(blob)
    return pickle.loads(raw)
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
    with tempfile.TemporaryDirectory(prefix="reset-demo-cwe502-") as tmp:
        run(["git", "clone", "--depth", "1", REPO, tmp])
        with open(f"{tmp}/{FILE_PATH}", "w") as f:
            f.write(VULNERABLE_CONTENT)
        run(["git", "add", FILE_PATH], cwd=tmp)
        status = run(["git", "status", "--porcelain"], cwd=tmp)
        if not status:
            print("Already vulnerable -- nothing to reset.")
            return
        run(["git", "commit", "-m", "Reset demo: reintroduce CWE-502 for a fresh live run"], cwd=tmp)
        run(["git", "push", "origin", "HEAD:main"], cwd=tmp)
        print("\nDemo reset. diagnostics/snapshot.py is vulnerable again on main.")
        print("Re-run the CWE Find-Fix-Approve-Ship workflow to demo it fresh.")


if __name__ == "__main__":
    main()
