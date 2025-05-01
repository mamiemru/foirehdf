from PIL import Image

def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

# Load the image
image = Image.open("logo.png").convert("RGB")
pixels = image.load()

# Define key colors and thresholds
green = (0, 255, 0)         # Background green
main_threshold = 85        # Threshold for detecting main subject vs green
bk_threshold = 85      # Threshold for background consistency
replacement_main = (85, 9, 34)   # For subject (not green)
replacement_bg = (0, 255, 0)   # For stray background (not close enough to green)

# Iterate over pixels
width, height = image.size
for x in range(width):
    for y in range(height):
        current = pixels[x, y]
        dist = color_distance(current, green)
        if dist > main_threshold:
            pixels[x, y] = replacement_main
        else:
            pixels[x, y] = replacement_bg
        # else: keep original green

# Save the result
image.save("logo_save.png")
