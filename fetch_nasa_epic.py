import requests
import os
from datetime import datetime
from environs import Env
from image_operations_helper import download_image
from urllib.parse import urlencode, urlunparse

IMAGE_COUNT = 10


def fetch_nasa_epic(api_key):
    url = 'https://api.nasa.gov/EPIC/api/natural/image'
    images_path = 'images'
    os.makedirs(images_path, exist_ok=True)

    params = {
        "api_key": api_key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    epic_images = response.json()
    for index, epic_entry in enumerate(epic_images[:IMAGE_COUNT]):
        date_obj = datetime.strptime(epic_entry["date"],
                                     "%Y-%m-%d %H:%M:%S")
        year = "{:04d}".format(date_obj.year)
        month = "{:02d}".format(date_obj.month)
        day = "{:02d}".format(date_obj.day)
        image_name = epic_entry["image"]
        image_url_path = (
            f"EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
        )
        image_url = urlunparse((
            "https", "api.nasa.gov", image_url_path, "", urlencode(params), ""
        ))

        filename = f"nasa_epic_{index}.png"
        download_image(image_url, filename)


def main():
    env = Env()
    env.read_env()
    api_key = env.str("NASA_API_KEY")
    fetch_nasa_epic(api_key)


if __name__ == "__main__":
    main()
