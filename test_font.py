from PIL import ImageFont, ImageDraw, Image

img = Image.new("RGB", (1280, 500), (255, 255, 255))
draw = ImageDraw.Draw(img)

# use a bitmap font
font = ImageFont.load("file.pil")

draw.text((10, 10), "the quick brown fox jumps over the lazy dog", 'blue', font=font)

img.save("hello.png")

# use a truetype font
# font = ImageFont.truetype("arial.ttf", 15)

# draw.text((10, 25), "world", font=font)
