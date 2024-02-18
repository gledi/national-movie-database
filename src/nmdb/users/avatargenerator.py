import random

from django.conf import settings
from django.contrib.staticfiles import finders
from PIL import Image, ImageDraw, ImageFont


def get_font(font_variant: str = "medium") -> ImageFont.FreeTypeFont | None:
    relative_path = settings.USER_AVATAR_FONT_VARIANTS.get(font_variant)
    if relative_path is None:
        relative_path = settings.USER_AVATAR_FONT_VARIANTS["medium"]

    font_filepath = finders.find(relative_path)
    font = None
    if font_filepath is not None:
        font = ImageFont.truetype(font_filepath, size=settings.USER_AVATAR_FONT_SIZE)

    return font


def get_initials(name: str) -> str:
    try:
        first, *rest = name.split()
    except ValueError:
        return "--"
    last = rest[-1] if rest else " "
    return f"{first[0]}{last[0]}".upper()


def generate_avatar_from_name(name: str, font_variant: str = "medium") -> Image.Image:
    fills = [
        (14, 113, 178),
        (48, 39, 85),
        (101, 84, 212),
        (26, 188, 156),
        (234, 76, 137),
    ]

    im = Image.new("RGBA", settings.USER_AVATAR_SIZE, (0, 0, 0, 0))
    font = get_font(font_variant)

    width, height = settings.USER_AVATAR_SIZE

    draw_circle = ImageDraw.Draw(im)
    draw_circle.ellipse(
        (100, 0, width - 101, height - 1),
        fill=random.choice(fills),
        outline=(0, 0, 0),
    )

    initials = get_initials(name)
    draw_initials = ImageDraw.Draw(im)
    _, _, iw, ih = draw_initials.textbbox((0, 0), initials, font=font)
    draw_initials.text(
        ((width - iw) / 2, (height - ih) / 2),
        initials,
        font=font,
        fill="white",
        stroke_width=1,
        stroke_fill="black",
    )

    return im
