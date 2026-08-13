"""Diagnostic snapshot import/export."""
import base64
import pickle
import json


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
    try:
        # Try to load as pickle first for backward compatibility
        # WARNING: Only accept pickles from trusted sources, never untrusted input
        return pickle.loads(raw)
    except Exception:
        # If pickle fails, try to load as JSON (safer alternative)
        return json.loads(raw.decode("ascii"))
