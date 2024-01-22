import telebot, os, cfg, tg_stats, g4f
import buttons as btn
from pytube import YouTube

bot = telebot.TeleBot(cfg.TOKEN)
channel_username = cfg.channel_name

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_in_channel = bot.get_chat_member(channel_username, user_id).status in ['member', 'administrator', 'creator']
    if user_in_channel:
        bot.send_message(message.chat.id, f"Стартовое сообщение", reply_markup=btn.func_btn)
    else:
        bot.send_message(message.chat.id, 'Для использования бота, подпишитесь на наш канал: ' + channel_username)

@bot.callback_query_handler(func=lambda call: True)
def func(call):
    if call.data == 'channel_stats':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите ссылку на тг канал:")
        bot.register_next_step_handler(call.message, tg_stat)
    elif call.data == 'download_video':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Выберете источник для скачивания видео", reply_markup=btn.video_btn)  
    elif call.data == 'vk':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите ссылку на видео:")
        bot.send_message(call.message.chat.id, "В разработке")
        start(call.message)
    elif call.data == 'youtube':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите ссылку на видео:")
        bot.register_next_step_handler(call.message, download_yt)
    elif call.data == 'instagram':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите ссылку на видео:")
        bot.send_message(call.message.chat.id, "В разработке")
        start(call.message)
    elif call.data == 'gpt':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите ваш запрос:")
        bot.register_next_step_handler(call.message, ask)

@bot.message_handler(func=lambda message: True)
def menu(message):
    bot.send_message(message.chat.id, f'Простите, я вас не понимаю.')

def ask(message):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": message.text}],
    )  
    bot.send_message(message.chat.id, response)
    start(message)

def download_yt(message):
    try:
        yt = YouTube(message.text)
        video = yt.streams.filter(file_extension='mp4', progressive=True).get_highest_resolution()
        video_title = ''.join(char for char in video.title if char.isalnum() or char in (' ', '.', '_', '_'))
        folder_name = 'download_media'
        os.makedirs(folder_name, exist_ok=True)
        video_path = os.path.join(folder_name, video_title + '.mp4')
        video.download(output_path=folder_name, filename=video_title + '.mp4')
        bot.send_video(message.chat.id, open(video_path, 'rb'))
        os.remove(video_path)
        start(message)
    except Exception as e:
        bot.send_message(message.chat.id, f'При скачивании видео возникла ошибка!')
        print(e)
        start(message)

def tg_stat(message):
    if len(message.text) < 14:
        bot.send_message(message.chat.id, f'Введите корректную ссылку')
        bot.register_next_step_handler(message, tg_stat)
    else:
        result = tg_stats.stat(message.text)
        bot.send_message(message.chat.id, result)
        start(message)

if __name__ == "__main__":
    bot.polling()