import sys
sys.path.append('/home/guilherme-x1/e-Paper/RaspberryPi_JetsonNano/python/lib')

from datetime import timedelta
from PIL import Image, ImageDraw
from waveshare_epd import epd2in13_V3
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
    return image

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
    draw.line((0, 108, WIDTH, 108), fill=0)
    draw.text((4, 110), label, fill=0)

if __name__ == "__main__":
    epd = epd2in13_V3.EPD()
    print("A inicializar display...")
    epd.init()
    epd.Clear()

    print("A gerar imagem...")
    image = create_image()

    print("A enviar para o display...")
    epd.display(epd.getbuffer(image))

    print("Concluido! A colocar display em sleep...")
    epd.sleep()
