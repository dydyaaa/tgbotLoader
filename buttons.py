from telebot import types

func_btn = types.InlineKeyboardMarkup(row_width=1)
video_btn = types.InlineKeyboardMarkup(row_width=1)
back_btn = types.InlineKeyboardMarkup(row_width=1)

item1 = types.InlineKeyboardButton('Скачать видео', callback_data='download_video')
item2 = types.InlineKeyboardButton('Посмотреть статистику тг канала', callback_data='channel_stats')
item3 = types.InlineKeyboardButton('гпт', callback_data='gpt')

item4 = types.InlineKeyboardButton('VK', callback_data='vk')
item5 = types.InlineKeyboardButton('YouTube', callback_data='youtube')
item6 = types.InlineKeyboardButton('Inst', callback_data='instagram')

item7 = types.InlineKeyboardButton('Назад', callback_data='back')

func_btn.add(item1, item2, item3)
video_btn.add(item4, item5, item6)
back_btn.add(item7)
