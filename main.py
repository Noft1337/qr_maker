import qrcode
import urllib.parse
import os
import imaging.text_to_iimg
import sys
import merge_all_qrs_to_page

DOCS_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSfTz8EdDPS06jMSmaO0h0h2gG_iZXSi_sRySuPjkXHwOKG73g/viewform?usp=pp_url&entry.1303423277={}&entry.633474312={}&entry.1549596454={}"
NAMES_FILE_PATH = ''
try:
    NAMES_FILE_PATH = sys.argv[1]
except IndexError:
    print("Usage: {} <path_to_file>".format(sys.argv[0]))
    exit(2)


def check_if_file_exists(path_to_file):
    return os.path.isfile(path_to_file)


def overwrite(path):
    valid = False
    while not valid:
        choice = input(f'"{path.split("/")[-1]}" already exists. \nWanna overwrite it? (y/n): ').lower()
        if choice == 'y':
            os.remove(path)
            return True
        if choice == 'n':
            return False
        else:
            print('Invalid pick, only "y/n" is valid')


def make_qr(path, final_link, serial, name):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(final_link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    text = imaging.text_to_iimg.create_image(serial[3::])
    # text = Image.open(text_unimaged)
    text_pos = ((img.size[0] - text.size[0]) // 2, (img.size[1] - text.size[1]) // 2)
    img.paste(text, text_pos)
    img_path = '{}/{}_{}.png'.format(path, serial[-4::], name[-3::])
    if check_if_file_exists(img_path):
        if not overwrite(img_path):
            return
    img.save(img_path)


def check_if_kita_name(line: str):
    return not (line.startswith('B15') or line.startswith('AH0015') or line.startswith('KSM'))


def create_directory(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def sterialize_line(line: str):
    line = line.replace('\n', '')
    line = line.replace('\t', ' ')
    return line


def mkdir():
    if not os.path.isdir('./images'):
        os.mkdir('./images')


def main():
    kita = ''
    path = './'
    mkdir()
    with open(NAMES_FILE_PATH, 'r') as file:
        for line in file.readlines():
            line = sterialize_line(line)
            if check_if_kita_name(line):
                kita = urllib.parse.quote_plus(line)
                path = './images'
                path = os.path.join(path, line)
                create_directory(path)
            else:
                split_line = line.split()
                name = split_line[0]
                serial = split_line[1]
                final_link = DOCS_LINK.format(kita, name, serial)
                make_qr(path, final_link, serial, name)
    merge_all_qrs_to_page.main()


if __name__ == '__main__':
    main()
