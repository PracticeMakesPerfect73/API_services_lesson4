import requests
import os
from get_file_extension import get_file_extension
import argparse


def fetch_spacex_launch(launch_id):
    base_url = 'https://api.spacexdata.com/v5/launches/'
    url = f"{base_url}{launch_id}"
    images_path = 'images'

    if not os.path.exists(images_path):
        os.mkdir(images_path)

    response = requests.get(url)
    response.raise_for_status()
    answer = response.json()

    images_links = answer['links']['flickr']['original']

    if not images_links:
        print("Нет доступных изображений для данного запуска.")
        return

    for index, image_link in enumerate(images_links):
        image_response = requests.get(image_link)
        image_response.raise_for_status()

        extension = get_file_extension(image_link)
        filename = f"spacex{index}{extension}"
        with open(os.path.join(images_path, filename), 'wb') as file:
            file.write(image_response.content)


def main():
    parser = argparse.ArgumentParser(
        description="Download spaceX launch images")
    parser.add_argument("launch_id", nargs="?",
                        default="latest", help="Идентификатор запуска")
    args = parser.parse_args()

    user_input = args.launch_id

    try:
        fetch_spacex_launch(user_input)
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка запроса: {e}")
    except KeyError:
        print("Ошибка: неожиданный формат ответа от API.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
