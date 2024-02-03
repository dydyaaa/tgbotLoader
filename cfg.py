import os


# Токен бота
TOKEN = '916278807:AAGsNPTB7NkuJ5AKqRX2njl-JrXa-IZiCVI'

# Ссыулка на канал
channel_link = 'https://t.me/evdaktest'

# Канал, на который нужно подписаться
channel_name = "@" + channel_link[13:]

directory = path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "download_media")