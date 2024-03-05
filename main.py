import os
import qrcode
from PIL import Image
from io import BytesIO
import requests

def generate_qr_code(data, quality='H'):
    """
    Generate a QR code image from the given data.

    Parameters:
    data (str): The data to be encoded in the QR code.
    quality (str): The error correction level for the QR code. Default is 'H'.

    Returns:
    PIL.Image: The generated QR code as a PIL Image object.
    """
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
    """
    Resize the given QR code image to 1000x1000 pixels and set the DPI to 300.

    Parameters:
    img (PIL.Image): The QR code image to be resized.

    Returns:
    PIL.Image: The resized QR code image.
    """
    img = img.resize((1000, 1000))
    img.info['dpi'] = (300, 300)
    return img

def calculate_max_size(img, percentage=None):
    """
    Calculate the maximum size for the logo based on a percentage of the QR code size.

    Parameters:
    img (PIL.Image): The QR code image.
    percentage (int): The percentage of the QR code size to use for the logo size.

    Returns:
    tuple: The maximum size for the logo as a tuple of (width, height).
    """
    max_size = (img.size[0] * percentage // 100, img.size[1] * percentage // 100)
    return max_size

def generate_and_save_qr_code(data, logo_path=None, quality='H'):
    """
    Generate a QR code from the given data, apply a logo, and save it to a BytesIO object.

    Parameters:
    data (str): The data to be encoded in the QR code.
    logo_path (str): The path to the logo image file. If the path is a URL, the logo will be downloaded.
    quality (str): The error correction level for the QR code. Default is 'H'.

    Returns:
    io.BytesIO: The QR code image saved to a BytesIO object.
    """
    img = generate_qr_code(data, quality)
    img = resize_qr_code(img)
    if logo_path is not None:
        img = apply_logo(img, logo_path)
    byte_arr = BytesIO()
    img.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    return byte_arr

def apply_logo(img, logo_path=None, percentage=29):
    """
    Apply a logo to the center of the given QR code image.

    Parameters:
    img (PIL.Image): The QR code image.
    logo_path (str): The path to the logo image file. If the path is a URL, the logo will be downloaded.
    percentage (int): The size of the logo as a percentage of the QR code size. Default is 25.

    Returns:
    PIL.Image: The QR code image with the logo applied.
    """
    if logo_path is None:
        # logo_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logo.png')
        return img

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
    """
    Check if the given logo path is a local file path or a URL.

    If the path is a URL, download the logo and return it as a PIL Image object.
    If the path is a local file path, open the file and return it as a PIL Image object.

    Parameters:
    logo_path (str): The path to the logo image file.

    Returns:
    PIL.Image: The logo as a PIL Image object.
    """
    if logo_path.startswith(('http://', 'https://')):
        # Download the logo from the web
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
        if extension in ['.png', '.jpg', '.jpeg', '.gif']:  # add or remove file extensions as needed
            human_readable_name = name.replace('_', ' ').replace('-', ' ').title()
            file_path = os.path.join('.', folder_path, filename)
            icons.append((human_readable_name, file_path))
    return icons

if __name__ == '__main__':
    print(scan_icons_folder())