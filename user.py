

class User:	

	id = None
	progressLabel = 'start'
	progressKey = -1

	_is_new_record = False

	def __init__(self, id = None):
		if (id == None):
			return
		cursor = User.db.execute(''' 
			SELECT progressLabel, progressKey FROM users
			WHERE id = {0}
			LIMIT 1;
		'''.format(id))
		row = cursor.fetchone()
		if row == None:
			self._is_new_record = True
		else:
			self.progressLabel = row[0]
			self.progressKey = row[1]

		self.id = id
	
	def save(self):
		if (not self._is_new_record):
			User.db.execute(''' 
				UPDATE users
				SET progressLabel = '{1}',
				progressKey = {2}
				WHERE id = {0}
				LIMIT 1;
			'''.format(self.id, self.progressLabel, self.progressKey))
		else:
			User.db.execute('''
				INSERT INTO users
				(id, progressLabel, progressKey)
				VALUES ({0},'{1}',{2});
			'''.format(self.id, self.progressLabel, self.progressKey))
		User.db.commit()

	@staticmethod
	def getAll():
		models = []
		cursor = User.db.execute('''
			SELECT id, progressLabel, progressKey FROM users
			WHERE 1
		''')
		rows = cursor.fetchall()
		for row in rows:
			model = User()
			model.id = row[0]
			model.progressLabel = row[1]
			model.progressKey = row[2]
			models.append(model)

		return models
