import json

class User:	

	id = None
	progressLabel = 'start'
	progressKey = -1
	active = 0
	lastMessage = 0
	variables = {}

	_is_new_record = False

	def __init__(self, id = None):
		if (id == None):
			return
		cursor = User.db.execute(''' 
			SELECT 
				progressLabel,
				progressKey,
				active,
				lastMessage,
				variables
			FROM users
			WHERE id = {0}
			LIMIT 1;
		'''.format(id))
		row = cursor.fetchone()
		if row == None:
			self._is_new_record = True
		else:
			self.progressLabel = row[0]
			self.progressKey = row[1]
			self.active = row[2]
			self.lastMessage = row[3]
			self.variables = json.loads(row[4])

		self.id = id
	
	def save(self):
		if (not self._is_new_record):
			User.db.execute(''' 
				UPDATE users SET
					progressLabel = '{1}',
					progressKey = {2},
					active = {3},
					lastMessage = {4},
					variables = '{5}'
				WHERE id = {0}
				LIMIT 1;
			'''.format(self.id, self.progressLabel, self.progressKey, self.active, self.lastMessage, json.dumps(self.variables)))
		else:
			User.db.execute('''
				INSERT INTO users
				(id, progressLabel, progressKey, active, lastMessage, variables)
				VALUES ({0},'{1}',{2}, {3}, {4}, '{5}');
			'''.format(self.id, self.progressLabel, self.progressKey, self.active, self.lastMessage, json.dumps(self.variables)))
		User.db.commit()

	@staticmethod
	def getAll(only_active = False, max_last_message = 99999999999999):
		models = []
		query = '''
			SELECT 
				id,
				progressLabel,
				progressKey,
				active,
				lastMessage,
				variables
			FROM users
			WHERE 
		'''
		if (only_active):
			query += 'active <> 0'
		else:
			query += '1'
		query += ' AND lastMessage < {0}'.format(max_last_message)

		cursor = User.db.execute(query)
		rows = cursor.fetchall()
		for row in rows:
			model = User()
			model.id = row[0]
			model.progressLabel = row[1]
			model.progressKey = row[2]
			model.active = row[3]
			model.lastMessage = row[4]
			model.variables = json.loads(row[5])
			models.append(model)

		return models

	def load(self, scenario):
		self.progressLabel, self.progressKey = scenario.progress
		self.variables = scenario.variables