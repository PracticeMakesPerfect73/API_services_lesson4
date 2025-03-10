import requests
import os
from datetime import datetime
from environs import env


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
    try:
        fetch_nasa_epic(api_key)
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка запроса: {e}")
    except KeyError:
        print("Ошибка: неожиданный формат ответа от API.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
