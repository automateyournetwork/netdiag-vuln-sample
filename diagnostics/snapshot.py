"""Diagnostic snapshot import/export."""
import base64
import json


def export_snapshot(data):
    """Serialize a diagnostic snapshot dict for later restore."""
    return base64.b64encode(json.dumps(data).encode("ascii")).decode("ascii")


def load_snapshot(blob):
    """Restore a previously exported diagnostic snapshot.

    blob is meant to be a base64-encoded JSON produced by
    export_snapshot() above, but this is also wired up to an internal
    "import snapshot" HTTP endpoint that accepts whatever a client
    uploads. JSON loading is safe and does not execute arbitrary code.
    """
    raw = base64.b64decode(blob)
    return json.loads(raw.decode("ascii"))
