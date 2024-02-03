import telebot, os, cfg, tg_stats, g4f, inst, glob
import buttons as btn
from pytube import YouTube

bot = telebot.TeleBot(cfg.TOKEN)
channel_username = cfg.channel_name
directory = cfg.directory

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_in_channel = bot.get_chat_member(channel_username, user_id).status in ['member', 'administrator', 'creator']
    if user_in_channel:
        bot.send_message(message.chat.id, f"Стартовое сообщение", reply_markup=btn.func_btn)
    else:
        bot.send_message(message.chat.id, 'Для использования бота, подпишитесь на наш канал: ', reply_markup=btn.link_btn)

@bot.message_handler(func=lambda message: True)
def func(message):
    user_id = message.from_user.id
    user_in_channel = bot.get_chat_member(channel_username, user_id).status in ['member', 'administrator', 'creator']
    if not user_in_channel:
        bot.send_message(message.chat.id, 'Для использования бота, подпишитесь на наш канал: ', reply_markup=btn.link_btn)
        return 0
    if message.text == 'Посмотреть статистику тг канала':
        bot.send_message(message.chat.id, "Введите ссылку на тг канал:", reply_markup=btn.back_btn)
        bot.register_next_step_handler(message, tg_stat) 
    elif message.text == 'Скачать видео':
        bot.send_message(message.chat.id, "Введите ссылку на видео:", reply_markup=btn.back_btn)
        bot.register_next_step_handler(message, choose_url)
    elif message.text == 'VK':
        bot.send_message(message.chat.id, "Введите ссылку на видео:")
        bot.send_message(message.chat.id, "В разработке", reply_markup=btn.func_btn)
    elif message.text == 'YouTube':
        bot.send_message(message.chat.id, "Введите ссылку на видео:", reply_markup=btn.back_btn)
        bot.register_next_step_handler(message, download_yt)
    elif message.text == 'Instagram':
        bot.send_message(message.chat.id, "Введите ссылку на видео:")
        bot.register_next_step_handler(message, download_inst)
    elif message.text == 'гпт':
        bot.send_message(message.chat.id, "Введите ваш запрос:", reply_markup=btn.back_btn)
        bot.register_next_step_handler(message, ask)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, f'Главное меню', reply_markup=btn.func_btn)
    else:
        bot.send_message(message.chat.id, f'Простите, я вас не понимаю.')

def choose_url(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, f'Главное меню', reply_markup=btn.func_btn)
        return 0
    if message.text[:14] == 'https://vk.com':
        bot.send_message(message.chat.id, "В разработке", reply_markup=btn.func_btn)
    elif message.text[:23] == 'https://www.youtube.com':
        (download_yt(message))
    elif message.text[:25] == 'https://www.instagram.com':
        (download_inst(message))
    else:
        bot.send_message(message.chat.id, f'Извините, но этот источник мне неизвестен.', reply_markup=btn.func_btn)

def ask(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, f'Главное меню', reply_markup=btn.func_btn)
        return 0
    try:
        response = g4f.ChatCompletion.create(
            model = g4f.models.gpt_4,
            messages=[{"role": "user", "content": message.text}],
        )  
        bot.send_message(message.chat.id, response, reply_markup=btn.func_btn)
    except Exception as e:
        bot.send_message(message.chat.id, 'При выполенении запроса произошла ошибка', reply_markup=btn.func_btn)
        print(e)

def download_inst(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, f'Главное меню', reply_markup=btn.func_btn)
        return 0
    
    try:
        inst.main(message.text)
        mp4_files = glob.glob(os.path.join(directory, '*.mp4'))
        latest_mp4_file = max(mp4_files, key=os.path.getmtime)
        full_path = os.path.abspath(latest_mp4_file)
        bot.send_video(message.chat.id, open(full_path, 'rb'), reply_markup=btn.func_btn)
        os.remove(full_path)

    except Exception as e:
        bot.send_message(message.chat.id, f'При скачивании видео возникла ошибка!', reply_markup=btn.func_btn)
        print(e)

def download_yt(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, f'Главное меню', reply_markup=btn.func_btn)
        return 0
    try:
        yt = YouTube(message.text)
        video = yt.streams.filter(file_extension='mp4', progressive=True).get_highest_resolution()
        video_title = ''.join(char for char in video.title if char.isalnum() or char in (' ', '.', '_', '|'))
        folder_name = 'download_media'
        os.makedirs(folder_name, exist_ok=True)
        video_path = os.path.join(folder_name, video_title + '.mp4')
        video.download(output_path=folder_name, filename=video_title + '.mp4')
        bot.send_video(message.chat.id, open(video_path, 'rb'), reply_markup=btn.func_btn)
        os.remove(video_path)
    except Exception as e:
        bot.send_message(message.chat.id, f'При скачивании видео возникла ошибка!', reply_markup=btn.func_btn)
        print(e)

def tg_stat(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, f'Главное меню', reply_markup=btn.func_btn)
        return 0
    if len(message.text) < 14:
        bot.send_message(message.chat.id, f'Введите корректную ссылку')
        bot.register_next_step_handler(message, tg_stat)
    else:
        result = tg_stats.stat(message.text)
        bot.send_message(message.chat.id, result, reply_markup=btn.func_btn)

if __name__ == "__main__":
    bot.polling()