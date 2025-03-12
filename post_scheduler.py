import random
import os
import time
import argparse
from environs import Env
from send_photo_TG import send_image


def main():
    env = Env()
    env.read_env()
    images_path = 'images'

    parser = argparse.ArgumentParser(
        description="Автоматическая публикация фото в Telegram."
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=env.int("PUBLICATION_INTERVAL_HOURS", 4),
        help="Интервал между публикациями в часах "
             "(по умолчанию из .env или 4 ч)."
    )
    args = parser.parse_args()

    publication_interval_hours = args.interval

    while True:
        images = [os.path.join(images_path, img)
                  for img in os.listdir(images_path)]
        random.shuffle(images)
        secs_in_hour = 3600

        if not images:
            time.sleep(publication_interval_hours * secs_in_hour)
            continue

        for image in images:
            send_image(image)
            time.sleep(publication_interval_hours * secs_in_hour)


if __name__ == "__main__":
    main()
