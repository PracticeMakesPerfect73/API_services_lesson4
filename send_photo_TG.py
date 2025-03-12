import telegram
import argparse
import os
import random
from environs import Env


def send_image(image_path):
    with open(image_path, 'rb') as photo:
        bot.send_photo(chat_id=TG_CHAT_ID, photo=photo)



def main():
    parser = argparse.ArgumentParser(
        description="Отправка фото в Telegram-канал"
    )
    parser.add_argument("image",
                        nargs="?",
                        default=None,
                        help="Путь к фото (если не указано - случайное)")
    args = parser.parse_args()

    images_path = 'images'
    images = [os.path.join(images_path, img)
              for img in os.listdir(images_path)]

    image_path = args.image if args.image else random.choice(images)
    try:
        send_image(image_path)
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    except ConnectionError as e:
        print(f"Ошибка соединения: {e}")

if __name__ == "__main__":
    env = Env()
    env.read_env()

    TG_TOKEN = env.str("TG_TOKEN")
    TG_CHAT_ID = env.str("TG_CHAT_ID")

    bot = telegram.Bot(token=TG_TOKEN)
    main()
