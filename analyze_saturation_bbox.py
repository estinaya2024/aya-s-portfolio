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
        # Convert to HSV to analyze Saturation channel
        hsv = img.convert("HSV")
        width, height = hsv.size
        
        # Saturation threshold: let's find pixels with saturation > 40 (out of 255)
        color_pixels = []
        for y in range(height):
            for x in range(width):
                h, s, v = hsv.getpixel((x, y))
                if s > 40:
                    color_pixels.append((x, y, s))
        
        if color_pixels:
            xs = [p[0] for p in color_pixels]
            ys = [p[1] for p in color_pixels]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            avg_x = sum(xs) / len(xs)
            avg_y = sum(ys) / len(ys)
            print(f"--- {img_name} ---")
            print(f"Size: {width}x{height}")
            print(f"Saturated pixels count: {len(color_pixels)}")
            print(f"Bounding Box: x=[{min_x}, {max_x}] width={max_x - min_x}, y=[{min_y}, {max_y}] height={max_y - min_y}")
            print(f"Center: ({avg_x:.1f}, {avg_y:.1f})")
            
            # Let's save a cropped version of this bounding box to inspect it or check its aspect ratio
            # Let's print out the saturation values of a 20x20 grid around the center
            cx, cy = int(avg_x), int(avg_y)
            print(f"Around center ({cx}, {cy}):")
            # We can print if the saturated area is circular or rectangular
            # Check distance of color pixels from the center
            dists = [((p[0]-cx)**2 + (p[1]-cy)**2)**0.5 for p in color_pixels]
            max_dist = max(dists)
            avg_dist = sum(dists) / len(dists)
            print(f"Max dist from center: {max_dist:.1f}, Avg dist: {avg_dist:.1f}")
            # If it's a circle, max_dist should be close to radius, and we can check ratio of area
        else:
            print(f"--- {img_name} ---")
            print("No saturated pixels found")
