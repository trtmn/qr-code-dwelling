import os
import qrcode
from PIL import Image
from io import BytesIO
import requests
import logging
import time

# Set up logging
logging.basicConfig(filename='app.log',level=logging.INFO)

def generate_qr_code(data, quality='H'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{quality}'),
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    return img

def resize_qr_code(img):
    img = img.resize((1000, 1000))
    img.info['dpi'] = (300, 300)
    return img

def calculate_max_size(img, percentage=None):
    max_size = (img.size[0] * percentage // 100, img.size[1] * percentage // 100)
    return max_size

def generate_and_save_qr_code(data, logo_path=None, quality='H'):
    img = generate_qr_code(data, quality)
    img = resize_qr_code(img)
    if logo_path is not None:
        img = apply_logo(img, logo_path)
    byte_arr = BytesIO()
    img.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    return byte_arr

def apply_logo(img, logo_path=None, percentage=29):
    start_time = time.time()

    if logo_path is None:
        return img

    if logo_path:
        logo = check_if_logo_path_is_local_or_remote(logo_path)
        max_size = calculate_max_size(img, percentage)
        logo.thumbnail(max_size, Image.LANCZOS)

        position = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)

        img = img.convert("RGBA")
        logo = logo.convert("RGBA")

        img.alpha_composite(logo, position)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logo_name = os.path.basename(logo_path)
    logging.info(f" {logo_name} took {elapsed_time} seconds.")

    return img

def check_if_logo_path_is_local_or_remote(logo_path):
    if logo_path.startswith(('http://', 'https://')):
        response = requests.get(logo_path)
        logo_path = BytesIO(response.content)
        logo_image = Image.open(logo_path)
        return logo_image
    else:
        return Image.open(logo_path)

def scan_icons_folder():
    folder_path = 'icons'
    icons = []
    for filename in os.listdir(folder_path):
        name, extension = os.path.splitext(filename)
        if extension in ['.png', '.jpg', '.jpeg', '.gif']:
            human_readable_name = name.replace('_', ' ').replace('-', ' ').title()
            file_path = os.path.join('icons', filename)
            icons.append((human_readable_name, file_path))
    icons = sorted(icons, key=lambda x: x[0])
    return icons

if __name__ == '__main__':
    print(scan_icons_folder())