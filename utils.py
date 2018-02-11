from constants import app_form_ru, app_form, coffee_ru
import storage
import constants
def send_app_form(dic):
	for i in dic.keys():
		if dic[i] == None:
			dic[i]=' ...'
	app_form = ' Имя %s\nСтрана %s\nГород %s\nРод занятий %s\nДата рождения %s\nЛюбимый кофе %s'%(dic['name'],dic['country'],dic['city'],dic['occupation'],dic['birthdate'],dic['favorite'])
	return app_form

def send_order_list(chat_id):
	user_data = storage.get_user_string(chat_id)
	if not user_data['order']:
		return constants.empty_order
	output = dict()
	debt = 0
	order_list = '============================\nВаш заказ:\n'
	for i in user_data['order']:
		if i not in output.keys():
			output[i]=1
		else:
			output[i]+=1
	
	for i in output.items():
		order_list+=str(coffee_ru[i[0]]+' '+str(i[1])+'шт.\n')
		debt+=int(i[0][-3:])*i[1]
	order_list+=str('Итого: '+str(debt)+'р.\n')
	order_list+='============================\n'

		
	return order_list

