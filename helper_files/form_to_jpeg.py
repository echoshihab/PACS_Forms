from PIL import Image, ImageFont, ImageDraw

img = Image.new('RGB', (812, 1052), 'white')
test_string = 'This is a tech note'

font = ImageFont.truetype("arial.ttf", 20)
w, h = font.getsize(test_string)

draw = ImageDraw.Draw(img)

draw.text((10, 10),
          test_string, font=font, fill="black")

img.save("tech_note.jpg", "JPEG")
