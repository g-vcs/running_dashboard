from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta, timezone

def fetch_activities():
    load_dotenv()
    ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

    if not ACCESS_TOKEN:
        raise RuntimeError("STRAVA_ACCESS_TOKEN not defined on env")

    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": "Bearer " + ACCESS_TOKEN}
    response = requests.get(url, headers=headers)

    return response.json()

def get_current_week_range():
    current_date = datetime.now(timezone.utc)
    days_since_sunday = (current_date.weekday() + 1) % 7
    week_start = (current_date - timedelta(days=days_since_sunday)).replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = week_start + timedelta(days=7)
    return week_start, week_end

def parse_strava_date(date_str: str):
    date_strava = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    #print(date_strava)
    return date_strava

def filter_week_runs(activities, week_start, week_end):
    weekly_runs = []
    for act in activities:
        if act.get("type") == "Run":
            start_dt = parse_strava_date(act["start_date"])
            if week_start <= start_dt < week_end:
                weekly_runs.append(act)
    return weekly_runs

def summarize_week(weekly_runs):
    total_distance = 0
    total_time = 0
    runs_count = len(weekly_runs)
    longest_run_km = 0
    for act in weekly_runs:
        total_distance += act["distance"]/1000
        total_time += act["elapsed_time"]
        if act["distance"] > longest_run_km:
            longest_run_km = act["distance"]

    if total_distance > 0:
        avg_pace_per_km = (total_time / 60) / total_distance
    else:
        avg_pace_per_km = 0

    return total_distance, total_time, runs_count, avg_pace_per_km, longest_run_km/1000

def render_weekly_summary(summary, week_start, week_end):
    print(f"Semana: {week_start} - {week_end}")
    print(f"Corridas: {summary[2]}\n"
          f"Distância: {summary[0]:.2f} km\n"
          f"Tempo total: {format_duration(summary[1])}\n"
          f"Corrida mais longa: {summary[4]:.2f} km \n"
          f"Pace médio: {summary[3]:.2f} min/km")

def format_duration(seconds):
    hours = seconds // 3600
    remaining = seconds % 3600
    minutes = remaining // 60
    secs = remaining % 60

    if hours > 0 and minutes > 0 and secs > 0:
        return str(hours) + "h " + str(minutes) + "m " + str(secs) + "s"
    if hours > 0 and minutes > 0 and secs == 0:
        return str(hours) + "h " + str(minutes) + "m"
    if hours > 0 and minutes == 0:
        return str(hours) + "h " + str(secs) + "s"
    if hours == 0 and minutes > 0:
        return str(minutes) + "m " + str(secs) + "s"
    else:
        return str(secs) + "s"

if __name__ == "__main__":
    activities = fetch_activities()
    week_start, week_end = get_current_week_range()
    weekly_runs = filter_week_runs(activities, week_start, week_end)
    summary = summarize_week(weekly_runs)
    render_weekly_summary(summary, week_start, week_end)
