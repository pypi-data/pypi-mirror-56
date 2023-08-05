import click


class TodoList:
	def __init__(self):
		self.title = None
		self.subtitle = None
		self.todos = []
		self.empty = True


class TodoItem:
	def __init__(self, text, completed=False):
		self.text = text
		self.completed = completed


def load(filename):
	with open(filename) as f:
		content = f.read()
	return content


def parse(file_content):
	lines = file_content.splitlines()
	todo_lists = []
	current_todo_list = TodoList()
	last_parsed = None
	for num, line in enumerate(lines):
		if line.startswith('# '):
			if last_parsed not in [None, 'empty']:
				raise Exception(f'Unexpected title line {num + 1} after {last_parsed} line {num}.')
			current_todo_list.title = line.replace('# ', '')
			current_todo_list.empty = False
			last_parsed = 'title'
		elif line.startswith('## '):
			if last_parsed not in ['title']:
				raise Exception(f'Unexpected subtitle line {num + 1} after {last_parsed} line {num}.')
			current_todo_list.subtitle = line.replace('## ', '')
			current_todo_list.empty = False
			last_parsed = 'subtitle'
		elif line.startswith('- [ ] '):
			if last_parsed in ['empty', None]:
				raise Exception(f'Unexpected task line{num + 1}  after {last_parsed} line {num}.')
			current_todo_list.todos.append(TodoItem(
				text=line.replace('- [ ] ', ''),
				completed=False
			))
			current_todo_list.empty = False
			last_parsed = 'task'
		elif line.startswith('- [x] '):
			if last_parsed in ['empty', None]:
				raise Exception(f'Unexpected task line {num + 1} after {last_parsed} line {num}.')
			current_todo_list.todos.append(TodoItem(
				text=line.replace('- [x] ', ''),
				completed=True
			))
			current_todo_list.empty = False
			last_parsed = 'task'
		elif line.strip() == '':
			if last_parsed not in ['task', None, 'empty']:
				raise Exception(f'Unexpected empty line {num + 1} after {last_parsed} line {num}.')
			if not current_todo_list.empty:
				todo_lists.append(current_todo_list)
				current_todo_list = TodoList()
			last_parsed = 'empty'
		else:
			raise Exception(f'Invalid syntax on line {num + 1}: {line}')
	if not current_todo_list.empty:
		todo_lists.append(current_todo_list)
		current_todo_list = TodoList()

	return todo_lists


def from_file(filepath):
	content = load(filepath)
	return parse(content)
