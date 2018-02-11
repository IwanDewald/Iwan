#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shelve
from config import shelve_name
from constants import app_form 

def set_user_string(chat_id):
	with shelve.open(shelve_name) as shl:
		shl[str(chat_id)] = app_form
		data = list(shl.keys())
	return data

def set_user_data(chat_id,item,data):
	with shelve.open(shelve_name) as shl:
		shl[str(chat_id)][str(item)] = str(data)

def get_user_string(chat_id):
	with shelve.open(shelve_name) as shl:
		user_string = shl[str(chat_id)]
	return user_string

def prepare_edit_user_string(chat_id,editing_item):
	with shelve.open(shelve_name) as shl:
		user_app_form = shl[str(chat_id)]
		user_app_form['editing_item'] = editing_item
		shl[str(chat_id)] = user_app_form

def edit_user_string(chat_id,data):
	with shelve.open(shelve_name) as shl:
		item  = shl[str(chat_id)]['editing_item']
		user_app_form = shl[str(chat_id)]
		if item in user_app_form.keys():
			user_app_form[item] = str(data)
			user_app_form['editing_item'] = None
			shl[str(chat_id)] = user_app_form

def get_editing_item(chat_id):
	with shelve.open(shelve_name) as shl:
		editing_item = shl[str(chat_id)]['editing_item']
		if editing_item == None:
			return False
		else:
			return str(editing_item)

def drop_editing_item(chat_id):
	with shelve.open(shelve_name) as shl:
		user_app_form = shl[str(chat_id)]
		user_app_form['editing_item'] = None
		shl[str(chat_id)] = user_app_form

def check_string_fulness(chat_id):
	with shelve.open(shelve_name) as shl:
		user_app_form = shl[str(chat_id)]
		if 'editing_item' in user_app_form:
			del user_app_form['editing_item']
		if None not in user_app_form.values():
			return True
		else:
			return False
    
def add_to_order(chat_id,data):
	with shelve.open(shelve_name) as shl:
		user_app_form = shl[str(chat_id)]
		user_app_form['order'].append(str(data))
		shl[str(chat_id)] = user_app_form

def remove_from_order(chat_id,data):
	with shelve.open(shelve_name) as shl:
		user_app_form = shl[str(chat_id)]
		if data in user_app_form['order']:
			user_app_form['order'].remove(str(data))
			shl[str(chat_id)] = user_app_form





def get_all():
	with shelve.open(shelve_name) as shl:
		all_data = list(shl.items())
	return all_data

def clear_all():
	with shelve.open(shelve_name) as shl:
		shl.clear()