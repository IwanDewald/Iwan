# bot.py
#!/usr/bin/venv python
# -*- coding: utf-8 -*-
import os

import telebot
from flask import Flask, request
from flask_sslify import SSLify

import config
import constants
import utils
import storage
import log

bot = telebot.TeleBot(config.token)
app = Flask(__name__)
SSL = SSLify(app)


@app.route("/{}".format(config.token), methods=['GET', 'POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    log.making_logs('Bot is processing new message')
    return ''


@app.route("/")
def web_hook():
    log.making_logs('Trying set webhook')
    bot.remove_webhook()
    bot.set_webhook(url=config.app_address)
    log.making_logs(bot.get_webhook_info())
    return ''


@bot.message_handler(commands=["start"])
def select_language(message):
    log.making_logs('Bot got "start" command')
    storage.set_user_string(message.chat.id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text=constants.ru, callback_data='ru'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=constants.eng, callback_data='eng'))
    bot.send_message(message.chat.id, text=constants.select_language, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['ru', 'eng', 'back_to_menu'])
def back_to_menu(call):
    """

    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text=constants.order, callback_data='order'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=constants.redact_profile, callback_data='redact'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=constants.language_selected, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == constants.redact_profile)
def list_of_items(message):
    storage.drop_editing_item(message.chat.id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    app_form = utils.send_app_form(storage.get_user_string(message.chat.id))
    items = constants.app_form_ru
    keyboard.add(telebot.types.InlineKeyboardButton(text=items['name'], callback_data='name'),
                 telebot.types.InlineKeyboardButton(text=items['country'], callback_data='country'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=items['city'], callback_data='city'),
                 telebot.types.InlineKeyboardButton(text=items['occupation'], callback_data='occupation'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=items['birthdate'], callback_data='birthdate'),
                 telebot.types.InlineKeyboardButton(text=items['favorite'], callback_data='favorite'))
    # keyboard.add(telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_app_form"))

    bot.send_message(message.chat.id, text=app_form, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "redact" or call.data == "back_to_redact")
def list_of_items(call):
    storage.drop_editing_item(call.message.chat.id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    app_form = utils.send_app_form(storage.get_user_string(call.message.chat.id))
    items = constants.app_form_ru
    keyboard.add(telebot.types.InlineKeyboardButton(text=items['name'], callback_data='name'),
                 telebot.types.InlineKeyboardButton(text=items['country'], callback_data='country'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=items['city'], callback_data='city'),
                 telebot.types.InlineKeyboardButton(text=items['occupation'], callback_data='occupation'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=items['birthdate'], callback_data='birthdate'),
                 telebot.types.InlineKeyboardButton(text=items['favorite'], callback_data='favorite'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_menu"))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=app_form,
                          reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in constants.app_form_ru.keys())
def edit_items(call):
    '''
    Собственно, чтобы ты заметил!
    Не лучше ли вот так организовывать дерево? PyCharm рекомендует.
    :param call:
    :return:
    '''
    mes_text = ''  # от вот этого надо бы избавиться по-хорошему. В другой файлик, например
    if call.data == 'name':
        storage.prepare_edit_user_string(chat_id=call.message.chat.id, editing_item='name')
        mes_text = constants.redact_name
    elif call.data == 'country':
        storage.prepare_edit_user_string(chat_id=call.message.chat.id, editing_item='country')
        mes_text = constants.redact_country
    elif call.data == 'city':
        storage.prepare_edit_user_string(chat_id=call.message.chat.id, editing_item='city')
        mes_text = constants.redact_city
    elif call.data == 'occupation':
        storage.prepare_edit_user_string(chat_id=call.message.chat.id, editing_item='occupation')
        mes_text = constants.redact_occupation
    elif call.data == 'birthdate':
        storage.prepare_edit_user_string(chat_id=call.message.chat.id, editing_item='birthdate')
        mes_text = constants.redact_birthdate
    elif call.data == 'favorite':
        storage.prepare_edit_user_string(chat_id=call.message.chat.id, editing_item='favorite')
        mes_text = constants.redact_favorite

    keyboard = telebot.types.InlineKeyboardMarkup()
    callback_button1 = telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_redact")
    keyboard.add(callback_button1)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mes_text,
                          reply_markup=keyboard)

    log.making_logs(f'\n{storage.get_user_string(call.message.chat.id)}\n')


@bot.message_handler(func=lambda message: message.text == 'ok')
def clear_storage(message):
    storage.clear_all()
    log.making_logs(utils.send_order_list(message.chat.id))


@bot.callback_query_handler(func=lambda call: call.data == 'order' or call.data == 'back_to_order')
def make_order(call):
    arr = storage.get_user_string(call.message.chat.id)['order']
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text=constants.coffee, callback_data='order_coffee'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=constants.dessert, callback_data='order_dessert'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=constants.sandwitch, callback_data='order_sandwitch'))
    if arr:
        keyboard.add(telebot.types.InlineKeyboardButton(text=constants.checkout, callback_data='checkout'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=constants.back_to_menu, callback_data="back_to_menu"))
    mes_text = utils.send_order_list(call.message.chat.id)
    bot.edit_message_text(chat_id=call.message.chat.id, text=mes_text, message_id=call.message.message_id,
                          reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'order_coffee')
def order_coffee(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in constants.coffee_list:
        keyboard.add(telebot.types.InlineKeyboardButton(text=i['text'], callback_data=i['call']))
        keyboard.add(telebot.types.InlineKeyboardButton(text=constants.plus, callback_data='+' + i['call']),
                     telebot.types.InlineKeyboardButton(text=constants.minus, callback_data='-' + i['call']))
    keyboard.add(telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_order"))
    mes_text = utils.send_order_list(call.message.chat.id)
    bot.edit_message_text(chat_id=call.message.chat.id, text=mes_text, message_id=call.message.message_id,
                          reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data[0] == '-' or call.data[0] == '+')
def redact_order(call):
    if call.data[0] == '+':
        storage.add_to_order(chat_id=call.message.chat.id, data=call.data[1:])
        print(storage.get_user_string(chat_id=call.message.chat.id))
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text='+' + str(call.data[-3:]) + constants.to_bill)
    if call.data[0] == '-':
        storage.remove_from_order(chat_id=call.message.chat.id, data=call.data[1:])
        print(storage.get_user_string(chat_id=call.message.chat.id))
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text='-' + str(call.data[-3:]) + constants.from_bill)

    mes_text = utils.send_order_list(call.message.chat.id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in constants.coffee_list:
        keyboard.add(telebot.types.InlineKeyboardButton(text=i['text'], callback_data=i['call']))
        keyboard.add(telebot.types.InlineKeyboardButton(text=constants.plus, callback_data='+' + i['call']),
                     telebot.types.InlineKeyboardButton(text=constants.minus, callback_data='-' + i['call']))
    keyboard.add(telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_order"))
    bot.edit_message_text(chat_id=call.message.chat.id, text=mes_text, message_id=call.message.message_id,
                          reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'checkout')
def checkout(call):
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=constants.zakaz)


@bot.message_handler(content_types=["text"])
def edit_app_form(message):
    editing_item = storage.get_editing_item(message.chat.id)
    log.making_logs(editing_item)
    if editing_item:
        storage.edit_user_string(chat_id=message.chat.id, data=message.text)
        keyboard = telebot.types.InlineKeyboardMarkup()
        app_form = utils.send_app_form(storage.get_user_string(message.chat.id))
        items = constants.app_form_ru
        keyboard.add(telebot.types.InlineKeyboardButton(text=items['name'], callback_data='name'),
                     telebot.types.InlineKeyboardButton(text=items['country'], callback_data='country'))
        keyboard.add(telebot.types.InlineKeyboardButton(text=items['city'], callback_data='city'),
                     telebot.types.InlineKeyboardButton(text=items['occupation'], callback_data='occupation'))
        keyboard.add(telebot.types.InlineKeyboardButton(text=items['birthdate'], callback_data='birthdate'),
                     telebot.types.InlineKeyboardButton(text=items['favorite'], callback_data='favorite'))
        keyboard.add(telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_menu"))
        bot.send_message(message.chat.id, text=app_form, reply_markup=keyboard)
    log.making_logs(message.text.encode())


@bot.message_handler(content_types='photo')
def photo(message):
    log.making_logs(message.photo[2])
    bot.send_message(chat_id=message.chat.id, text=message.photo[2])


if __name__ == '__main__':
    try:
        log.making_logs('The script was started')
        log.making_logs(bot.get_webhook_info())
        app.run(port=os.environ.get('PORT', 5000))
    except Exception as e:
        log.making_logs(e)
	
