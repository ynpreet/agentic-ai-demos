# Agentic AI Workshop — Run All 9 Demos

One command starts all nine demo web UIs. Open the printed URLs in your
browser — every demo is on `localhost`, only the port number changes.

## Quick start

```bash
git clone https://github.com/ynpreet/agentic-ai-demos.git
cd agentic-ai-demos
python3 run_all_demos.py
```

That's it. The script clones any demo repo you don't have yet, starts all
nine servers, waits until each one answers, and prints the URL table.
Press `Ctrl+C` to stop everything cleanly.

Requirements: `python3`, `git`, internet (first run only, for cloning).
No `pip` installs — every demo runs on the Python standard library.

## The nine demos

| Port | Demo |
|------|------|
| 8001 | Personalized Care Management |
| 8002 | HHV Copilot (Medicare Advantage) |
| 8003 | Restaurant Location Agent |
| 8004 | AeroYield AI (Airline Revenue) |
| 8005 | Music Mood Agent |
| 8006 | FixMate AI (Maintenance) |
| 8007 | GameGuard AI (Gaming Safety) |
| 8008 | GuestFirst AI (Restaurants) |
| 8009 | Resume Reviewer AI |

## Notes

- Already have a demo repo cloned, or a port already in use? The script
  skips it gracefully instead of crashing.
- If a demo fails to start, check `logs/<repo>.log` for the error.
- Each demo also runs standalone: `cd <demo-repo> && python3 app.py`.
