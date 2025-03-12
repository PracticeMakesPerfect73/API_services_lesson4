import requests
from image_operations_helper import get_file_extension, download_image
import argparse


def fetch_spacex_launch(launch_id):
    base_url = 'https://api.spacexdata.com/v5/launches/'
    url = f"{base_url}{launch_id}"

    response = requests.get(url)
    response.raise_for_status()
    answer = response.json()

    images_links = answer['links']['flickr']['original']

    if not images_links:
        print("Нет доступных изображений для данного запуска.")
        return

    for index, image_link in enumerate(images_links):
        extension = get_file_extension(image_link)
        filename = f"spacex{index}{extension}"
        download_image(image_link, filename)


def main():
    parser = argparse.ArgumentParser(
        description="Download spaceX launch images")
    parser.add_argument("launch_id", nargs="?",
                        default="latest", help="Идентификатор запуска")
    args = parser.parse_args()

    launch_id = args.launch_id
    fetch_spacex_launch(launch_id)


if __name__ == "__main__":
    main()
