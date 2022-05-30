from PIL import Image, ImageDraw, ImageFont
import os

X = 120
Y = 140
WORKING_DIR = './images/final_pages/'
DIRS_DIR = './images'
PATH = './images/%s/'


def get_dirs():
    final_dirs = []
    dirs = os.listdir(DIRS_DIR)
    for single_dir in dirs:
        if os.path.isdir(PATH % single_dir):
            final_dirs.append(single_dir)
    return final_dirs


def generate_text(text: str):
    text_img = Image.new('RGB', (580, 130), color=(255, 255, 255))
    fnt = ImageFont.truetype('/Desktop/Desktop/QRs/imaging/font/arial.ttf', 72)
    text_pos = ((text_img.size[0] - fnt.getsize(text)[0]) // 2, (text_img.size[1] - fnt.getsize(text)[1]) // 2)
    d = ImageDraw.Draw(text_img)
    d.text(text_pos, text, font=fnt, fill=(0, 0, 0))
    return text_img


def label_page(page: Image.Image, text):
    text = generate_text(text)
    page.paste(text, ((page.size[0] - text.size[0]) // 2, 40))
    return page


def create_page(name: str):
    img = Image.new('RGB', (2480, 3508), color=(255, 255, 255))
    img = label_page(img, name)
    return img


def is_image(file_name: str):
    return file_name.endswith(('.png', 'jpg', 'jpeg'))


def get_images(path):
    images = []
    files = os.listdir(path)
    for file in files:
        if is_image(file):
            images.append(file)
    return images


def draw_qr_on_page(page: Image.Image, positions: tuple, qr: Image.Image):
    page.paste(qr, positions)
    return page


def get_image_path(image_name: str, dir_name: str):
    return '{}/{}'.format(PATH % dir_name, image_name)


def validate_image(path_to_image):
    opened_image = Image.open(path_to_image)
    return opened_image.size[0] == opened_image.size[1]


def merge(images: list, dir_name: str):
    page = create_page(dir_name)
    page_num = 1
    i = 0
    for image in images:
        if not validate_image(get_image_path(image, dir_name)):
            continue
        if i == 12:
            page.save(WORKING_DIR + dir_name + str(page_num) + '.png')
            page = create_page(dir_name)
            i = 0
            page_num += 1
        image = Image.open(get_image_path(image, dir_name))
        image = image.resize((700, 700))
        image_pos = (X + (X + image.size[0]) * (i % 3), Y + (Y + image.size[1]) * int(i / 3))
        page = draw_qr_on_page(page, image_pos, image)
        i += 1
    page.save(WORKING_DIR + dir_name + str(page_num) + '.png')


def handle_path(path, dir_name):
    images = get_images(path)
    merge(images, dir_name)


def run_through_dirs(dirs: list):
    for dirr in dirs:
        path = PATH % dirr
        handle_path(path, dirr)


def create_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def main():
    create_dir(WORKING_DIR)
    dirs = get_dirs()
    if 'final_pages' in dirs:
        dirs.remove('final_pages')
    run_through_dirs(dirs)


if __name__ == '__main__':
    main()
