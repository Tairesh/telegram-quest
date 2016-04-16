

class Scenario:
	_file = None
	_labels = {}
	progress = ("start", -1)

	def __init__(self, file):
		self._file = open(file)
		
		current_label = None
		menu_jumps = 0;
		for line in self._file:
			line = line.strip().split("#")[0]
			
			if (not line or (line.split(" ")[0] in ("image", "show", "hide", "with", "define", "scene", "play"))):
				continue
			elif (line.startswith("label")):
				label = line.split(" ")[1].split(":")[0]
				self._labels[label] = []
				current_label = label
			else:
				if (menu_jumps > 0):
					menu_item = 2 - menu_jumps
					if line.startswith("jump"):
						self._labels[current_label][len(self._labels[current_label])-1].menu[menu_item] = (self._labels[current_label][len(self._labels[current_label])-1].menu[menu_item], line.split(" ")[1])
						menu_jumps -= 1
					else:
						self._labels[current_label][len(self._labels[current_label])-1].menu.append(line)
				else:
					if line.startswith("jump"):
						self._labels[current_label][len(self._labels[current_label])-1] = NodeJump(self._labels[current_label][len(self._labels[current_label])-1].text, line.split(" ")[1])
					elif line.startswith("return"):
						self._labels[current_label][len(self._labels[current_label])-1] = NodeReturn(self._labels[current_label][len(self._labels[current_label])-1].text)
					elif line.startswith("menu"):
						self._labels[current_label][len(self._labels[current_label])-1] = NodeMenu(self._labels[current_label][len(self._labels[current_label])-1].text, [])
						menu_jumps = 2
					else:
						self._labels[current_label].append(Node(line))

		# print (self._labels)

	def get_current(self):
		return self._labels[self.progress[0]][self.progress[1]]

	def goto(self, label, key = -1):
		self.progress = (label, key)

	def next(self):
		self.progress = (self.progress[0], self.progress[1]+1)
		
		node = self._labels[self.progress[0]][self.progress[1]]

		if (node.__class__.__name__ == "NodeJump"):
			self.progress = (node.link,-1)
			return self.next()
		elif (node.__class__.__name__ == "NodeReturn"):
			return (node.text, [("Начать заново", "start")])
		elif (node.__class__.__name__ == "NodeMenu"):
			return (node.text, node.menu)
		else:
			return (node.text, None)

class Node():
	def __init__(self, text):
		self.text = text
		

class NodeJump(Node):
	def __init__(self, text, link):
		super(NodeJump, self).__init__(text)
		self.link = link
		
class NodeMenu(Node):
	def __init__(self, text, menu):
		super(NodeMenu, self).__init__(text)
		self.menu = menu

class NodeReturn(Node):
	def __init__(self, text):
		super(NodeReturn, self).__init__(text)