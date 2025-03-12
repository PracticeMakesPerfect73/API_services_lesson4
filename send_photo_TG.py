import telegram
import argparse
import os
import random
from environs import Env


def send_image(bot, tg_chat_id, image_path):
    with open(image_path, 'rb') as photo:
        bot.send_photo(chat_id=tg_chat_id, photo=photo)



def main():
    env = Env()
    env.read_env()

    tg_token = env.str("TG_TOKEN")
    tg_chat_id = env.str("TG_CHAT_ID")

    bot = telegram.Bot(token=tg_token)

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
        send_image(bot, tg_chat_id, image_path)
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    except ConnectionError as e:
        print(f"Ошибка соединения: {e}")

if __name__ == "__main__":
    main()
