# Whoop

Pulls recovery, resting heart rate, HRV, sleep, strain and workouts for a date range and prints them as markdown tables for an entry and for `../state.md`.

## Setup (once)

1. Create an app at https://developer.whoop.com (Developer Dashboard, Create App).
   - Redirect URL: `http://localhost:8000/callback`
   - Scopes: `read:recovery read:sleep read:cycles read:workout read:body_measurement offline`
2. Install dependencies in a virtual environment:
   ```
   cd whoop
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and paste `WHOOP_CLIENT_ID` and `WHOOP_CLIENT_SECRET` from the dashboard.
4. Log in. A browser opens; sign in to Whoop and approve access:
   ```
   .venv/bin/python auth.py
   ```
   Tokens are saved to `tokens.json` and refreshed automatically later.

`.env` and `tokens.json` hold secrets and are listed in `.gitignore`. Keep them out of git.

## Usage

```
.venv/bin/python fetch.py 2026-01-05 2026-01-11
```

Without arguments it fetches the last 7 days. Days follow your computer's time zone. Recovery, RHR, HRV and sleep belong to the morning they were measured, so they reflect the night before.
