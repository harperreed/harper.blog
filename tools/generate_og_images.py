import os
import argparse
from PIL import Image, ImageDraw, ImageFont

def generate_og_image(content_type: str, output_dir: str) -> None:
    width, height = 1200, 630
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font_path = "arial.ttf"
    font_size = 100

    if content_type == "posts":
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)
        font_size = 100
    elif content_type == "notes":
        background_color = (240, 240, 240)
        text_color = (50, 50, 50)
        font_size = 80
    elif content_type == "music":
        background_color = (0, 0, 0)
        text_color = (255, 255, 255)
        font_size = 100
    elif content_type in ["links", "books"]:
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)
        font_size = 100

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)

    text = content_type.capitalize()
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2

    draw.text((text_x, text_y), text, font=font, fill=text_color)

    output_path = os.path.join(output_dir, f"{content_type}_og_image.png")
    image.save(output_path)
    print(f"OG image saved to {output_path}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate OG images for different content types.")
    parser.add_argument("content_type", choices=["posts", "notes", "music", "links", "books"], help="The content type for the OG image.")
    parser.add_argument("output_dir", help="The directory to save the generated OG image.")
    args = parser.parse_args()

    generate_og_image(args.content_type, args.output_dir)

if __name__ == "__main__":
    main()
