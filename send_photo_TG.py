import telegram
import argparse
import os
import random
from environs import Env


env = Env()
env.read_env()

TG_TOKEN = env.str("TG_TOKEN")
TG_CHAT_ID = env.str("TG_CHAT_ID")

bot = telegram.Bot(token=TG_TOKEN)


def send_image(image_path):
    try:
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=TG_CHAT_ID, photo=photo)
    except Exception as e:
        print(f"Ошибка при отправке: {e}")


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
    send_image(image_path)


if __name__ == "__main__":
    main()
