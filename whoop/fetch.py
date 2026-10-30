"""Prints Whoop data for a date range as markdown tables.

Usage: .venv/bin/python fetch.py [FROM] [TO]   (dates YYYY-MM-DD, default last 7 days)
"""
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
import requests

from whoop_client import API_BASE, get_access_token

TZ = datetime.now().astimezone().tzinfo  # your computer's local time zone


def _get_all(path, start, end, token):
    """Fetches all records, following pagination."""
    records = []
    params = {"start": start, "end": end, "limit": 25}
    while True:
        resp = requests.get(
            f"{API_BASE}{path}",
            headers={"Authorization": f"Bearer {token}"},
            params=params,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        records.extend(data.get("records", []))
        token_next = data.get("next_token")
        if not token_next:
            return records
        params["nextToken"] = token_next


def _local_dt(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(TZ)


def _local_day(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(TZ).date()


def _fmt(v, nd=0):
    if v is None:
        return "n/a"
    return f"{v:.{nd}f}"


def main():
    if len(sys.argv) >= 3:
        d_from = date.fromisoformat(sys.argv[1])
        d_to = date.fromisoformat(sys.argv[2])
    else:
        d_to = date.today()
        d_from = d_to - timedelta(days=6)

    # margin to catch the night before the first day and the whole last day
    start = datetime.combine(d_from - timedelta(days=1), datetime.min.time(), TZ).astimezone(timezone.utc)
    end = datetime.combine(d_to + timedelta(days=1), datetime.min.time(), TZ).astimezone(timezone.utc)
    start_s = start.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_s = end.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    token = get_access_token()
    recoveries = _get_all("/recovery", start_s, end_s, token)
    sleeps = _get_all("/activity/sleep", start_s, end_s, token)
    cycles = _get_all("/cycle", start_s, end_s, token)
    workouts = _get_all("/activity/workout", start_s, end_s, token)

    # recovery and sleep belong to the morning the sleep ended
    sleep_by_id = {s["id"]: s for s in sleeps}
    rec_by_day = {}
    for r in recoveries:
        s = sleep_by_id.get(r.get("sleep_id"))
        day = _local_day(s["end"]) if s else _local_day(r["created_at"])
        rec_by_day[day] = r.get("score") or {}

    sleep_by_day = {}
    for s in sleeps:
        if s.get("nap"):
            continue
        sleep_by_day[_local_day(s["end"])] = s.get("score") or {}

    # a Whoop cycle starts in the evening with sleep, so strain belongs to the day
    # of that cycle's recovery, or without recovery to the day after the start
    cycle_day = {}
    for r in recoveries:
        s = sleep_by_id.get(r.get("sleep_id"))
        if s:
            cycle_day[r["cycle_id"]] = _local_day(s["end"])
    strain_by_day = {}
    for c in cycles:
        day = cycle_day.get(c["id"]) or _local_day(c["start"]) + timedelta(days=1)
        strain_by_day[day] = (c.get("score") or {}).get("strain")

    acts_by_day = defaultdict(list)
    for w in workouts:
        day = _local_day(w["start"])
        mins = (datetime.fromisoformat(w["end"].replace("Z", "+00:00"))
                - datetime.fromisoformat(w["start"].replace("Z", "+00:00"))).seconds // 60
        sc = w.get("score") or {}
        extra = ""
        if sc:
            extra = (f", start {_local_dt(w['start']):%H:%M}, strain {_fmt(sc.get('strain'), 1)}, "
                     f"avg HR {_fmt(sc.get('average_heart_rate'))} / max {_fmt(sc.get('max_heart_rate'))}")
        acts_by_day[day].append(f"{w.get('sport_name', '?')} {mins} min{extra}")

    print(f"## Whoop data, {d_from.isoformat()} to {d_to.isoformat()}\n")
    print("| Date | Recovery | RHR | HRV | Sleep | Strain |")
    print("|---|---|---|---|---|---|")
    day = d_from
    while day <= d_to:
        r = rec_by_day.get(day, {})
        s = sleep_by_day.get(day, {})
        print(
            f"| {day.isoformat()} "
            f"| {_fmt(r.get('recovery_score'))}% "
            f"| {_fmt(r.get('resting_heart_rate'))} "
            f"| {_fmt(r.get('hrv_rmssd_milli'), 1)} "
            f"| {_fmt(s.get('sleep_performance_percentage'))}% "
            f"| {_fmt(strain_by_day.get(day), 1)} |"
        )
        day += timedelta(days=1)

    print("\nRecovery, RHR, HRV and sleep are measured on the morning of that day, so they reflect the night before. Strain is the whole day.\n")

    print(f"## Whoop activities, {d_from.isoformat()} to {d_to.isoformat()}\n")
    print("| Date | Activities |")
    print("|---|---|")
    day = d_from
    while day <= d_to:
        acts = acts_by_day.get(day)
        print(f"| {day.isoformat()} | {', '.join(acts) if acts else 'none'} |")
        day += timedelta(days=1)


if __name__ == "__main__":
    main()
