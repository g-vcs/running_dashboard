from PIL import Image, ImageDraw

WIDTH = 250
HEIGHT = 122
HEADER_BOTTOM = 24
MASCOT_BOTTOM = 65
DAYS = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"]


def create_image():
    image = Image.new("1", (WIDTH, HEIGHT), 1)
    draw = ImageDraw.Draw(image)

    draw_header(draw)
    draw_mascot(draw)
    draw_week_bar(draw, "")

    image.save("dashboard.png")
    print("Imagem criada: dashboard.png")


def draw_header(draw):
    draw.text((4, 2), "24.11 -> 30.11")
    draw.text((4, 12), "25.3 km | 3 corridas")
    draw.line((0, HEADER_BOTTOM, WIDTH - 1, HEADER_BOTTOM), fill=0)


def draw_mascot(draw):
    center_y = int(HEADER_BOTTOM + (MASCOT_BOTTOM - HEADER_BOTTOM) / 2)
    face = "(o_o)"
    len_face = draw.textlength(face)
    draw.text(((WIDTH - len_face) / 2, center_y), face)

    draw.line((0, MASCOT_BOTTOM, WIDTH - 1, MASCOT_BOTTOM), fill=0)


def draw_week_bar(draw, daily_stats):
    mock_km = [12, 0, 0, 5, 0, 7, 0]
    col_width = (WIDTH - 8) / 7.0

    for i in range(7):
        center_x = 4 + i * col_width + col_width / 2

        day_name = DAYS[i]
        day_name_width = draw.textlength(day_name)
        text_day_name = center_x - day_name_width / 2

        km_value = mock_km[i]
        km = str(mock_km[i])
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
