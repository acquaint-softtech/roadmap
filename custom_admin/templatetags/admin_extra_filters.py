import os

from PIL import Image, ImageDraw, ImageFont
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def generate_og_image(text_data, slug=None, type=None):
    img_path = os.path.join(settings.MEDIA_ROOT, 'project_og_img')
    width = 512
    height = 512

    file_name = slug if slug else text_data

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    file_path = os.path.join(img_path, f"{file_name}.jpg")

    if not os.path.exists(file_path):
        font = ImageFont.truetype('/home/acquaint/Roadmap/static/font/Roboto-Bold.ttf', 70)
        img = Image.open(os.path.join(settings.BASE_DIR, "static", 'images', 'og-template.jpg'))
        img_draw = ImageDraw.Draw(img)
        text_width, text_height = img_draw.textsize(type if type else text_data, font=font)
        img_draw.text(((width - text_width) / 2, (height - text_height) / 2),
                      f"Roadmap - {type if type else text_data}", font=font,
                      fill='red')
        if type:
            img_draw.text(((width - text_width) / 2, (height - text_height) / 2 + 80),
                          text_data, font=font,
                          fill='black')

        final_path = os.path.join(img_path, f"{file_name}.jpg")
        img.save(final_path)

    return str(os.path.join('/', 'media', 'project_og_img', f"{file_name}.jpg"))


@register.simple_tag
def set_bg_color(code):
    color_code = f'bg-[{code}]' if code else 'bg-[#d42020]'
    print(color_code,"color_code")
    return color_code
