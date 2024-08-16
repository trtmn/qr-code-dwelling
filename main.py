import os
import qrcode
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styledpil import StyledPilImage
from PIL import Image
from io import BytesIO
import requests
import logging
import time

# Set up logging
logging.basicConfig(filename='app.log',level=logging.INFO)

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
        box_size=100,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white',image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
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

def shorten_url(url):
    #TODO: allow for custom shortening services - using environment variables
    #For now, just check the environment of shorten True or False
    shorten = os.environ.get('shorten', 'False')
    if shorten.lower() != 'true':
        logging.info(f"Shortening is set to False, not shortening {url}")
        return url

    #check if the url is already shortened
    if url.startswith(('https://trtmn.io/', 'https://go.trtmn.io/')):
        logging.info(f"{url} is already shortened, not shortening again.")
        return url
    #if the url is from thedwelling.church, don't shorten it
    if url.startswith(('https://thedwelling.church', 'https://www.thedwelling.church')):
        return url

    #check if it's an actual url
    if not url.startswith('http'):
        logging.info(f"{url} is not a valid url, not shortening.")
        return url

    #check the length of the url, if it is greater than the standard shortened length, shorten it.
    if len(url) > len('https://trtmn.io/aaa'):
        #get the api key from the environment
        logging.info(f"Shortening {url} using the yourls service.")

        #create the post request
        yourls_key = os.environ.get('yourls_key')
        post_url = f'https://go.trtmn.io/yourls-api.php?signature={yourls_key}&action=shorturl&format=json&url={url}'
        response = requests.post(post_url)

        #log the response
        logging.info(f"{response.json()}")
        short_url = response.json()['shorturl']
        logging.info(f"Shortening {url} to {short_url}")
        return response.json()['shorturl']
    else:
        return url



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
    data = shorten_url(data)
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
    start_time = time.time()  # Start the timer

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

    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate elapsed time
    logo_name = os.path.basename(logo_path)  # Get the logo name
    logging.info(f" {logo_name} took {elapsed_time} seconds.")  # Log the elapsed time

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
    """
    Scans the 'icons' folder for image files and adds a predefined web image.

    This function searches through a specified folder ('icons') for files with
    image extensions (.png, .jpg, .jpeg, .gif). For each found image, it generates
    a human-readable name by replacing underscores and dashes with spaces and
    capitalizing the words. It then constructs a list of tuples, each containing
    the human-readable name and the file path of an image. Additionally, a predefined
    web image is added to this list. Finally, the list is sorted by the human-readable
    names of the images and returned.

    Returns:
        list of tuple: A sorted list of tuples, each containing the human-readable
                       name and the file path of an image, including a predefined
                       web image.
    """
    folder_path = 'icons'
    icons = []
    for filename in os.listdir(folder_path):
        name, extension = os.path.splitext(filename)
        if extension in ['.png', '.jpg', '.jpeg', '.gif']:  # add or remove file extensions as needed
            human_readable_name = name.replace('_', ' ').replace('-', ' ').title()
            file_path = os.path.join('.', folder_path, filename)
            icons.append((human_readable_name, file_path))
    # Add a gravatar option
    #TODO: Move this to a list of predefined remote images
    icons.append((r"Fishy's Gravatar", "https://gravatar.com/avatar/2e8f5f13323d9221726cf865f3488ddb8bc2811ef5706b3c1c78afcf30605ce6.png?s=800"))
    icons = sorted(icons, key=lambda x: x[0])  # Sort icons by human-readable name
    return icons



if __name__ == '__main__':
    print(scan_icons_folder())