import os
from PIL import Image

brain_dir = r"C:\Users\ayaka\.gemini\antigravity-ide\brain\4860af73-357c-4813-beaf-ac7f347a891c"
images = [
    "media__1779478247866.png",
    "media__1779478386257.png",
    "media__1779478746594.png"
]

for img_name in images:
    path = os.path.join(brain_dir, img_name)
    if not os.path.exists(path):
        continue
    with Image.open(path) as img:
        width, height = img.size
        # We want to find the bounding box of the colored region.
        # Let's convert to HSV and find all pixels with S > 50 and V > 50.
        hsv = img.convert("HSV")
        colored_coords = []
        for y in range(height):
            for x in range(width):
                h, s, v = hsv.getpixel((x, y))
                # S > 50 means it's colored (not grayscale or near-grayscale)
                if s > 50 and v > 30:
                    colored_coords.append((x, y))
        
        if colored_coords:
            xs = [p[0] for p in colored_coords]
            ys = [p[1] for p in colored_coords]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            w = max_x - min_x
            h = max_y - min_y
            print(f"{img_name}: colored region bounding box: x=[{min_x}, {max_x}] (width={w}), y=[{min_y}, {max_y}] (height={h})")
            
            # Let's save a crop of this colored region as a debug png
            crop_img = img.crop((min_x, min_y, max_x, max_y))
            crop_img.save(os.path.join(brain_dir, f"crop_{img_name}"))
            print(f"Saved crop_{img_name} to brain directory.")
        else:
            print(f"{img_name}: no colored region found")
