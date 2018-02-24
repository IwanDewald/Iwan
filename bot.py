
#!/usr/bin/venv python
# -*- coding: utf-8 -*-
import os
import socket

import telebot
from flask import Flask, request
from werkzeug.contrib.fixers import ProxyFix

import config
import constants 
import utils
import storage
# import cherrypy


# WEBHOOK_HOST = '93.170.131.202'
# WEBHOOK_PORT = 443 
# WEBHOOK_LISTEN = '0.0.0.0'  

# WEBHOOK_SSL_CERT = './webhook_cert.pem' 
# WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  

# WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
# WEBHOOK_URL_PATH = "/%s/" % (config.token)


# class WebhookServer(object):
#     @cherrypy.expose
#     def index(self):
#         if 'content-length' in cherrypy.request.headers and \
#                         'content-type' in cherrypy.request.headers and \
#                         cherrypy.request.headers['content-type'] == 'application/json':
#             length = int(cherrypy.request.headers['content-length'])
#             json_string = cherrypy.request.body.read(length).decode("utf-8")
#             update = telebot.types.Update.de_json(json_string)
            
#             bot.process_new_updates([update])
#             return ''
#         else:
#             raise cherrypy.HTTPError(403)

bot = telebot.TeleBot(config.token)

app = Flask(__name__)
URL_PATH = 'https://3466532a.ngrok.io/531911280:AAHoFolyb09Fi8PCHNZkOaZmadxwhth4F1U'
print(socket.gethostname())

# ловим ответ от телеграмма
@app.route("/{}".format(config.token), methods=['GET', 'POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return ''


# Устанавливаем веб-хук (который не устанавливается отсюда)
@app.route("/")
def webhook():
    print('webhook')
    bot.remove_webhook()
    bot.set_webhook(url=URL_PATH, sertificate=open('public.pem', 'r'))
    return ''


@bot.message_handler(commands=["start"])
def select_language(message):
	print(bot.get_webhook_info() )
	storage.set_user_string(message.chat.id)
	keyboard = telebot.types.InlineKeyboardMarkup()
	keyboard.add(telebot.types.InlineKeyboardButton(text=constants.ru, callback_data='ru'))
	keyboard.add(telebot.types.InlineKeyboardButton(text=constants.eng,callback_data='eng'))
	bot.send_message(message.chat.id,text=constants.select_language,reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['ru','eng','back_to_menu'])
def back_to_menu(call):
	"""
	
	"""
	keyboard = telebot.types.InlineKeyboardMarkup()
	keyboard.add(telebot.types.InlineKeyboardButton(text=constants.order, callback_data='order'))
	keyboard.add(telebot.types.InlineKeyboardButton(text=constants.redact_profile, callback_data='redact'))
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=constants.language_selected, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == constants.redact_profile)
def list_of_items(message):
	storage.drop_editing_item(message.chat.id)
	keyboard = telebot.types.InlineKeyboardMarkup()
	app_form = utils.send_app_form(storage.get_user_string(message.chat.id))
	items = constants.app_form_ru
	keyboard.add(telebot.types.InlineKeyboardButton(text=items['name'], callback_data='name'),telebot.types.InlineKeyboardButton(text=items['country'], callback_data='country'))
	keyboard.add(telebot.types.InlineKeyboardButton(text=items['city'], callback_data='city'),telebot.types.InlineKeyboardButton(text=items['occupation'] , callback_data='occupation'))
	keyboard.add(telebot.types.InlineKeyboardButton(text=items['birthdate'], callback_data='birthdate'),telebot.types.InlineKeyboardButton(text=items['favorite'], callback_data='favorite'))
	#keyboard.add(telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_app_form"))

	bot.send_message(message.chat.id,text=app_form,reply_markup=keyboard)

	
@bot.callback_query_handler(func=lambda call: call.data == "redact" or call.data == "back_to_redact")
def list_of_items(call):
	storage.drop_editing_item(call.message.chat.id)
	keyboard = telebot.types.InlineKeyboardMarkup()
	app_form = utils.send_app_form(storage.get_user_string(call.message.chat.id))
	items = constants.app_form_ru
	keyboard.add(telebot.types.InlineKeyboardButton(text=items['name'], callback_data='name'),telebot.types.InlineKeyboardButton(text=items['country'], callback_data='country'))
	keyboard.add(telebot.types.InlineKeyboardButton(text=items['city'], callback_data='city'),telebot.types.InlineKeyboardButton(text=items['occupation'] , callback_data='occupation'))
	keyboard.add(telebot.types.InlineKeyboardButton(text=items['birthdate'], callback_data='birthdate'),telebot.types.InlineKeyboardButton(text=items['favorite'], callback_data='favorite'))
	keyboard.add(telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_menu"))

	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=app_form, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in constants.app_form_ru.keys())
def edit_items(call):
	if call.data == 'name':
		storage.prepare_edit_user_string(chat_id = call.message.chat.id, editing_item = 'name')
		mes_text = constants.redact_name
	if call.data == 'country':
		storage.prepare_edit_user_string(chat_id = call.message.chat.id, editing_item = 'country')
		mes_text = constants.redact_country
	if call.data == 'city':
		storage.prepare_edit_user_string(chat_id = call.message.chat.id, editing_item = 'city')
		mes_text = constants.redact_city
	if call.data == 'occupation':
		storage.prepare_edit_user_string(chat_id = call.message.chat.id, editing_item = 'occupation')
		mes_text = constants.redact_occupation
	if call.data == 'birthdate':
		storage.prepare_edit_user_string(chat_id = call.message.chat.id, editing_item = 'birthdate')
		mes_text = constants.redact_birthdate
	if call.data == 'favorite':
		storage.prepare_edit_user_string(chat_id = call.message.chat.id, editing_item = 'favorite')
		mes_text = constants.redact_favorite


	keyboard =telebot.types.InlineKeyboardMarkup()
	callback_button1 = telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_redact")
	keyboard.add(callback_button1)
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mes_text, reply_markup=keyboard)

	

	print(storage.get_user_string(call.message.chat.id))




@bot.message_handler(func = lambda message: message.text == 'ok')
def clear_storage(message):
	storage.clear_all()
	print(utils.send_order_list(message.chat.id))

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
	bot.edit_message_text(chat_id = call.message.chat.id, text = mes_text, message_id=call.message.message_id, reply_markup = keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'order_coffee')
def order_coffee(call):
	keyboard = telebot.types.InlineKeyboardMarkup()
	for i in constants.coffee_list:
		keyboard.add(telebot.types.InlineKeyboardButton(text=i['text'], callback_data=i['call']))
		keyboard.add(telebot.types.InlineKeyboardButton(text=constants.plus, callback_data='+'+i['call']), telebot.types.InlineKeyboardButton(text=constants.minus, callback_data='-'+i['call']) )
	keyboard.add(telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_order"))
	mes_text = utils.send_order_list(call.message.chat.id)
	bot.edit_message_text(chat_id = call.message.chat.id, text = mes_text, message_id=call.message.message_id, reply_markup = keyboard)

@bot.callback_query_handler(func=lambda call: call.data[0] == '-' or call.data[0] == '+')
def redact_order(call):
	if   call.data[0] == '+':
		storage.add_to_order(chat_id=call.message.chat.id,data=call.data[1:])
		print(storage.get_user_string(chat_id=call.message.chat.id))
		bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='+'+str(call.data[-3:])+constants.to_bill)
	if call.data[0] == '-':
		storage.remove_from_order(chat_id=call.message.chat.id,data=call.data[1:])
		print(storage.get_user_string(chat_id=call.message.chat.id))
		bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='-'+str(call.data[-3:])+constants.from_bill)
		
	mes_text = utils.send_order_list(call.message.chat.id)
	keyboard = telebot.types.InlineKeyboardMarkup()
	for i in constants.coffee_list:
		keyboard.add(telebot.types.InlineKeyboardButton(text=i['text'], callback_data=i['call']))
		keyboard.add(telebot.types.InlineKeyboardButton(text=constants.plus, callback_data='+'+i['call']), telebot.types.InlineKeyboardButton(text=constants.minus, callback_data='-'+i['call']) )
	keyboard.add(telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_order"))
	bot.edit_message_text(chat_id = call.message.chat.id, text = mes_text, message_id=call.message.message_id, reply_markup = keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'checkout')
def checkout(call):
	bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=constants.zakaz)


@bot.message_handler(content_types=["text"])
def edit_app_form(message):
	editing_item = storage.get_editing_item(message.chat.id)
	print(editing_item,'\n')
	if editing_item :
		storage.edit_user_string(chat_id = message.chat.id ,data = message.text)
		keyboard = telebot.types.InlineKeyboardMarkup()
		app_form = utils.send_app_form(storage.get_user_string(message.chat.id))
		items = constants.app_form_ru
		keyboard.add(telebot.types.InlineKeyboardButton(text=items['name'], callback_data='name'),telebot.types.InlineKeyboardButton(text=items['country'], callback_data='country'))
		keyboard.add(telebot.types.InlineKeyboardButton(text=items['city'], callback_data='city'),telebot.types.InlineKeyboardButton(text=items['occupation'] , callback_data='occupation'))
		keyboard.add(telebot.types.InlineKeyboardButton(text=items['birthdate'], callback_data='birthdate'),telebot.types.InlineKeyboardButton(text=items['favorite'], callback_data='favorite'))
		keyboard.add(telebot.types.InlineKeyboardButton(text=constants.back, callback_data="back_to_menu"))
		bot.send_message(message.chat.id,text=app_form,reply_markup=keyboard)
	print(message.text.encode())

@bot.message_handler(content_types = 'photo')
def photo(message):
	print(message.photo[2])
	bot.send_message(chat_id = message.chat.id, text = message.photo[2])

# bot.remove_webhook()

 
# bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                 certificate=open(WEBHOOK_SSL_CERT, 'r'))

# cherrypy.config.update({
#     'server.socket_host': WEBHOOK_LISTEN,
#     'server.socket_port': WEBHOOK_PORT,
#     'server.ssl_module': 'builtin',
#     'server.ssl_certificate': WEBHOOK_SSL_CERT,
#     'server.ssl_private_key': WEBHOOK_SSL_PRIV
# })

# cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
	app.run(port=os.environ.get('PORT', 5000))

