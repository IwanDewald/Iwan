# -*- coding: utf-8 -*-
app_form_warning = u'Для продолжения работы заполните анкету'

app_form = {'name' : None, 'country' : None, 'city' : None, 'occupation' : None, 'birthdate' : None, 'favorite' : None, 'editing_item':None, 'order' : []}
app_form_ru = {'name' : u'Имя', 'country' : u'Страна', 'city' : u'Город', 'occupation' : u'Род занятий', 'birthdate' : u'Дата рождения', 'favorite' : u'Любимый кофе' }

empty_order=u"""
*============================*

*Ваш заказ пуст*

*============================*
"""

redact_name = u'Введите имя'
redact_country = u'Ведите название страны'
redact_city = u'Введите название города'
redact_occupation = u'Род деятельности'
redact_birthdate = u"Введите дату Вашего рождения в формате дд.мм (e.g. 31.05)"
redact_favorite = u'Выберите свой любимый кофе'
back = u'Назад'
back_to_menu = u'Назад'

redact_profile = '\N{BUSTS IN SILHOUETTE}' + u'Редактировать профиль'
order = '\N{TEACUP WITHOUT HANDLE}' + 'Сделать предзаказ'

select_language = u'Выберите язык\nSelect your language '
language_selected =u'Язык установлен             \nВыберите один из пунктов меню'
ru ='\N{REGIONAL INDICATOR SYMBOL LETTER R}'+'\N{REGIONAL INDICATOR SYMBOL LETTER U}'+'Русский'
eng = '\N{REGIONAL INDICATOR SYMBOL LETTER G}'+'\N{REGIONAL INDICATOR SYMBOL LETTER B}'+'English'

coffee = '\N{TEACUP WITHOUT HANDLE}' + 'Кофе'
dessert = '\N{SHORTCAKE}' + 'Десерты'
sandwitch = '\N{HAMBURGER}' + 'Сэндвичи'



coffee_menu = u"""
*============================*
Все просто: 1 клик -> +1 пункт к заказу
*============================*
"""
coffee_list =  [{'text':u'Латте 400мл./180р.','call':'Latte_180','price':180}, {'text':u'Латте 250мл./120р.','call':'Latte_120','price':120}, {'text':u'Мокко  400мл./150р.','call':'Mocco_150','price':150}, {'text':u'Мокко 250мл./100р.','call':'Mocco_100','price':100}, {'text':u'Ванильный раф 400мл./150р.','call':'Ruff_150','price':150}]
coffee_calls = ['Latte_180','Latte_120','Mocco_150','Mocco_100','Ruff_150']
coffee_ru = {'Latte_180': u'Латте 400мл./180р.', 'Latte_120':u'Латте 250мл./120р.','Mocco_150': u'Мокко  400мл./150р.','Mocco_100': u'Мокко 250мл./100р.','Ruff_150': u'Ванильный раф 400мл./150р.' }
minus = '\N{HEAVY MINUS SIGN}'
plus = '\N{HEAVY PLUS SIGN}'

checkout = '\N{HEAVY EXCLAMATION MARK SYMBOL}'+'Оформить заказ'+'\N{HEAVY EXCLAMATION MARK SYMBOL}'

to_bill = 'р. к чеку'
from_bill = 'р. из чека'

zakaz = 'Заказ оформлен!'
