import requests
import os
from urllib.parse import urlparse, unquote
from datetime import datetime
from environs import env


def get_file_extension(url):
    url = unquote(url)
    path = urlparse(url).path
    head, tail = os.path.split(path)
    root, extension = os.path.splitext(tail)
    return extension


def fetch_spacex_last_launch():
    url = 'https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a'
    images_path = 'images'
    extension = get_file_extension(url)

    if not os.path.exists(images_path):
        os.mkdir(images_path)

    response = requests.get(url)
    response.raise_for_status()
    answer = response.json()

    images_links = answer['links']['flickr']['original']

    for index, image_link in enumerate(images_links):
        image_response = requests.get(image_link)
        image_response.raise_for_status()

        filename = f"spacex{index}{extension}"
        with open(os.path.join(images_path, filename), 'wb') as file:
            file.write(image_response.content)


def fetch_nasa_apod(api_key):
    url = 'https://api.nasa.gov/planetary/apod'
    images_path = 'images'
    extension = get_file_extension(url)

    if not os.path.exists(images_path):
        os.mkdir(images_path)

    params = {"api_key": api_key,
              "count": 40
              }
    response = requests.get(url, params=params)
    response.raise_for_status()
    answer = response.json()

    images_links = [item["url"] for item in answer]

    for index, image_link in enumerate(images_links):
        image_response = requests.get(image_link)
        image_response.raise_for_status()

        filename = f"nasa_apod_{index}{extension}"
        with open(os.path.join(images_path, filename), 'wb') as file:
            file.write(image_response.content)


def fetch_nasa_epic(api_key):
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    images_path = 'images'

    if not os.path.exists(images_path):
        os.mkdir(images_path)

    params = {"api_key": api_key,
              }

    response = requests.get(url, params=params)
    response.raise_for_status()
    answer = response.json()
    for index, item in enumerate(answer[:10]):
        date_obj = datetime.strptime(item["date"],
                                     "%Y-%m-%d %H:%M:%S")
        year = "{:04d}".format(date_obj.year)
        month = "{:02d}".format(date_obj.month)
        day = "{:02d}".format(date_obj.day)
        image_name = item["image"]
        image_url = ("https://api.nasa.gov/EPIC/archive/natural/{}/"
                     "{}/{}/png/{}.png?api_key={}").format(
            year, month, day, image_name, api_key
        )
        image_response = requests.get(image_url)
        image_response.raise_for_status()

        filename = f"nasa_epic_{index}.png"
        with open(os.path.join(images_path, filename), 'wb') as file:
            file.write(image_response.content)


def main():
    env.read_env()
    api_key = env.str("API_KEY")
    fetch_spacex_last_launch()
    fetch_nasa_apod(api_key)
    fetch_nasa_epic(api_key)


if __name__ == "__main__":
    main()
