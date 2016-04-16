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
	if message.text == "/start" or message.text == "Начать заново":
		user.progressLabel, user.progressKey = "start", -1
		user.save() 	
		return ("Вы начали игру заново", None)
	else:
		scenario.progress = (user.progressLabel, user.progressKey)
		if scenario.get_current().__class__.__name__ == "NodeMenu":
			menu_item_finded = False
			for line,label in scenario.get_current().menu:
				if (line == message.text):
					menu_item_finded = True
					scenario.goto(label,-1)
					break
			if (menu_item_finded):
				reply, menu = scenario.next()
				user.progressLabel, user.progressKey = scenario.progress
				user.save()
				if (menu):
					return (reply, ReplyKeyboardMarkup.create([[line] for line,label in menu]))
				else:
					return (reply, ReplyKeyboardHide.create())
			else:
				return ("???", ReplyKeyboardMarkup.create([[line] for line,label in scenario.get_current().menu]))
		else:
			return ("Чтобы начать заново введите /start", ReplyKeyboardHide.create())



bot = TelegramBot('203607471:AAGIXeoretNObpGdN8lh1ecOQWUa5xY12c8')
bot.update_bot_info().wait()
print (bot.username)
bot.on_error = lambda: print("error")

last_update_id = 0

try:
	while True:


		updates = bot.get_updates(last_update_id+1).wait()
		for update in updates:
			last_update_id = update.update_id
			
			reply, keyboard = get_message_reply(update.message)
			bot.send_message(update.message.sender.id, reply, reply_markup = keyboard)
			# print ("sended "+reply)

		users = User.getAll()
		for user in users:
			if (user.progressKey == -1):
				scenario.progress = (user.progressLabel, 0)
			else:
				scenario.progress = (user.progressLabel, user.progressKey)
			if scenario.get_current().__class__.__name__ != "NodeMenu" and scenario.get_current().__class__.__name__ != "NodeReturn":

				time.sleep(1)

				scenario.progress = (user.progressLabel, user.progressKey)
				reply, menu = scenario.next()
				user.progressLabel, user.progressKey = scenario.progress
				user.save()
				if (menu):
					bot.send_message(user.id, reply, reply_markup = ReplyKeyboardMarkup.create([[line] for line,label in menu]))
				else:
					bot.send_message(user.id, reply, reply_markup = ReplyKeyboardHide.create())
				# print ("sended "+reply)

			
except KeyboardInterrupt:
	User.db.close()
	exit()
