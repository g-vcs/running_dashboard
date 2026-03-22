from datetime import timedelta
from PIL import Image, ImageDraw
from running_dashboard import get_week_data, format_pace


WIDTH = 250
HEIGHT = 122
DAYS = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"]

def create_image():
    summary, daily_stats, week_start, week_end = get_week_data()
    image = Image.new("1", (WIDTH, HEIGHT), 1)
    draw = ImageDraw.Draw(image)
    draw_header(draw, summary)
    draw_separator(draw, y=38)
    draw_days(draw, daily_stats)
    draw_footer(draw, week_start, week_end)
    image.save("dashboard.png")
    print("Imagem criada: dashboard.png")

def draw_header(draw, summary):
    total_km, _, runs_count, pace, _ = summary
    km_text = f"{total_km:.1f} km"
    pace_text = format_pace(pace)
    runs_text = f"{runs_count} corridas"
    draw.text((4, 2), km_text, fill=0)
    draw.text((4, 16), pace_text, fill=0)
    draw.text((150, 16), runs_text, fill=0)

def draw_separator(draw, y):
    draw.line((0, y, WIDTH, y), fill=0)

def draw_days(draw, daily_stats):
    cell_w = WIDTH // 7
    cell_h = 68
    top = 40

    for i, stats in enumerate(daily_stats):
        x = i * cell_w
        ran = stats["distance_km"] > 0

        if ran:
            draw.rectangle([x, top, x + cell_w - 2, top + cell_h], fill=0)
            draw.text((x + 2, top + 2), DAYS[i], fill=1)
            draw.text((x + 2, top + 18), f"{stats['distance_km']:.1f}", fill=1)
            draw.text((x + 2, top + 30), "km", fill=1)
        else:
            draw.rectangle([x, top, x + cell_w - 2, top + cell_h], fill=1, outline=0)
            draw.text((x + 2, top + 2), DAYS[i], fill=0)
            draw.text((x + 14, top + 28), "-", fill=0)

def draw_footer(draw, week_start, week_end):
    last_day = week_end - timedelta(days=1)
    label = f"{week_start.day:02d}.{week_start.month:02d}-{last_day.day:02d}.{last_day.month:02d}"
    draw.line((0, 110), fill=0)
    draw.line((0, 110, WIDTH, 110), fill=0)
    draw.text((4, 113), label, fill=0)

if __name__ == "__main__":
    create_image()
