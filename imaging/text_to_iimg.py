from PIL import Image, ImageFont, ImageDraw

test = ''


def create_image(text):
    img = Image.new('RGB', (252, 110), color=(255, 255, 255))

    fnt = ImageFont.truetype('/Desktop/Desktop/QRs/imaging/font/M54.ttf', 65)
    text_pos = ((img.size[0] - fnt.getsize(text)[0]) // 2, 15)
    d = ImageDraw.Draw(img)
    d.text(text_pos, text, font=fnt, fill=(0, 0, 0))

    return img


if __name__ == '__main__':
    image = create_image(test)
    image.save('image.png')
