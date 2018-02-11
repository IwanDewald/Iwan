# -*- coding: utf-8 -*-
app_form_warning = 'Для продолжения работы заполните анкету'

app_form = {'name' : None, 'country' : None, 'city' : None, 'occupation' : None, 'birthdate' : None, 'favorite' : None, 'editing_item':None, 'order' : []}
app_form_ru = {'name' : 'Имя', 'country' : 'Страна', 'city' : 'Город', 'occupation' : 'Род занятий', 'birthdate' : 'Дата рождения', 'favorite' : 'Любимый кофе' }

empty_order="""
*============================*

*Ваш заказ пуст*

*============================*
"""

redact_name = 'Введите имя'
redact_country = 'Ведите название страны'
redact_city = 'Введите название города'
redact_occupation = 'Род деятельности'
redact_birthdate = "Введите дату Вашего рождения в формате дд.мм (e.g. 31.05)"
redact_favorite = 'Выберите свой любимый кофе'
back = 'Назад'
back_to_menu = 'Назад'

redact_profile = '\N{BUSTS IN SILHOUETTE}' + 'Редактировать профиль'
order = '\N{TEACUP WITHOUT HANDLE}' + 'Сделать предзаказ'

select_language = 'Выберите язык\nSelect your language '
language_selected = 'Язык устанвлен             \nВыберите один из пунктов меню'
ru ='\N{REGIONAL INDICATOR SYMBOL LETTER R}'+'\N{REGIONAL INDICATOR SYMBOL LETTER U}'+'Русский'
eng = '\N{REGIONAL INDICATOR SYMBOL LETTER G}'+'\N{REGIONAL INDICATOR SYMBOL LETTER B}'+'English'

coffee = '\N{TEACUP WITHOUT HANDLE}' + 'Кофе'
dessert = '\N{SHORTCAKE}' + 'Десерты'
sandwitch = '\N{HAMBURGER}' + 'Сэндвичи'



coffee_menu = """
*============================*
Все просто: 1 клик -> +1 пункт к заказу
*============================*
"""#'Латте 400мл./180р. 250мл./120р.\nМокко 400мл./150р. 250мл./100р.\nВанильный раф 400мл./150р.'
coffee_list =  [{'text':'Латте 400мл./180р.','call':'Latte_180','price':180}, {'text':'Латте 250мл./120р.','call':'Latte_120','price':120}, {'text':'Мокко  400мл./150р.','call':'Mocco_150','price':150}, {'text':'Мокко 250мл./100р.','call':'Mocco_100','price':100}, {'text':'Ванильный раф 400мл./150р.','call':'Ruff_150','price':150}]
coffee_calls = ['Latte_180','Latte_120','Mocco_150','Mocco_100','Ruff_150']
coffee_ru = {'Latte_180': 'Латте 400мл./180р.', 'Latte_120':'Латте 250мл./120р.','Mocco_150': 'Мокко  400мл./150р.','Mocco_100': 'Мокко 250мл./100р.','Ruff_150': 'Ванильный раф 400мл./150р.' }
minus = '\N{HEAVY MINUS SIGN}'
plus = '\N{HEAVY PLUS SIGN}'

checkout = '\N{HEAVY EXCLAMATION MARK SYMBOL}'+'Оформить заказ'+'\N{HEAVY EXCLAMATION MARK SYMBOL}'