#!/usr/bin/env python3
"""
Agentic AI Workshop -- launch ALL 9 demos with one command.

Usage:
    git clone https://github.com/ynpreet/agentic-ai-demos.git
    cd agentic-ai-demos
    python3 run_all_demos.py

Then open the URLs it prints -- every demo is on localhost,
only the port number changes (8001 -> 8009).

What it does:
    - Clones any of the 9 demo repos you don't have yet.
    - Starts all 9 web UIs at once, each on its own port.
    - Waits until each one answers, then prints the URL table.
    - Ctrl+C stops everything cleanly.

Requirements: python3, git, internet (first run only, for cloning).
No pip installs -- every demo runs on the Python standard library.
"""

import socket
import subprocess
import sys
import time
from pathlib import Path

DEMOS = [
    # (github repo, port, display name)
    ("agentic-care-management",   8001, "01 - Personalized Care Management"),
    ("hhv-copilot",               8002, "02 - HHV Copilot (Medicare Advantage)"),
    ("restaurant-location-agent", 8003, "03 - Restaurant Location Agent"),
    ("aeroyield-ai",              8004, "04 - AeroYield AI (Airline Revenue)"),
    ("music-mood-agent",          8005, "05 - Music Mood Agent"),
    ("fixmate-ai",                8006, "06 - FixMate AI (Maintenance)"),
    ("gameguard-ai",              8007, "07 - GameGuard AI (Gaming Safety)"),
    ("guestfirst-ai",             8008, "08 - GuestFirst AI (Restaurants)"),
    ("resume-reviewer-agent",     8009, "09 - Resume Reviewer AI"),
]
OWNER = "ynpreet"
CLONE_TIMEOUT = 180
START_TIMEOUT = 25


def port_open(port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def main():
    root = Path.cwd()
    logdir = root / "logs"
    logdir.mkdir(exist_ok=True)
    procs = []

    print("=" * 64)
    print(" Agentic AI Workshop -- starting all 9 demos")
    print("=" * 64)

    for repo, port, name in DEMOS:
        d = root / repo
        if not (d / "app.py").exists():
            print("[clone] %s ..." % repo)
            r = subprocess.run(
                ["git", "clone", "--quiet",
                 "https://github.com/%s/%s.git" % (OWNER, repo), str(d)],
                timeout=CLONE_TIMEOUT)
            if r.returncode != 0 or not (d / "app.py").exists():
                print("  !! failed to clone %s -- skipping" % repo)
                continue
        if port_open(port):
            print("[skip]  %s -- port %d already in use (already running?)" % (name, port))
            continue
        logf = open(logdir / ("%s.log" % repo), "w")
        p = subprocess.Popen([sys.executable, "app.py"], cwd=str(d),
                             stdout=logf, stderr=subprocess.STDOUT)
        procs.append((repo, port, name, p, logf))
        print("[start] %s (port %d) ..." % (name, port))

    print("-" * 64)
    for repo, port, name, p, logf in procs:
        deadline = time.time() + START_TIMEOUT
        ok = False
        while time.time() < deadline:
            if p.poll() is not None:
                break
            if port_open(port):
                ok = True
                break
            time.sleep(0.3)
        if ok:
            print("  READY   http://localhost:%d  (%s)" % (port, name))
        else:
            print("  FAILED  %s -- see logs/%s.log" % (name, repo))
            try:
                p.terminate()
            except OSError:
                pass

    print("=" * 64)
    print(" Open any URL above -- only the port number changes.")
    print(" Press Ctrl+C to stop everything.")
    print("=" * 64)
    try:
        while True:
            time.sleep(2)
            for repo, port, name, p, logf in procs:
                if p.poll() is not None:
                    print("  !! %s (port %d) stopped unexpectedly -- see logs/%s.log"
                          % (name, port, repo))
                    procs.remove((repo, port, name, p, logf))
    except KeyboardInterrupt:
        print("\nStopping all demos ...")
        for _, _, _, p, _ in procs:
            try:
                p.terminate()
            except OSError:
                pass
        for _, _, _, p, _ in procs:
            try:
                p.wait(timeout=5)
            except Exception:
                try:
                    p.kill()
                except OSError:
                    pass
        print("All stopped. Bye!")


if __name__ == "__main__":
    main()
