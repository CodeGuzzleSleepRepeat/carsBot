import requestsimport requests
import time
#from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import json
import datetime
import asyncio
from threading import Thread
#from telegram import Bot
#from telegram.ext import Dispatcher, CommandHandler
#from telegram.ext.dispatcher import run_async




#TOKEN = '5127651114:AAGKbGTvpZlcZWEyhNPiJ-r4adPV0svrIV4'
URL = 'https://api.telegram.org/bot'
TOKEN = '5177823817:AAHM-d-I065pue_oLXvrsMNnVQTH0jJ9puw'

#photo_url = 'https://yandex.ru/images/search?text=car&from=tabbar&pos=0&img_url=https%3A%2F%2Ffunart.pro%2Fuploads%2Fposts%2F2021-04%2F1618365707_5-funart_pro-p-mashina-sportkar-mashini-krasivo-foto-6.jpg&rpt=simage'
#photo_url2 = 'https://yandex.ru/images/search?text=car&from=tabbar&pos=1&img_url=https%3A%2F%2Fget.wallhere.com%2Fphoto%2Fcar-vehicle-sports-car-Ferrari-coupe-performance-car-Ferrari-458-netcarshow-netcar-car-images-car-photo-2016-488-GTB-by-Novitec-Rosso-wheel-supercar-land-vehicle-automotive-design-automobile-make-luxury-vehicle-390461.jpg&rpt=simage'


#data = pd.DataFrame(index = range(20))
data = []

#admin = '349446478'

admin_name = [['fcknmaggot', '-1']]

managers = pd.DataFrame()
#managers[0] = ('@fcknmaggot', 'Салон: Царицыно', '349446478')
#managers[1] = ('@fcknmaggot', 'Менеджер', '349446478')

chats = []
chat_ids = []


flag = {}
flag_data = {}
flag_car = {}
flag_admin = {}
counter = {}
num_of_photos = {}
gl_clas = {}
cur_manager = {}

start_pos = 20

def parse_data(date):
	global data
	global start_pos
	url_poster = 'https://api.maxposter.ru/partners-api/vehicles/active'
	headers = {'Content-type' : 'application/json', 'Authorization' : 'Basic Y2hlc3RhdnRvQG1heHBvc3Rlci5ydTpuNWsxZzdxRA'}
	fields = json.dumps({"filters" : [{"fields": "acquisitionDate","type": "greaterOrEqual","value": date}], "offset": "0","orders": ["-acquisitionDate"]})
	res = requests.post(f'{url_poster}', headers=headers, data=fields)
	pool = json.loads(res.text)['data']['vehicles']
	i = len(data)
	for car in pool:
		if str(car).find('price') > -1:
			price = str(car['price'])
		else:
			price = "Не указана"
		if str(car).find('generation') > -1:
			gen = str(car['generation']['name'])
		else:
			gen = "Не указано"
		if str(car).find('mileage') > -1:
			miles = str(car['mileage'])
		else:
			miles = "Не указан"
		if str(car).find('car_condition') > -1:
			if car['car_condition'] == 'excelent':
				cond = 'Отличное'
			else:
				cond = 'Среднее'
		else:
			cond = "Не указано"
		if str(car).find('modification') > -1:
			mod = str(car['modification']['name'])
		else:
			mod = "Не указана"
		if str(car).find('engineVolume') > -1:
			vol = str(car['engineVolume'])
		else:
			vol = "Не указан"
		if str(car).find('engineType') > -1:
			if str(car['engineType']) == 'petrol':
				eng_type = 'бензин'
			elif str(car['engineType']) == 'diesel':
				eng_type = 'дизель'
			else:
				eng_type = 'электро'
		else:
			eng_type = "Не указан"
		if str(car).find('gearboxType') > -1:
			if str(car['gearboxType']) == 'automatic':
				gear = 'автомат'
			else:
				gear = 'механика'
		else:
			gear = "Не указана"
		if str(car).find('driveType') > -1:
			if str(car['driveType']) == 'rear':
				driveType = 'задний'
			elif str(car['driveType']) == 'full_4wd':
				driveType = 'полный'
			else:
				driveType = 'передний'
		else:
			driveType = "Не указан"
		if str(car).find('complectation') > -1:
			if str(car['complectation']) == 'None':
				compl = "Не указана"
			else:
				compl = str(car['complectation']['name'])
		else:
			compl = "Не указана"
		if str(car).find('bodyConfiguration') > -1:
			body = str(car['bodyConfiguration']['name'])
		else:
			body = "Не указана"
		if str(car).find('steeringWheel') > -1:
			if str(car['steeringWheel']) == 'left':
				wheel = 'левый'
			else:
				wheel = 'правый'
		else:
			wheel = "Не указан"
		if str(car).find('uin') > -1:
			uin = str(car['uin'])
		else:
			uin = "Не указан"
		if str(car).find('bodyColor') > -1:
			color = str(car['bodyColor'])
		else:
			color = "Не указан"
		#if car.find('bodyConfiguration') > -1:
		#	 = str(car['bodyConfiguration']['name'])
		#else:
		#	body = "Не указана"



		ddd = ['id: ' + str(i), 'Марка и модель: ' + car['brand']['name']  + ' ' + car['model']['name'], 'Салон: ' + car['address'], 'Год выпуска: ' + str(car['year']),
		'Поколение: ' + gen, 'Пробег: ', miles + ' км', 'Модификация: ' + mod,
		 'Объем двигателя: ' + vol, 'Тип двигателя: ' + eng_type, 'Коробка передач: ' + gear, 'Привод: ' + driveType, 'Комплектация: ' + compl, 
		 'Тип кузова: ' + body, 'Цвет: ' + color, 'Руль: ' + wheel, 'VIN или номер кузова: ' + uin, 'Цена: ' + price] 

		start_pos = len(ddd)

		j = 0
		
		for photo in car['photos']:
			pic = requests.get(photo['url']).content
			file = open('car' + str(i) + '_photo' + str(j) + '.jpg', "wb")
			file.write(pic)
			ddd.append('car' + str(i) + '_photo' + str(j) + '.jpg')
			j += 1
		print("Downloading photos: " + str(i) " done")
		i += 1
		data.append(ddd)
	


def get_managers():
	file = open('managers.txt', "r")
	res = file.read()
	i = 0
	arr = res.split('\n')
	for line in arr:
		if line == '':
			break
		pos1 = line.find(' ')
		pos2 = line.rfind(' ')
		managers[0] = (line[:pos1], line[pos1 + 1: pos2], line[pos2 + 1:])
		i += 1


def get_admins():
	file = open('admins.txt', "r")
	res = file.read()
	arr = res.split('\n')
	for line in arr:
		if line == '':
			break
		pos1 = line.find(' ')
		admin_name.append([line[:pos1], line[pos1 + 1:]])








def get_updates(offset=0):
    result = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    return result['result']

def editMessage(mes_id, chat_id, text):
	requests.get(f'{URL}{TOKEN}/editMessage?chat_id={chat_id}&message_id={mes_id}&text={text}')



def sendMedia1(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)
def sendMedia2(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia3(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia4(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia5(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia6(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-6"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb") 
	    , "random-name-6": open(data[int(text)][start_num + 5], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia7(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-6"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-7"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb") 
	    , "random-name-6": open(data[int(text)][start_num + 5], "rb") 
	    , "random-name-7": open(data[int(text)][start_num + 6], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia8(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-6"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-7"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-8"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb") 
	    , "random-name-6": open(data[int(text)][start_num + 5], "rb") 
	    , "random-name-7": open(data[int(text)][start_num + 6], "rb") 
	    , "random-name-8": open(data[int(text)][start_num + 7], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia9(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-6"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-7"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-8"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-9"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb") 
	    , "random-name-6": open(data[int(text)][start_num + 5], "rb") 
	    , "random-name-7": open(data[int(text)][start_num + 6], "rb") 
	    , "random-name-8": open(data[int(text)][start_num + 7], "rb") 
	    , "random-name-9": open(data[int(text)][start_num + 8], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)

def sendMedia10(chat_id, text, start_num):
	params = {
	    "chat_id": chat_id
	    , "media":
	    """[
	        {
	            "type": "photo"
	            , "media": "attach://random-name-1"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-2"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-3"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-4"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-5"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-6"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-7"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-8"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-9"},
	        {
	            "type": "photo"
	            , "media": "attach://random-name-10"}
	    ]"""
	}

	files = {
	    "random-name-1": open(data[int(text)][start_num], "rb") 
	    , "random-name-2": open(data[int(text)][start_num + 1], "rb") 
	    , "random-name-3": open(data[int(text)][start_num + 2], "rb") 
	    , "random-name-4": open(data[int(text)][start_num + 3], "rb") 
	    , "random-name-5": open(data[int(text)][start_num + 4], "rb") 
	    , "random-name-6": open(data[int(text)][start_num + 5], "rb") 
	    , "random-name-7": open(data[int(text)][start_num + 6], "rb") 
	    , "random-name-8": open(data[int(text)][start_num + 7], "rb") 
	    , "random-name-9": open(data[int(text)][start_num + 8], "rb") 
	    , "random-name-10": open(data[int(text)][start_num + 9], "rb")}	
	return requests.get(f'{URL}{TOKEN}/sendMediaGroup', params=params, files=files)


def sendMedia(chat_id, ind, start_num):
	length = len(data[int(ind)]) - start_num
	if length == 1:
		sendMedia1(chat_id, ind, start_num)
	elif length == 2:
		sendMedia2(chat_id, ind, start_num)
	elif length == 3:
		sendMedia3(chat_id, ind, start_num)
	elif length == 4:
		sendMedia4(chat_id, ind, start_num)
	elif length == 5:
		sendMedia5(chat_id, ind, start_num)
	elif length == 6:
		sendMedia6(chat_id, ind, start_num)
	elif length == 7:
		sendMedia7(chat_id, ind, start_num)
	elif length == 8:
		sendMedia8(chat_id, ind, start_num)
	elif length == 9:
		sendMedia9(chat_id, ind, start_num)
	elif length == 10:
		sendMedia10(chat_id, ind, start_num)
	else:
		sendMedia10(chat_id, ind, start_num)
		sendMedia(chat_id, ind, start_num + 10)




def editMessageCaption(mes_id, chat_id, text, cur, photo_num, salon):
	caption = '\n'.join(data[int(text)][1:17])
	price = ''
	l = len(data[int(text)][17])
	for i in range(l):
		price += data[int(text)][17][l - i - 1]
		if i % 3 == 2:
			price += ' '
	p = price.rfind(' ')
	price = price[:p] + price[p + 1:]
	caption += '\n' + ''.join(reversed(price))
	reply_markup = {'inline_keyboard': [[{'text' : 'Связаться с менеджером', 'callback_data' : 'manager' + str(text) + '_' + str(salon)}]]}
	sendMedia(chat_id, text, 18)

	requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&reply_markup={json.dumps(reply_markup)}&text={caption}')
	


def editReplyMarkup(chat_id, clas, text):
	reply_markup = { "keyboard": [['Все авто'], ["Эконом (до 1 млн)"], ["Комфорт (от 1 до 3 млн)"], ["Премиум (от 3 до 10 млн)"], ["Элит (больше 10 млн)"], ["Выставить свою машину"]], "resize_keyboard": True, "one_time_keyboard": False}
	data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
	requests.post(f'{URL}{TOKEN}/sendMessage', data=data)



def reply_keyboard(chat_id, text):
	reply_markup = { "keyboard": [['Все авто'], ["Эконом (до 1 млн)"], ["Комфорт (от 1 до 3 млн)"], ["Премиум (от 3 до 10 млн)"], ["Элит (больше 10 млн)"], ["Выставить свою машину"]], "resize_keyboard": True, "one_time_keyboard": False}
	data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
	requests.post(f'{URL}{TOKEN}/sendMessage', data=data)		


def reply_admin_keyboard(chat_id, text):
	reply_markup = { "keyboard": [["Добавить админа"], ["Назначить менеджера"], ["Удалить менеджера"]], "resize_keyboard": True, "one_time_keyboard": False}
	data = {'chat_id': chat_id, 'text' : text, 'reply_markup': json.dumps(reply_markup)}
	requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

def reply_manager_keyboard(chat_id, text):
	reply_markup = { "keyboard": [["Удалить авто"]], "resize_keyboard": True, "one_time_keyboard": False}
	data = {'chat_id': chat_id, 'text' : text, 'reply_markup': json.dumps(reply_markup)}
	requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

def send_photo_url(chat_id, img_url):
    requests.get(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_url}&caption=hi')

def send_photo_file(chat_id, img, caption):
	file = {'photo' : open(img, 'rb'), 'caption' : caption}
	requests.post(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}', data=file)

def send_message(chat_id, text):
	return json.loads(requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}').text)




def inline_keyboard(chat_id, ddd):
	for d in ddd:
		d += '\n'
	text = '\n'.join(ddd[1:5])
	l = len(ddd[17])
	price = ''
	for i in range(l):
		price += ddd[17][l - i - 1]
		if i % 3 == 2 and i != 0:
			price += ' '
	p = price.rfind(' ')
	price = price[:p] + price[p + 1:]
	text += '\n' + ''.join(reversed(price))
	file =  {'photo' : open(ddd[18], 'rb')}
	salon = ddd[2][7:]
	reply_markup = {'inline_keyboard': [[{'text': 'Подробнее', 'callback_data' : 'show' + ddd[0] + '_' + salon}, {'text' : 'Связаться с менеджером', 'callback_data' : 'manager' + ddd[0] + '_' + salon}]]}
	data = {'chat_id': chat_id, 'caption': text, 'reply_markup': json.dumps(reply_markup)}
	return requests.post(f'{URL}{TOKEN}/sendPhoto', files=file, data = data)


def add_admin(str):
	global admin_name
	file = open('admins.txt', "a+")
	if (str[0] != '@'):
		return 'Неверный ник'
	admin_name.append([str[1:], '-1'])
	file.write(str[1:])
	file.write(' ')
	file.write('-1')
	file.write('\n')
	return 'Админ успешно добавлен'

def add_manager(str):
	global managers
	file = open('managers.txt', "a+")
	pos = str.find(' ')
	name = str[:pos]
	salon = str[pos + 1:]
	if (name[0] != '@'):
		return 'Неверный ник'
	name = name[1:]

	length = len(data)
	length_managers = len(managers.columns)
	managers[length_managers] = [name, salon, '-1']

	if length > 0:
		file.write('\n')
	file.write(name)
	file.write(' ')
	file.write(salon)
	file.write(' ')
	file.write('-1')
	#file.write('\n')
	return 'Менеджер успешно добавлен'

def delete_manager(name):
	global managers
	length = len(managers.columns)
	f = False
	file = open('managers.txt', "w")
	for i in range(length - 1):
		if (managers[i][0] == name):
			managers = managers.drop(columns = i)
			f = True
	
	length = len(managers.columns)
	for i in range(length - 1):
		file.write(managers[i][0])
		file.write(' ')
		file.write(managers[i][1])
		file.write(' ')
		file.write(str(managers[i][2]))
		file.write('\n')
	if f:
		return 'Менеджер успешно удален'
	return 'Такого менеджера нет'




def shpw_one_clas(message, clas, num, count):

	global last_clas
	
	price1 = 0
	price2 = 0
	j = 0
	if (clas.find('Эконом') == 0):
		
		price1 = 1000000
		price2 = 0
	elif (clas.find('Комфорт') == 0):
		price1 = 3000000
		price2 = 1000000
	elif (clas.find('Премиум') == 0):
		price2 = 3000000
		price1 = 10000000
	elif (clas.find('Элит') == 0):
		price2 = 10000000
		price1 = 100000000
	elif (clas.find('Все авто') == 0):
		price2 = 0
		price1 = 100000000
	else:
		return False

	cc = 0
	length = len(data)
	for i in range(length):
		if int(data[i][17][6:]) < price1 and int(data[i][17][6:]) >= price2:
			if j >= count:
				inline_keyboard(message['message']['chat']['id'], data[i])
				cc += 1
			j += 1 
			if (j == num + count):
				break

	if count + 1 <= cc + count:
		editReplyMarkup(message['message']['chat']['id'], clas, 'Авто ' + str(count + 1) + '-' + str(cc + count)) 
	gl_clas[message['message']['chat']['id']] = clas
	if i == length - 1:
		send_message(message['message']['chat']['id'], 'Больше нет объявлений в этой категории')
	return True

def send_file(message):
	global num_of_photos
	man = ""
	length = len(managers.columns)
	for i in range(length - 1):
		if (managers[i][1].lower() == 'Менеджер'.lower()):
			man = managers[i][2]
			break
	else:
		send_message(message['message']['chat']['id'], 'Менеджер еще не пользуется ботом')
		return -1

	send_message(man, 'Сообщение от ' + message['message']['chat']['first_name'] + ' ' + str(message['message']['chat']['id'])[5:] + '. Чтобы написать пользователю - ответьте на его сообщение')
	#send_message(message['message']['chat']['id'], 'Фото доставлены')
	mes = message['message']['photo'][3]['file_id']
	return requests.get(f'{URL}{TOKEN}/sendPhoto?chat_id={man}&photo={mes}')



def check_message(message):
	if str(message).find('data') > -1:
		return 1



	global data
	global flag_data
	global flag
	global flag_car

	chat_id_cur = message['message']['chat']['id']
	
	if str(message).find('file') > -1 and flag_car[chat_id_cur] == 7:
		rrr = send_file(message).json()
		if rrr == -1:
			return 1
		chats.append([rrr['result']['message_id'], chat_id_cur])
		#send_message(message['message']['chat']['id'], '2. Введите марку автомобиля')
		return 1

	
	if str(message).find('reply_to_message') > -1:
		length = len(managers.columns)
		for j in range(length):
			if str(message['message']['chat']['id']) == str(managers[j][2]):
				for i in range (len(chats)):
					if message['message']['reply_to_message']['message_id'] == chats[i][0]:
						chats.append([send_message(chats[i][1], managers[j][1] + ': ' + message['message']['text'])['result']['message_id'], message['message']['chat']['id']])
						#reply_keyboard(message['message']['chat']['id'], 'Сообщение')
				return 1


	if str(message).find('file') > -1:
		return 1

	if flag_car[chat_id_cur] == 7:
		flag_car[chat_id_cur] = 0
	
	if message['message']['text'] == 'Выставить свою машину':
		leng = len(managers.columns)
		print(leng)
		print(managers)
		for i in range(leng - 1):
			if managers[i][1].lower() == 'Менеджер'.lower():
				cur_manager[chat_id_cur][0] = managers[i][2]
				cur_manager[chat_id_cur][1] = managers[i][1]
				send_message(message['message']['chat']['id'], '1. Введите ваш город')
				break
		else:
			cur_manager[chat_id_cur][0] = -1
			send_message(message['message']['chat']['id'], 'К сожалению, менеджер еще не пользуется ботом')
			return
		flag_car[chat_id_cur] = 1
		return
				
	
	

	for name in admin_name:
		username = ""
		if str(message['message']['chat']).find('username') > -1:
			username = str(message['message']['chat']['username'])
		if username == str(name[0]) and name[1] == -1:
			name[1] = message['message']['chat']['id']
		if username == str(name[0]) and message['message']['text'] == 'Назначить менеджера':
			send_message(name[1], "Введите ник менеджера и название салона (например, Мкад, 51-й километр) через пробел (для назначения менеджера по приему объявлений напишите просто Менеджер)")
			flag[chat_id_cur] = 1
			return 1
		if username == str(name[0]) and message['message']['text'] == 'Добавить админа':
			send_message(name[1], "Введите ник админа")
			flag_admin[chat_id_cur] = 1
			return 1
		if username == str(name[0]) and message['message']['text'] == 'Удалить менеджера':
			send_message(name[1], "Введите ник менеджера")
			flag[chat_id_cur] = -1
			return 1

	
	length = len(managers.columns)
	length_data = len(data)

	
	for i in range(length):
		#if message['message']['chat']['username'] == managers[i][0] and managers[i][2] == -1:
		#	managers[i][2] = message['message']['chat']['id']
		if int(message['message']['chat']['id']) == int(managers[i][2]) and message['message']['text'] == 'Удалить авто':
			send_message(managers[i][2], "Введите id авто")
			flag_data[chat_id_cur] = 1
			return 1
	
	for i in range(length - 1):
		if int(message['message']['chat']['id']) == int(managers[i][2]) and flag_data[chat_id_cur] == 1:
			for j in range(length_data):
				if data[j][0][4:] == message['message']['text']:
					data = data.pop(i)
					send_message(managers[i][2], "Авто успешно удалено")
					break
			else:
				send_message(managers[i][2], 'Авто с таким id не найдено')
			flag_data[chat_id_cur] = 0
			return 1

	
	
	for name in admin_name:
		username = ""
		if str(message['message']['chat']).find('username') > -1:
			username = str(message['message']['chat']['username'])
		if username == str(name[0]) and flag_admin[chat_id_cur] == 1:
			send_message(name[1], add_admin(message['message']['text']))
			flag_admin[chat_id_cur] = 0
			return 1
		if username == str(name[0]) and flag[chat_id_cur] == 1:
			send_message(name[1], add_manager(message['message']['text']))
			flag[chat_id_cur] = 0
			return 1

		if username == str(name[0]) and flag[chat_id_cur] == -1:
			send_message(name[1], delete_manager(message['message']['text']))
			flag[chat_id_cur] = 0
			return 1


	num = length_data																				#Число авто за раз
	global counter
	if shpw_one_clas(message, message['message']['text'], num, 0):
		counter[chat_id_cur] = 0
		return 1

	
	if message['message']['text'].find('Показать больше авто') > -1:
		clas = message['message']['text'][21:]
		counter[chat_id_cur] += num
		shpw_one_clas(message, clas, num, counter[chat_id_cur])
		return 1
	
	"""
	if flag_car[chat_id_cur] == 2:
		length = len(managers.columns)
		for i in range(length):
			if (managers[i][1].lower() == 'Менеджер'.lower()):
				man = managers[i][2]
				break
		else:
			send_message(message['message']['chat']['id'], 'Менеджер еще не пользуется ботом')
		return 1
		"""
	
	if flag_car[chat_id_cur] == 1:
		
		flag_car[chat_id_cur] = 2
		length = len(managers.columns)
		man_id = -1
		for i in range(length - 1):
			if (managers[i][1].lower() == 'Менеджер'.lower()):
				man_id = managers[i][2]
				break
		if int(man_id) == -1:
			send_message(message['message']['chat']['id'], 'К сожалению, менеджер еще не пользуется ботом')
			return 1
		#username = ""
		#if str(message['message']['chat']).find('username') > -1:
		#	username = str(message['message']['chat']['username'])
		#else:
		username = str(message['message']['chat']['first_name'])
		send_message(man_id, 'Новая машина от пользователя ' + username + ' id ' + str(message['message']['chat']['id'])[5:] + ': ' + ': город ' + message['message']['text'])
		send_message(message['message']['chat']['id'], '2. Введите марку автомобиля')
		return 1


	#if len(cur_manager[chat_id_cur]) > 0:
	#	if int(cur_manager[chat_id_cur][0]) > -1 and flag_car[chat_id_cur] == 2:
	#		chats.append([send_message(cur_manager[chat_id_cur][0], 'От ' + message['message']['chat']['first_name'] + ' id ' + str(message['message']['chat']['id'])[5:] + ': ' + message['message']['text'])['result']['message_id'], message['message']['chat']['id']])
			#	flag_car[chat_id_cur] = 0
	#		if cur_manager[chat_id_cur][1].lower() == 'Manager'.lower():
	#			reply_keyboard(message['message']['chat']['id'], 'Сообщение доставлено менеджеру')
	#			return 1
	#		editReplyMarkup(message['message']['chat']['id'], gl_clas[chat_id_cur], 'Сообщение доставлено менеджеру')
	#		return 1

	elif len(cur_manager[chat_id_cur]) > 0:
		if int(cur_manager[chat_id_cur][0]) > -1 and flag_car[chat_id_cur] == 0:
			chats.append([send_message(cur_manager[chat_id_cur][0], 'От ' + message['message']['chat']['first_name'] + ' id ' + str(message['message']['chat']['id'])[5:] + ': ' + message['message']['text'])['result']['message_id'], message['message']['chat']['id']])
			editReplyMarkup(message['message']['chat']['id'], gl_clas[chat_id_cur], 'Сообщение доставлено менеджеру')
			return 1
	
	if flag_car[chat_id_cur] == 2:
		length = len(managers.columns)
		for i in range(length - 1):
			if (managers[i][1].lower() == 'Менеджер'.lower()):
				man = managers[i][2]
				break
		else:
			send_message(message['message']['chat']['id'], 'Менеджер еще не пользуется ботом')
		#chats.append([send_message(man, 'Новая машина от пользователя: ' + message['message']['chat']['username'] + ': ' + message['message']['text'])['result']['message_id'], message['message']['chat']['id']])
		#username = ""
		#if str(message['message']['chat']).find('username') > -1:
		#	username = str(message['message']['chat']['username'])
		#else:
		username = str(message['message']['chat']['first_name'])
		send_message(man, 'Сообщение от ' + username + ' ' + str(message['message']['chat']['id'])[5:] + ': Марка: ' + message['message']['text'])
		send_message(message['message']['chat']['id'], '3. Отправьте модель')
		flag_car[chat_id_cur] = 3
		#send_message(message['message']['chat']['id'], 'Данные отправлены менеджеру, он скоро с вами свяжется')
		#reply_keyboard(message['message']['chat']['id'], 'Хотите посмотреть объявления?')
		return 1

	if flag_car[chat_id_cur] == 3:
		length = len(managers.columns)
		for i in range(length - 1):
			if (managers[i][1].lower() == 'Менеджер'.lower()):
				man = managers[i][2]
				break
		else:
			send_message(message['message']['chat']['id'], 'Менеджер еще не пользуется ботом')
		#chats.append([send_message(man, 'Новая машина от пользователя: ' + message['message']['chat']['username'] + ': ' + message['message']['text'])['result']['message_id'], message['message']['chat']['id']])
		#username = ""
		#if str(message['message']['chat']).find('username') > -1:
		#	username = str(message['message']['chat']['username'])
		#else:
		username = str(message['message']['chat']['first_name'])
		send_message(man, 'Сообщение от ' + username + ' ' + str(message['message']['chat']['id'])[5:] + ': Модель: ' + message['message']['text'])
		send_message(message['message']['chat']['id'], '4. Отправьте пробег')
		flag_car[chat_id_cur] = 4
		#reply_keyboard(message['message']['chat']['id'], 'Хотите посмотреть объявления?')
		return 1


	if flag_car[chat_id_cur] == 4:
		length = len(managers.columns)
		for i in range(length - 1):
			if (managers[i][1].lower() == 'Менеджер'.lower()):
				man = managers[i][2]
				break
		else:
			send_message(message['message']['chat']['id'], 'Менеджер еще не пользуется ботом')
		#chats.append([send_message(man, 'Новая машина от пользователя: ' + message['message']['chat']['username'] + ': ' + message['message']['text'])['result']['message_id'], message['message']['chat']['id']])
		#username = ""
		#if str(message['message']['chat']).find('username') > -1:
		#	username = str(message['message']['chat']['username'])
		#else:
		username = str(message['message']['chat']['first_name'])
		send_message(man, 'Сообщение от ' + username + ' ' + str(message['message']['chat']['id'])[5:] +  ': Пробег: '+ message['message']['text'])
		send_message(message['message']['chat']['id'], '5. Отправьте VIN')
		flag_car[chat_id_cur] = 5
		#send_message(message['message']['chat']['id'], 'Данные отправлены менеджеру, он скоро с вами свяжется')
		#reply_keyboard(message['message']['chat']['id'], 'Хотите посмотреть объявления?')
		return 1


	if flag_car[chat_id_cur] == 5:
		length = len(managers.columns)
		for i in range(length - 1):
			if (managers[i][1].lower() == 'Менеджер'.lower()):
				man = managers[i][2]
				break
		else:
			send_message(message['message']['chat']['id'], 'Менеджер еще не пользуется ботом')
		#chats.append([send_message(man, 'Новая машина от пользователя: ' + message['message']['chat']['username'] + ': ' + message['message']['text'])['result']['message_id'], message['message']['chat']['id']])
		#username = ""
		#if str(message['message']['chat']).find('username') > -1:
		#	username = str(message['message']['chat']['username'])
		#else:
		username = str(message['message']['chat']['first_name'])
		send_message(man, 'Сообщение от ' + username + ' ' + str(message['message']['chat']['id'])[5:] + ': VIN: ' + message['message']['text'])
		send_message(message['message']['chat']['id'], '6. Отправьте фото')
		flag_car[chat_id_cur] = 7
		#send_message(message['message']['chat']['id'], 'Данные отправлены менеджеру, он скоро с вами свяжется')
		#reply_keyboard(message['message']['chat']['id'], 'Хотите посмотреть объявления?')
		return 1

	

	#flag_car[chat_id_cur] = 0
	
	
	



def find_manager(message):
	length = len(managers.columns)
	for i in range(length - 1):
		message['callback_query']['data'][message['callback_query']['data'].find('_') + 1:].lower(), managers[i][1].lower()
		if message['callback_query']['data'][message['callback_query']['data'].find('_') + 1:].lower() == managers[i][1].lower():
			if int(managers[i][2]) > -1:
				return i
	return -1



def check_query(message):
	if str(message).find('query') == -1:
		return


	global cur_manager
	#if message['callback_query']['data'].find('show') > -1:
	#	editMessageCaption(message['callback_query']['message']['message_id'], message['callback_query']['from']['id'], message['callback_query']['data'][4], 'hide', 4, message['callback_query']['data'].split('_')[1])
	#	return

	chat_id_cur = message['callback_query']['message']['chat']['id']

	if message['callback_query']['data'].find('show') > -1:
		#print(message['callback_query']['data']['file'].text)
		pos = message['callback_query']['data'].find('_')
		for i in range(len(data)):
			if data[i][0] == 'id: ' + message['callback_query']['data'][8:pos]:
				res = i
		editMessageCaption(message['callback_query']['message']['message_id'], message['callback_query']['from']['id'], res, 'hide', 17, message['callback_query']['data'][pos + 1:])
		return

	#if message['callback_query']['data'].find('hide') > -1:
	#	editMessageCaptionHide(message['callback_query']['message']['message_id'], message['callback_query']['from']['id'], message['callback_query']['data'][4], 'show', message['callback_query']['data'].split('_')[1])
	#	return
	#if message['callback_query']['data'].find('next') > -1:
	#	editMessageCaption(message['callback_query']['message']['message_id'], message['callback_query']['from']['id'], message['callback_query']['data'][4], 'hide', message['callback_query']['data'].split('_')[2], message['callback_query']['data'].split('_')[1])
	#	return
	if message['callback_query']['data'].find('manager') > -1:
		man = find_manager(message)
		if not man == -1:
			if not cur_manager[chat_id_cur][0] == -1 and not cur_manager[chat_id_cur][0] == managers[man][2]:
				send_message(message['query']['chat']['id'], 'Вы начали диалог с менеджером салона ' + managers[man][2] + '. Чтобы продолжить переписку с менеджером из салона ' + cur_manager[1] + ' еще раз свяжитесь с ним')
				length_chats = len(chats)
				for i in range(length_chats):
					if chats[i][1] ==  message['query']['chat']['id']:
						chats.pop(i)
						break    						#if manager == client - change?
			cur_manager[chat_id_cur][0] = managers[man][2]
			cur_manager[chat_id_cur][1] = managers[man][1]
		else:
			cur_manager[chat_id_cur][0] = -1

		car_id = message['callback_query']['data'][7:message['callback_query']['data'].find('_')]
		#user = 'No_name'
		#if message['callback_query']['message']['chat'].find('username') > -1:
		#	user = message['callback_query']['message']['chat']['username']
		first_name = message['callback_query']['message']['chat']['first_name']
		#last_name = message['callback_query']['message']['chat']['last_name']
		chat_id = message['callback_query']['message']['chat']['id']
		if (not cur_manager[chat_id_cur][0] == -1):
			chats.append([send_message(cur_manager[chat_id_cur][0], 'Сообщение от ' + first_name + ' ' + str(chat_id)[5:] + ' по поводу машины ' + car_id)['result']['message_id'], chat_id])
			send_message(chat_id, 'Менеджер ответит вам в ближайшее время')
		else:
			send_message(chat_id, 'К сожалению, менеджер еще не пользуется ботом')
		return




def run():
	date = datetime.date.today()
	tt = datetime.datetime.now()
	fl = True
	#while fl:
	#	try:
	parse_data("2019-01-01")
	#		fl = False
	#	except:
	#		time.sleep(1)
	it = {}
	get_admins()
	print("Admins: ", admin_name)
	get_managers()
	print("Managers: ", managers)
	#bot = Bot(TOKEN)
	#dp = Dispatcher(bot, None, workers=4)
	#start_handler = CommandHandler('start', check_message)
	#dp.add_handler(start_handler)
	fl = True
	while fl:
		try:
			update_id = get_updates()[-1]['update_id']
			fl = False
		except:
			time.sleep(1)
	while True:
		#time.sleep(0.02)
		cur_time = datetime.datetime.now()
		cur_date = datetime.date.today()
		if int(cur_time.minute) >= int(tt.minute) + 15:
			try:
				thread3 = Thread(target = parse_data, args = [str(date.year) + '-' + str(date.month) + '-' + str(date.day)])
				thread3.start()
				#parse_data(date.year + '-' + date.month + '-' + date.day)
				date = cur_date
				tt = cur_time
			except:
				print("Unable to get today`s updates")
		try:
			messages = get_updates(update_id)
		except:
			time.sleep(1)
		for message in messages:
			if update_id != message['update_id']:
				if update_id < message['update_id']:
					update_id = message['update_id']

				for ch_id in chat_ids:
					if str(message).find('query') > -1:
						break
					if message['message']['chat']['id'] == ch_id:
						break
				else:	
					flag[message['message']['chat']['id']] = 0
					flag_data[message['message']['chat']['id']] = 0
					flag_car[message['message']['chat']['id']] = 0
					flag_admin[message['message']['chat']['id']] = 0
					counter[message['message']['chat']['id']] = 0
					num_of_photos[message['message']['chat']['id']] = 0
					cur_manager[message['message']['chat']['id']] = [-1, -1]
					gl_clas[message['message']['chat']['id']] = '' 
					chat_ids.append(message['message']['chat']['id'])
					it[message['message']['chat']['id']] = 0

				if str(message).find('query') == -1:
					if it[message['message']['chat']['id']] == 0:
						length = len(managers.columns)
						username = ""
						if str(message['message']['chat']).find('username') > -1:
								username = message['message']['chat']['username']
						for name in admin_name:						
							if str(username) == name[0]:	
								name[1] = message['message']['chat']['id']
								reply_admin_keyboard(message['message']['chat']['id'], 'Добро пожаловать!')
								for i in range(length - 1):
									if managers[i][0] == name[0]:
										managers[i][2] = message['message']['chat']['id']
								break
						else:
						#if True:
							for j in range(length):
								if str(username) == str(managers[j][0]):
									managers[j][2] = message['message']['chat']['id']
									reply_manager_keyboard(managers[j][2], 'Добро пожаловать!')
									break
							else:
								reply_keyboard(message['message']['chat']['id'], 'Добро пожаловать!')
						it[message['message']['chat']['id']] = 1

				
				#try:
				
				#check_message(message)
				
				#check_query(message)
				#except:
				#send_message(message['message']['chat']['id'], 'Произошел сбой, пожалуйста, отправьте свое сообщение повторно')
				
				mes1 = message
				mes2 = message
				try:
					thread1 = Thread(target=check_message, args=[mes1])
					thread2 = Thread(target=check_query, args=[mes2])
					thread1.start()
					thread2.start()
				except:
					send_message(message['message']['chat']['id'], 'Произошел сбой, пожалуйста, отправьте свое сообщение повторно')
				#thread1.join()
				#thread2.join()

#loop = asyncio.new_event_loop()
#loop.create_task(run())
#loop.run_until_complete()

run()

