

class Scenario:
	_file = None
	_labels = {}
	progress = ("start", -1)

	def __init__(self, file):
		self._file = open(file)
		
		current_label = None
		for line in self._file:
			line = line.strip().split("#")[0]
			
			if (not line or (line.split(" ")[0] in ("image", "show", "with", "define", "scene", "play"))):
				continue
			elif (line.startswith("label")):
				label = line.split(" ")[1].split(":")[0]
				self._labels[label] = []
				current_label = label
			else:
				self._labels[current_label].append(line)

		print (self._labels)

	def next(self):
		self.progress = (self.progress[0], self.progress[1]+1)
		
		node = self._labels[self.progress[0]][self.progress[1]]
		if (node.startswith("jump")):
			newlabel = node.split(" ")[1]
			self.progress = (newlabel,-1)
			return self.next()
		elif (node == "return"):
			return None
		else:
			return node
