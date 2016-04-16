import sqlite3

db = sqlite3.connect('space-quest.db')

db.execute(''' 
	CREATE TABLE users (
		`id` INT PRIMARY KEY NOT NULL,
		`progressLabel` STRING NOT NULL DEFAULT 'start',
		`progressKey` INT NOT NULL DEFAULT -1
	);
''')
db.commit()
db.close()
