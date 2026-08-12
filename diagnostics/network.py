"""Network reachability checks."""
import subprocess


def ping_host(host):
    """Ping a host once and return the raw command output."""
    command = ["ping", "-c", "1", host]
    return subprocess.run(command, capture_output=True, text=True).stdout
