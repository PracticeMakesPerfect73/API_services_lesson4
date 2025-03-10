import telegram
from environs import env

env.read_env()
TG_TOKEN = env.str("TG_TOKEN")
TG_CHAT_ID = env.str("TG_CHAT_ID")
bot = telegram.Bot(token=TG_TOKEN)
updates = bot.get_updates()
print(updates[0])
print(bot.get_me())
bot.send_message(text='Hi John!', chat_id=TG_CHAT_ID)