import requests
import os
from environs import Env
from image_operations_helper import get_file_extension, download_image

IMAGE_COUNT = 40

def fetch_nasa_apod(api_key):
    url = 'https://api.nasa.gov/planetary/apod'
    images_path = 'images'
    os.makedirs(images_path, exist_ok=True)

    params = {
        "api_key": api_key,
        "count": IMAGE_COUNT
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    answer = response.json()

    images_links = [item["url"] for item in answer]

    for index, image_link in enumerate(images_links):
        extension = get_file_extension(image_link)
        filename = f"nasa_apod_{index}{extension}"
        download_image(image_link, filename)


def main():
    env = Env()
    env.read_env()
    api_key = env.str("NASA_API_KEY")
    fetch_nasa_apod(api_key)


if __name__ == "__main__":
    main()
