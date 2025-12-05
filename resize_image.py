from PIL import Image, ImageFilter
import os, sys
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

TARGET_WIDTH = 1280
TARGET_HEIGHT = 720

def make_landscape_with_blur(src_path, dst_path):
    try:
        img = Image.open(src_path).convert("RGB")
        w, h = img.size

        # Make sure final canvas is landscape
        width = max(TARGET_WIDTH, TARGET_HEIGHT)
        height = min(TARGET_WIDTH, TARGET_HEIGHT)

        # Scale original image to fit inside landscape canvas
        ratio = min(width / w, height / h)
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        main_img = img.resize((new_w, new_h), Image.LANCZOS)

        # Create blurred background
        bg = img.resize((width, height), Image.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(30))

        # Paste centered
        x = (width - new_w) // 2
        y = (height - new_h) // 2
        bg.paste(main_img, (x, y))

        # Save output
        bg.save(dst_path)

    except Exception as e:
        print(f"Error processing '{src_path}': {e}")


def is_image_file(filename):
    ext = filename.lower().split(".")[-1]
    return ext in ["jpg", "jpeg", "png", "webp", "bmp", "gif", "tiff"]


def process_path(user_path):
    user_path = user_path.strip()

    if not os.path.exists(user_path):
        print("Error: Path does not exist.")
        return

    # Output folder at script root
    output_folder = os.path.join(os.getcwd(), "output")
    os.makedirs(output_folder, exist_ok=True)

    if os.path.isfile(user_path):
        if not is_image_file(user_path):
            print("Error: Provided file is not an image.")
            return

        filename = os.path.basename(user_path)
        dst_path = os.path.join(output_folder, filename)

        print(f"Processing file: {filename}")
        make_landscape_with_blur(user_path, dst_path)
        print("Done.")

    else:
        # Folder: process all images inside
        files = os.listdir(user_path)
        image_files = [f for f in files if is_image_file(f)]

        if not image_files:
            print("No image files found in the folder.")
            return

        print(f"Processing {len(image_files)} images...")

        for file in image_files:
            src = os.path.join(user_path, file)
            dst = os.path.join(output_folder, file)
            print(f"- {file}")
            make_landscape_with_blur(src, dst)

        print("Batch processing complete.")


if __name__ == "__main__":
    user_input = prompt(
        "Enter image file OR folder path: ",
        completer=PathCompleter(expanduser=True),
        complete_while_typing=True
    )
    process_path(user_input)
    input("Press Enter to exit…")