

class Scenario:
	_file = None
	_labels = {}
	progress = ("start", -1)
	variables = {}

	def __init__(self, file):
		self._file = open(file)
		
		current_label = None
		menu_jumps = 0
		currentIf = False
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
						node = NodeJump("------", line.split(" ")[1])
						if (currentIf):
							self._labels[current_label][len(self._labels[current_label])-1].actions[len(self._labels[current_label][len(self._labels[current_label])-1].actions)-1] = (self._labels[current_label][len(self._labels[current_label])-1].actions[len(self._labels[current_label][len(self._labels[current_label])-1].actions)-1][0], node)
							currentIf = False
						else:
							self._labels[current_label].append(node)
					elif line.startswith("return"):
						node = NodeReturn("Игра окончена! По вопросам и пожеланиям вы можете связаться с разработчиком @Tairesh")
						if (currentIf):
							self._labels[current_label][len(self._labels[current_label])-1].actions[len(self._labels[current_label][len(self._labels[current_label])-1].actions)-1] = (self._labels[current_label][len(self._labels[current_label])-1].actions[len(self._labels[current_label][len(self._labels[current_label])-1].actions)-1][0], node)
							currentIf = False
						else:
							self._labels[current_label].append(node)
					elif line.startswith("menu"):
						self._labels[current_label][len(self._labels[current_label])-1] = NodeMenu(self._labels[current_label][len(self._labels[current_label])-1].text, [])
						menu_jumps = 2
					elif line.startswith("$"):
						code = line[2::]
						self._labels[current_label].append(NodeCode(code))
					elif (line.startswith("if")):
						statement = line[3:-1:]
						self._labels[current_label].append(NodeIf("------", [(statement, None)]))
						currentIf = True
					elif (line.startswith("elif")):
						statement = line[5:-1:]							
						self._labels[current_label][len(self._labels[current_label])-1].actions.append((statement,None))
						currentIf = True
					elif (line.startswith("else")):
						self._labels[current_label][len(self._labels[current_label])-1].actions.append(("else",None))
						currentIf = True
					else:
						node = Node(line.strip('"'))
						if (currentIf):
							self._labels[current_label][len(self._labels[current_label])-1].actions[len(self._labels[current_label][len(self._labels[current_label])-1].actions)-1] = (self._labels[current_label][len(self._labels[current_label])-1].actions[len(self._labels[current_label][len(self._labels[current_label])-1].actions)-1][0], node)
							currentIf = False
						else:
							self._labels[current_label].append(node)

		# print (self._labels)

	def get_current(self):
		return self._labels[self.progress[0]][self.progress[1]]

	def goto(self, label, key = -1):
		self.progress = (label, key)

	def next(self):
		self.progress = (self.progress[0], self.progress[1]+1)
		
		node = self._labels[self.progress[0]][self.progress[1]]
		node_type = node.__class__.__name__

		if (node_type == "NodeJump"):
			self.progress = (node.link,-1)
			return self.next()
		elif (node_type == "NodeCode"):
			variable, action, constant = (node.text.split(" "))

			constant = string_to_intbool(constant)

			if not (variable in self.variables):
				self.variables[variable] = 0

			if action == "=":							
				self.variables[variable] = constant
			elif action == "+=":
				self.variables[variable] = int(self.variables[variable]) + constant
			elif action == "-=":
				self.variables[variable] = int(self.variables[variable]) - constant
			return self.next()
		elif (node_type == "NodeIf"):

			for statement, ifnode in node.actions:
				statement_correct = False

				if statement == "else" or (statement in self.variables and self.variables[statement]):
					statement_correct = True
				elif ("<" in statement or ">" in statement or "=" in statement):
					leftval, operator, rightval = (statement.split(" "))

					if (leftval in self.variables):
						leftval = self.variables[leftval]
					else:
						leftval = string_to_intbool(leftval)
					if (rightval in self.variables):
						rightval = self.variables[rightval]
					else:
						rightval = string_to_intbool(rightval)

					if (operator == "=="):
						if (leftval == rightval):
							statement_correct = True
					elif (operator == "<"):
						if (leftval < rightval):
							statement_correct = True
					elif (operator == ">"):
						if (leftval > rightval):
							statement_correct = True
					elif (operator == "<="):
						if (leftval <= rightval):
							statement_correct = True
					elif (operator == ">="):
						if (leftval >= rightval):
							statement_correct = True
					elif (operator == "and"):
						if (leftval and rightval):
							statement_correct = True
					elif (operator == "or"):
						if (leftval or rightval):
							statement_correct = True

				if statement_correct:
					ifnode_type = ifnode.__class__.__name__

					if (ifnode_type == "NodeJump"):
						self.progress = (ifnode.link,-1)
						return self.next()
					else:
						return (ifnode.text, None)

			return self.next()

		elif (node_type == "NodeReturn"):
			return (node.text, [("🔄 Начать заново", "start")])
		elif (node_type == "NodeMenu"):
			return (node.text, node.menu)
		else:
			return (node.text, None)

	def load(self, user):
		self.progress = (user.progressLabel, user.progressKey)
		self.variables = user.variables

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

class NodeCode(Node):
	def __init__(self, text):
		super(NodeCode, self).__init__(text)

class NodeIf(Node):
	def __init__(self, text, actions):
		super(NodeIf, self).__init__(text)
		self.actions = actions

def string_to_intbool(constant):
	if (constant == "True"):
		return True
	elif (constant == "False"):
		return False
	else:
		return int(constant)