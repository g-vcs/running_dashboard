from datetime import timedelta

from PIL import Image, ImageDraw

from running_dashboard import get_week_data

WIDTH = 250
HEIGHT = 122
HEADER_BOTTOM = 36
MASCOT_BOTTOM = 65
DAYS = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"]


def create_image():
    summary, daily_stats, week_start, week_end = get_week_data()

    image = Image.new("1", (WIDTH, HEIGHT), 1)
    draw = ImageDraw.Draw(image)

    draw_header(draw, summary, week_start, week_end)
    draw_mascot(draw, summary)
    draw_week_bar(draw, daily_stats)

    image.save("dashboard.png")
    print("Imagem criada: dashboard.png")


def draw_header(draw, summary, week_start, week_end):
    total_km, _, runs_count, pace, _ = summary
    last_day = week_end - timedelta(days=1)
    line1 = f"{week_start.day:02d}.{week_start.month:02d} -> {last_day.day:02d}.{last_day.month:02d}"
    line2 = f"{total_km:.1f} km | {runs_count} corridas"
    line3 = f"{round(pace,2)} min/km"

    draw.text((4, 2), line1)
    draw.text((4, 12), line2)
    draw.text((4, 24), line3)
    draw.line((0, HEADER_BOTTOM, WIDTH - 1, HEADER_BOTTOM), fill=0)


def draw_mascot(draw, summary):
    total_km, _, runs_count, _, _ = summary
    if runs_count == 0:
        face = "(x_x)"
    elif total_km < 10:
        face = "(-_-)"
    else:
        face = "(^_^)"

    center_y = int(HEADER_BOTTOM + (MASCOT_BOTTOM - HEADER_BOTTOM) / 2) - 5
    len_face = draw.textlength(face)
    draw.text(((WIDTH - len_face) / 2, center_y), face)

    draw.line((0, MASCOT_BOTTOM, WIDTH - 1, MASCOT_BOTTOM), fill=0)


def draw_week_bar(draw, daily_stats):
    col_width = (WIDTH - 8) / 7.0

    for i in range(7):
        center_x = 4 + i * col_width + col_width / 2

        day_name = DAYS[i]
        day_name_width = draw.textlength(day_name)
        text_day_name = center_x - day_name_width / 2

        distance = round(daily_stats[i]["distance_km"], 1)
        km_value = distance
        km = str(distance)
        km_width = draw.textlength(km)
        text_km = center_x - km_width / 2

        check = "[x]" if km_value != 0 else "[ ]"
        check_width = draw.textlength(check)
        text_check = center_x - check_width / 2

        draw.text((text_day_name, MASCOT_BOTTOM + 5), day_name)
        draw.text((text_km, MASCOT_BOTTOM + 17), km)
        draw.text((text_check, MASCOT_BOTTOM + 29), check)


if __name__ == "__main__":
    create_image()
