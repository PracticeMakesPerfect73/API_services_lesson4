import telegram
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
