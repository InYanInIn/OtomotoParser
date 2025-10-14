import os
import time

import telebot

import checkerService
import databaseService
import parser
from checkerService import check_new_ads, processed_urls
from parser import get_urls, get_ad_data, HEADERS
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))


def main_menu(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    is_checking = checkerService.is_checking(chat_id)
    btn1 = telebot.types.KeyboardButton("🔎 Choose filters")
    btn2 = telebot.types.KeyboardButton("🌐 Send a link")
    if is_checking:
        btn3 = telebot.types.KeyboardButton("⏹ Stop checking")
    else:
        btn3 = telebot.types.KeyboardButton("▶ Start checking")
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


@bot.message_handler(commands=['start'])
def show_menu(message):
    chat_id = message.from_user.id
    bot.send_message(chat_id, "Главное меню:", reply_markup=main_menu(chat_id))

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message, "Witaj! Wyślij mi link do ogłoszenia z otomoto.pl, a ja pobiorę dane o pojeździe.")
#     print("User started the bot. Chat ID:", message.from_user.id)


@bot.message_handler(commands=['check'])
def start_browsing(message):
    chat_id = message.from_user.id
    if parser.URL.get(chat_id) is None:
        bot.send_message(message.from_user.id, "No URL set. Please send a URL first.")
    else:
        if checkerService.is_checking(chat_id):
            bot.send_message(chat_id, "Ad checker is already running.")
            return
        bot.send_message(chat_id, "Starting the ad checker.")
        print("Starting ad checker for chat_id:", chat_id, "with URL:", parser.URL[chat_id])

        check_new_ads(bot, chat_id, parser.URL[chat_id])
        bot.send_message(chat_id, "Ad checker is being started.", reply_markup=main_menu(chat_id))




@bot.message_handler(commands=['stop'])
def stop_browsing(message):
    chat_id = message.from_user.id
    if not checkerService.is_checking(chat_id):
        bot.send_message(chat_id, "Ad checker is not running.")
        return
    checkerService.stop_checking(chat_id)
    bot.send_message(chat_id, "Ad checker being stopped.", reply_markup=main_menu(chat_id))


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id

    if call.data == "filters":
        # bot.send_message(call.message.chat.id, "Фильтры пока не реализованы.")
        pass
    elif call.data == "send_link":
        # bot.send_message(call.message.chat.id, "Send a link to Otomoto.pl listing.")
        pass
    elif call.data == "start":
        # bot.send_message(call.message.chat.id, "Start checking ✅")
        pass
    elif call.data == "stop":
        # bot.send_message(call.message.chat.id, "Stop checking ⏹")
        pass


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.from_user.id

    if message.text.startswith("🔎 Choose filters"):
        bot.send_message(chat_id, "Filters are not implemented yet, please choose link option.")
    elif message.text.startswith("🌐 Send a link"):
        bot.send_message(chat_id, "Send a link to Otomoto.pl listing.")
    elif message.text.startswith("▶ Start checking"):
        start_browsing(message)
    elif message.text.startswith("⏹ Stop checking"):
        stop_browsing(message)

    elif message.text.startswith("http"):
        bot.send_message(message.from_user.id, "Pobieram dane z ogłoszenia... Please wait.")
        parser.URL[chat_id] = message.text
        checkerService.processed_urls[chat_id] = get_urls(message.text, HEADERS)
        data = {}
        current = 0
        for url in checkerService.processed_urls[chat_id]:
            current += 1
            print(f"Processing {current}/{len(checkerService.processed_urls[chat_id])}: {url}")
            data[url] = get_ad_data(url, HEADERS)
            databaseService.save_ad_to_database(data[url])
            # bot.send_message(message.from_user.id, str(data[url]))

        bot.send_message(message.from_user.id, f"Done!")
        if current == 0:
            bot.send_message(message.from_user.id, "No ads found. Please check the URL and try again.")
        else:
            bot.send_message(message.from_user.id, f"Use ▶ Start checking button to start checking for new ads every minute.")


bot.infinity_polling()
