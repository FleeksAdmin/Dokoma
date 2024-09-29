import telebot
import yt_dlp
import os
from telebot import types

# Ваш токен от BotFather
TOKEN = '6164368241:AAE_ifHXwOYY_K5WWDA26Im1NwU0a5kljxI'
bot = telebot.TeleBot(TOKEN)

# ID вашего канала
CHANNEL_USERNAME = '@btq_dev'  # Ваш канал

# Функция для загрузки видео с YouTube в MP4 (без необходимости использования ffmpeg)
def download_youtube_video(url):
    ydl_opts = {
        'format': 'mp4',  # Используем формат mp4, чтобы избежать необходимости слияния потоков
        'outtmpl': 'video.mp4'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    subscribe_button = types.InlineKeyboardButton("🩸ПОДПИСАТЬСЯ🩸", url="https://t.me/btq_dev")
    check_button = types.InlineKeyboardButton("ПРОВЕРИТЬ ПОДПИСКУ✅", callback_data="check_subscription")
    markup.add(subscribe_button)
    markup.add(check_button)
    
    bot.send_message(
        message.chat.id, 
        "<b>ПРИВЕТ! Я БОТ КОТОРЫЙ УМЕЕТ КАЧАТЬ ВИДЕО ИЗ ЮТУБ!</b>\n"
        "ДЛЯ НАЧАЛА ПОДПИШИСЬ НА КАНАЛ:", 
        parse_mode='HTML', 
        reply_markup=markup
    )

# Проверка подписки на канал
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    user_id = call.from_user.id
    member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
    
    if member.status in ['member', 'administrator', 'creator']:
        bot.answer_callback_query(call.id, "Вы подписаны на канал! Теперь можете отправить ссылку на видео.")
        bot.send_message(call.message.chat.id, "Отправьте ссылку на YouTube видео, и я скачаю его для вас.")
    else:
        bot.answer_callback_query(call.id, "😡Подпишитесь на канал, чтобы пользоваться ботом!😡")

# Обработка ссылок на YouTube
@bot.message_handler(func=lambda message: 'youtube.com' in message.text or 'youtu.be' in message.text)
def handle_video_request(message):
    # Проверка подписки перед загрузкой видео
    user_id = message.from_user.id
    member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
    
    if member.status in ['member', 'administrator', 'creator']:
        bot.send_message(message.chat.id, 'Загружаю видео...')
        
        video_url = message.text
        
        try:
            # Загрузка видео
            download_youtube_video(video_url)
            
            # Отправка видео пользователю
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            
            # Удаление загруженного файла
            os.remove('video.mp4')
        
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка: {e}')
    
    else:
        bot.send_message(message.chat.id, '😡Подпишитесь на канал, чтобы пользоваться ботом!😡')

# Запуск бота
bot.polling()
