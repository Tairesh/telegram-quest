from twx.botapi import TelegramBot, ReplyKeyboardMarkup, ReplyKeyboardHide
from user import User
from scenario import Scenario
import time
import sys
import sqlite3

scenario_file = 'script.rpy'
if len(sys.argv) > 1:
	scenario_file = sys.argv[1]

scenario = Scenario(scenario_file)

User.db = sqlite3.connect('space-quest.db')

def get_message_reply(message):	
	user = User(message.sender.id)
	if message.text == "/start" or message.text == "🔄 Начать заново":
		user.progressLabel, user.progressKey, user.active, user.variables = "start", -1, 1, {}
		user.save() 	
		return ("Вы начали игру заново", ReplyKeyboardMarkup.create([['⏸ Приостановить игру']],resize_keyboard=True))
	elif message.text == "/pause" or message.text == "⏸ Приостановить игру":
		user.active = 0
		user.save()
		return ("Игра приостановлена", ReplyKeyboardMarkup.create([['🔄 Начать заново'],['▶️ Продолжить игру']],resize_keyboard=True))
	elif message.text == "/continue" or message.text == "▶️ Продолжить игру":
		user.active = 1
		user.save()
		return ("Игра возобновлена", ReplyKeyboardMarkup.create([['⏸ Приостановить игру']],resize_keyboard=True))
	else:
		scenario.load(user)
		if scenario.get_current().__class__.__name__ == "NodeMenu":
			menu_item_finded = False
			for line,label in scenario.get_current().menu:
				if (line == message.text):
					menu_item_finded = True
					scenario.goto(label,-1)
					break
			if (menu_item_finded):
				reply, menu = scenario.next()
				user.load(scenario)
				user.lastMessage = round(time.time())
				user.save()
				if (menu):
					return (reply, ReplyKeyboardMarkup.create([[line] for line,label in menu],resize_keyboard=True))
				else:
					return (reply, ReplyKeyboardMarkup.create([['⏸ Приостановить игру']],resize_keyboard=True))
			else:
				return ("???", ReplyKeyboardMarkup.create([[line] for line,label in scenario.get_current().menu] + [['🔄 Начать заново']],resize_keyboard=True))
		else:
			if (user.active):
				return ("Чтобы начать заново введите /start, чтобы приостановить игру введите /pause", ReplyKeyboardMarkup.create([['🔄 Начать заново'],['⏸ Приостановить игру']],resize_keyboard=True))
			else:
				return ("Чтобы начать заново введите /start, чтобы продолжить игру введите /continue", ReplyKeyboardMarkup.create([['🔄 Начать заново'],['▶️ Продолжить игру']],resize_keyboard=True))



bot = TelegramBot('203607471:AAGIXeoretNObpGdN8lh1ecOQWUa5xY12c8')
bot.update_bot_info().wait()
print (bot.username)

last_update_id = 0

try:
	while True:


		updates = bot.get_updates(last_update_id+1).wait()
		for update in updates:
			last_update_id = update.update_id
			
			reply, keyboard = get_message_reply(update.message)
			bot.send_message(update.message.sender.id, reply, reply_markup = keyboard, parse_mode = 'Markdown')
			# print ("sended "+reply)
			time.sleep(0.5)

		users = User.getAll(True, round(time.time())+1) #up to -5
		for user in users:
			if (user.progressKey == -1):
				scenario.progress = (user.progressLabel, 0)
			else:
				scenario.progress = (user.progressLabel, user.progressKey)
			if scenario.get_current().__class__.__name__ != "NodeMenu" and scenario.get_current().__class__.__name__ != "NodeReturn":

				scenario.load(user)
				reply, menu = scenario.next()
				user.load(scenario)
				user.lastMessage = round(time.time())
				user.save()
				if (menu):
					bot.send_message(user.id, reply, reply_markup = ReplyKeyboardMarkup.create([[line] for line,label in menu],resize_keyboard=True), parse_mode = 'Markdown')
				else:
					bot.send_message(user.id, reply, reply_markup = ReplyKeyboardMarkup.create([['⏸ Приостановить игру']],resize_keyboard=True), parse_mode = 'Markdown')

				time.sleep(0.5)
				# print ("sended "+reply)

			
except KeyboardInterrupt:
	User.db.close()
	exit()
