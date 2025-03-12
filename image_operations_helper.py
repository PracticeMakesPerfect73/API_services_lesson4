import os
import requests
from urllib.parse import urlparse, unquote


def get_file_extension(url):
    url = unquote(url)
    path = urlparse(url).path
    head, tail = os.path.split(path)
    root, extension = os.path.splitext(tail)
    return extension


def download_image(url, filename):
    images_path = 'images'
    os.makedirs(images_path, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()

    with open(os.path.join(images_path, filename), 'wb') as file:
        file.write(response.content)