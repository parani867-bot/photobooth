from PIL import Image
import os
from datetime import datetime
import config

def create_photo_strip(photo_paths):
    # Ensure output folder exists
    os.makedirs(config.STRIPS_DIR, exist_ok=True)

    # Load images
    images = [Image.open(p) for p in photo_paths if os.path.exists(p)]

    if not images:
        print("No images to create strip")
        return None

    # Resize all images to same width
    target_width = 600
    resized_images = []

    for img in images:
        ratio = target_width / img.width
        new_height = int(img.height * ratio)
        resized_images.append(img.resize((target_width, new_height)))

    spacing = 30
    total_height = sum(img.height for img in resized_images) + spacing * (len(resized_images) - 1)

    strip = Image.new("RGB", (target_width, total_height), "white")

    y_offset = 0
    for img in resized_images:
        strip.paste(img, (0, y_offset))
        y_offset += img.height + spacing

    filename = os.path.join(
        config.STRIPS_DIR,
        f"strip_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    )

    strip.save(filename, quality=95)
    return filename
