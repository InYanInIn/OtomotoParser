import threading
import time
import databaseService

from parser import get_urls, HEADERS, get_ad_data, get_new_urls

processed_urls = {}
timers = {}


def check_new_ads(bot, chat_id, message_url):
    global processed_urls
    global timers
    print(time.strftime("%H:%M") + " - Checking for new ads...")
    print(processed_urls[chat_id])
    urls = get_new_urls(processed_urls[chat_id], message_url, HEADERS)

    new_ads = []
    for url in urls:
        if url not in processed_urls[chat_id]:
            ad_data = get_ad_data(url, HEADERS)
            new_ads.append(ad_data)
            processed_urls[chat_id].append(url)

    if len(new_ads) > 0:
        print(f"Found {len(new_ads)} new ads.")
        for ad in new_ads:
            databaseService.save_ad_to_database(ad)
            bot.send_message(chat_id=chat_id, text=str(ad))
    else:
        # bot.send_message(chat_id="724762862", text="No new ads found.")
        print("No new ads found. " + time.strftime("%H:%M"))

    timers[chat_id] = threading.Timer(60, lambda: check_new_ads(bot, chat_id, message_url))
    timers[chat_id].start()

    return new_ads


def stop_checking(chat_id):
    global timers
    if chat_id in timers:
        timers[chat_id].cancel()
        del timers[chat_id]

def is_checking(chat_id):
    global timers
    return chat_id in timers and timers[chat_id].is_alive()

