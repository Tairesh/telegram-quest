from twx.botapi import TelegramBot, ReplyKeyboardMarkup, Message
import sqlite3
from user import User
from scenario import Scenario

scenario = Scenario('script.rpy')

User.db = sqlite3.connect('space-quest.db')

def get_message_reply(message):
	if message.text == "/start":
		return "Привет!"
	else:
		user = User(message.sender.id)
		scenario.progress = (user.progressLabel, user.progressKey)
		message = scenario.next()
		if (message == None):
			message = "Вы прошли игру!"
		else:
			user.progressLabel, user.progressKey = scenario.progress
			user.save()
		return message



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
			
			reply = get_message_reply(update.message)
			bot.send_message(update.message.sender.id, reply)

			
except KeyboardInterrupt:
	User.db.close()
	exit()
