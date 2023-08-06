import shaonutil
primary_seperator = ':'

def get_session_title(lines):
	# session title
	count = 0
	for line in lines:
		count += 1
		if line.count('\t') == 0:
			param,value = [line.strip() for c in line.split(primary_seperator,1)]
			if 'run' in param:
				return value,lines[count:]

def get_tasks_and_funcs(lines):
	tasks = {}
	functions = {}
	c = 0
	task = []
	function = []
	currentTaskName = ''
	currentFuncName = ''
	currentObj = '' #task/func
	LineNumber = 1
	while c < len(lines):
		line = lines[c]
		if line.count('\t') == 1:
			param,value = [kc.strip() for kc in line.split(primary_seperator,1)]
			if 'task' in param or 'func' in param:
				if c > 0:
					if currentObj == 'task':
						tasks[currentTaskName] = lines[1:c]
						lines = lines[c:]
						c = 0
						currentTaskName = value
					elif currentObj == 'func':
						functions[currentFuncName] = lines[1:c]
						lines = lines[c:]
						c = 0
						currentFuncName = value

				if 'task' in param:
					currentObj = 'task'
					currentTaskName = value
					tasks[currentTaskName] = []
				elif 'func' in param:
					currentObj = 'func'
					currentFuncName = value
					functions[currentFuncName] = []
		else:
			if line.count('\t') > 1:
				lines[c] = line.strip()
			else:
				raise ValueError("Syntax Error at Line ",LineNumber)
		c += 1
		LineNumber += 1
	
	if c == len(lines):
		if c > 0:
			if currentObj == 'task':
				tasks[currentTaskName] = lines[1:c]
				lines = lines[c:]
				c = 0
				currentTaskName = value
			elif currentObj == 'func':
				functions[currentFuncName] = lines[1:c]
				lines = lines[c:]
				c = 0
				currentFuncName = value

	return tasks,functions

def task_language_parser(filename):
	language_dic = {}

	lines = shaonutil.file.read_file(filename)

	# get session title
	title,lines = get_session_title(lines)
	language_dic[title] = {}
	
	# get tasks and functions
	tasks,functions = get_tasks_and_funcs(lines)



	shaonutil.strings.nicely_print(functions)
			

task_language_parser("github.tasks")
