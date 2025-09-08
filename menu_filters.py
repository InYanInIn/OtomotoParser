# # словарь для хранения состояния фильтров по пользователю
# user_states = {}
#
# # список возможных фильтров (можно расширять)
# brands = ["BMW", "Audi", "Toyota"]
# models = {
#     "BMW": ["3 Series", "5 Series"],
#     "Audi": ["A4", "A6"],
#     "Toyota": ["Corolla", "Camry"]
# }
# generations = {
#     "3 Series": ["E90", "F30"],
#     "5 Series": ["E60", "G30"],
#     "A4": ["B8", "B9"],
#     "A6": ["C6", "C7"],
#     "Corolla": ["E150", "E210"],
#     "Camry": ["XV40", "XV70"]
# }
#
# @bot.callback_query_handler(func=lambda call: call.data == "filters")
# def choose_brand(call):
#     bot.answer_callback_query(call.id)
#     chat_id = call.message.chat.id
#     user_states[chat_id] = {}  # сброс состояния
#     markup = telebot.types.InlineKeyboardMarkup()
#     for b in brands:
#         markup.add(telebot.types.InlineKeyboardButton(b, callback_data=f"brand:{b}"))
#     bot.send_message(chat_id, "Выберите марку:", reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("brand:"))
# def choose_model(call):
#     bot.answer_callback_query(call.id)
#     chat_id = call.message.chat.id
#     brand = call.data.split(":")[1]
#     user_states[chat_id]["brand"] = brand
#
#     markup = telebot.types.InlineKeyboardMarkup()
#     for m in models[brand]:
#         markup.add(telebot.types.InlineKeyboardButton(m, callback_data=f"model:{m}"))
#     bot.edit_message_text(f"Марка выбрана: {brand}\nТеперь выберите модель:",
#                           chat_id, call.message.message_id, reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("model:"))
# def choose_generation(call):
#     bot.answer_callback_query(call.id)
#     chat_id = call.message.chat.id
#     model = call.data.split(":")[1]
#     user_states[chat_id]["model"] = model
#
#     markup = telebot.types.InlineKeyboardMarkup()
#     for g in generations[model]:
#         markup.add(telebot.types.InlineKeyboardButton(g, callback_data=f"gen:{g}"))
#     bot.edit_message_text(f"Модель выбрана: {model}\nТеперь выберите поколение:",
#                           chat_id, call.message.message_id, reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("gen:"))
# def choose_body_type(call):
#     bot.answer_callback_query(call.id)
#     chat_id = call.message.chat.id
#     gen = call.data.split(":")[1]
#     user_states[chat_id]["generation"] = gen
#
#     # пример выбора кузова
#     body_types = ["Sedan", "Coupe", "SUV"]
#     markup = telebot.types.InlineKeyboardMarkup()
#     for bt in body_types:
#         markup.add(telebot.types.InlineKeyboardButton(bt, callback_data=f"body:{bt}"))
#     bot.edit_message_text(f"Поколение выбрано: {gen}\nТеперь выберите тип кузова:",
#                           chat_id, call.message.message_id, reply_markup=markup)
#
#
# # дальше аналогично: цена от-до, год от-до, пробег, коробка, топливо, объем
