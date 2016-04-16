import sqlite3

db = sqlite3.connect('space-quest.db')

db.execute(''' 
	UPDATE users SET `progressLabel` = 'start', `progressKey` = -1 WHERE 1;
''')
db.commit()
db.close()
