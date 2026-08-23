# log_util.py
# Simple logger for KM-Waechter.

import time

LOG_LINES: list[str] = []


def log(message: str) -> None:
    """Append a timestamped message to the log and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Append all buffered log lines to the given file and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(f"{line}\n")
    LOG_LINES.clear()
