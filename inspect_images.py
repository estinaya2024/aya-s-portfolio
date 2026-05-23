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
        print(f"{img_name} does not exist")
        continue
    with Image.open(path) as img:
        print(f"--- {img_name} ---")
        print(f"Format: {img.format}, Size: {img.size}, Mode: {img.mode}")
        # Downsample to a small grid to see where colors (saturation) are high
        # We can convert to HSV and check the Saturation channel
        small = img.resize((10, 10)).convert("HSV")
        pixels = list(small.getdata())
        print("Saturation grid (10x10):")
        for y in range(10):
            row = [pixels[y*10 + x][1] for x in range(10)]
            # print values in range 0-255 scaled to 0-9
            print(" ".join(str(val // 26) for val in row))
