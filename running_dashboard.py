from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta, timezone

DAYS_PT = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"]


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
    # print(date_strava)
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
        total_distance += act["distance"] / 1000
        total_time += act["elapsed_time"]
        if act["distance"] > longest_run_km:
            longest_run_km = act["distance"]

    if total_distance > 0:
        avg_pace_per_km = (total_time / 60) / total_distance
    else:
        avg_pace_per_km = 0

    return total_distance, total_time, runs_count, avg_pace_per_km, longest_run_km / 1000


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


def group_runs_by_day(weekly_runs, week_start):
    daily_stats = [
        {
            "distance_km": 0.0,
            "time_s": 0,
        }
        for _ in range(7)
    ]

    for act in weekly_runs:
        start_dt = parse_strava_date(act["start_date"])
        day_offset = (start_dt.date() - week_start.date()).days
        daily_stats[day_offset]["distance_km"] += act["distance"] / 1000
        daily_stats[day_offset]["time_s"] += act["elapsed_time"]

    return daily_stats

def render_daily_overview(daily_stats):
    day_cells = []
    dist_cells = []
    check_cells = []

    for i, stats in enumerate(daily_stats):
        day_name = DAYS_PT[i]
        dist = int(round(stats["distance_km"]))
        worked = "☑" if dist != 0 else "☐"

        day_cells.append(day_name)
        dist_cells.append(f"{dist} km")
        check_cells.append(worked)

    col_width = 8

    print("".join(cell.ljust(col_width) for cell in day_cells))
    print("".join(cell.ljust(col_width) for cell in dist_cells))
    print("".join(cell.ljust(col_width) for cell in check_cells))



if __name__ == "__main__":
    activities = fetch_activities()
    week_start, week_end = get_current_week_range()
    weekly_runs = filter_week_runs(activities, week_start, week_end)
    summary = summarize_week(weekly_runs)
   #render_weekly_summary(summary, week_start, week_end)

    daily_stats = group_runs_by_day(weekly_runs, week_start)
    render_daily_overview(daily_stats)

