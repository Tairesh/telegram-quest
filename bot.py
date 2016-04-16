from twx.botapi import TelegramBot, ReplyKeyboardMarkup, Message
import sqlite3
from user import User
from scenario import Scenario

scenario = Scenario('script.rpy')

User.db = sqlite3.connect('space-quest.db')

def get_message_reply(message):	
	user = User(message.sender.id)
	if message.text == "/start":
		user.progressLabel, user.progressKey = "start", -1
		user.save() 	
		return ("Вы начали игру заново", None)
	else:
		scenario.progress = (user.progressLabel, user.progressKey)
		if scenario.get_current.__class__.__name__ == "NodeMenu":
			for line,label in scenario.get_current.menu:
				if (line == message.text):
					scenario.goto(label,-1)
					break
		reply, menu = scenario.next()
		user.progressLabel, user.progressKey = scenario.progress
		user.save()
		if (menu):
			return (reply, ReplyKeyboardMarkup.create([[line] for line,label in menu]))
		else:
			return (reply, None)



bot = TelegramBot('203607471:AAGIXeoretNObpGdN8lh1ecOQWUa5xY12c8')
bot.update_bot_info().wait()
print (bot.username)

last_update_id = 0;

try:
	while True:
		updates = bot.get_updates(last_update_id+1).wait()
		for update in updates:
#			print (update.message)
			last_update_id = update.update_id
			
			reply, keyboard = get_message_reply(update.message)
			bot.send_message(update.message.sender.id, reply, reply_markup = keyboard)

			
except KeyboardInterrupt:
	User.db.close()
	exit()
