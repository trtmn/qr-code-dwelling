import os
import qrcode
from PIL import Image
from io import BytesIO
import requests

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
    # Calculate max size based on the given percentage of the QR code
    max_size = (img.size[0] * percentage // 100, img.size[1] * percentage // 100)
    return max_size

def generate_and_save_qr_code(data, logo_path=None, quality='H'):
    img = generate_qr_code(data, quality)
    img = resize_qr_code(img)
    img = apply_logo(img, logo_path)

    byte_arr = BytesIO()
    img.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    return byte_arr

def apply_logo(img, logo_path=None, percentage=25):
    if logo_path is None:
        logo_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logo.png')

    if logo_path:
        logo = check_if_logo_path_is_local_or_remote(logo_path)
        max_size = calculate_max_size(img, percentage)  # Use the new function here
        logo.thumbnail(max_size, Image.LANCZOS)  # Apply LANCZOS filter here

        # Calculate the position for the logo
        position = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)

        # Convert images to RGBA to ensure they have an alpha channel
        img = img.convert("RGBA")
        logo = logo.convert("RGBA")

        # Perform alpha composite
        img.alpha_composite(logo, position)
    return img


def check_if_logo_path_is_local_or_remote(logo_path):
    if logo_path.startswith(('http://', 'https://')):
        # Download the logo from the web
        response = requests.get(logo_path)
        logo_path = BytesIO(response.content)
        logo_image = Image.open(logo_path)
        return logo_image
    else:
        return Image.open(logo_path)