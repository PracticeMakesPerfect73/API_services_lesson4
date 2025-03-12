import requests
import os
from environs import Env
from get_file_extension import get_file_extension


def fetch_nasa_apod(api_key):
    url = 'https://api.nasa.gov/planetary/apod'
    images_path = 'images'
    os.makedirs(images_path, exist_ok=True)

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

        extension = get_file_extension(image_link)
        filename = f"nasa_apod_{index}{extension}"
        with open(os.path.join(images_path, filename), 'wb') as file:
            file.write(image_response.content)


def main():
    env = Env()
    env.read_env()
    api_key = env.str("NASA_API_KEY")
    fetch_nasa_apod(api_key)


if __name__ == "__main__":
    main()
