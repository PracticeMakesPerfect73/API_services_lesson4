import telegram
from environs import env

def send_photo(photo_path):
    env.read_env()
    TG_TOKEN = env.str("TG_TOKEN")
    TG_CHAT_ID = env.str("TG_CHAT_ID")
    bot = telegram.Bot(token=TG_TOKEN)
    bot.send_photo(chat_id=TG_CHAT_ID, photo=open(f'{photo_path}', 'rb'))


if __name__ == "__main__":
    send_photo(photo_path)