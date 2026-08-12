"""Network reachability checks."""
import subprocess


def ping_host(host):
    """Ping a host once and return the raw command output.

    host comes straight from user input (a CLI argument here, but the same
    function backs an internal HTTP endpoint elsewhere). Using
    subprocess.run with an argument list (no shell=True) means host is
    passed as a single literal argument to ping, never interpreted by a
    shell -- this closes the OS command injection vulnerability that
    existed here previously (os.popen with a shell-interpolated string).
    """
    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.stdout
