from telebot import types
import cfg

func_btn = types.ReplyKeyboardMarkup(row_width=1)
video_btn = types.ReplyKeyboardMarkup(row_width=1)
link_btn = types.InlineKeyboardMarkup(row_width=1)
back_btn = types.ReplyKeyboardMarkup(row_width=1)
clear = types.ReplyKeyboardRemove()

item1 = types.KeyboardButton('Скачать видео') 
item2 = types.KeyboardButton('Посмотреть статистику тг канала') 
item3 = types.KeyboardButton('гпт') 

item4 = types.KeyboardButton('VK') 
item5 = types.KeyboardButton('YouTube') 
item6 = types.KeyboardButton('Instagram') 

item7 = types.KeyboardButton('Назад') 
item8 = types.InlineKeyboardButton('ТГ канал', url=cfg.channel_link)

func_btn.add(item1, item2, item3)
video_btn.add(item4, item5, item6, item7)
link_btn.add(item8)
back_btn.add(item7)