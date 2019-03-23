import os, curses
from time import sleep
import datetime
from random import random
import source.objects as obj

class EngineError(Exception):
	"""Custom Exception"""
	def __init__(self, message, errors = []):
		super().__init__(message)

def read_from_file(fname):
	"""Reads a file and returns its insides"""
	_file = open(fname, 'r')
	insides = _file.read()
	_file.close()
	return insides

def clear():
	"""Clears the console"""
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')

def poll(variants, msg=''):
	"""Asks a question until getting a valid answer"""
	clear()
	if msg != '':
		print(msg)
	print('\n'.join(variants))
	lowercase = lambda _str: _str.lower().split()
	lower = list(map(lowercase, variants))
	result = ''
	while True:
		_input = input('Your choice: ').lower().split()
		if _input in lower:
			result = ' '.join(_input)
			break
		else:
			print('Incorrect input. Please, make a correct choice.')
	return result

def message(msg, period):
	"""Prints a message"""
	clear()
	print(msg)
	sleep(period)

def init_options():
	"""Reads and returns the options"""
	cfg = read_from_file('resource/config.ini').strip().split('\n')
	opts = dict()
	for opt in cfg:
		_type, value = opt.split()
		opts[_type] = value
	return opts

def save_game(field, snake, food, score):
	"""Saves the game to a save file"""
	tupstr = lambda tup: ' '.join(map(str, tup[0])) + ' ' + str(tup[1])
	date = datetime.datetime.today()
	_file = open(date.strftime('save/%Y_%m_%d_%H_%M_%S'), 'w+')
	ls = list(map(str, (field, snake, len(food), '\n'.join(list(map(tupstr, food.items()))), str(score))))
	_file.write('\n'.join(ls))
	_file.close()

def load(screen, save):
	"""Loads a game from a save"""
	content = read_from_file('save/' + save).strip().split('\n')
	coords = content[0].split()
	field = obj.Field(screen, (int(coords[0]), int(coords[1])))
	speed = tuple(map(int, content[1].split()))
	length = int(content[2])
	body = []
	for i in range(3, 3 + length):
		piece = content[i].split()
		body.append((int(piece[0]), int(piece[1])))
	alive = bool(content[i + 1])
	snake = obj.Snake(screen, field, (0, 0), speed, alive)
	snake.queue = body
	foodcount = int(content[i + 2])
	food = dict()
	for j in range(i + 3, i + 3 + foodcount):
		fd = content[j].split()
		food[(int(fd[0]), int(fd[1]))] = int(fd[2])
	screen.refresh()
	score = obj.MutableInt(int(content[j + 1]))
	return (field, snake, food, score)

def controls_manager(symb, ctype, snake):
	"""Manages controls"""
	if ctype == 'wasd':
		if (symb == ord('w') or symb == ord('W')) and snake.speed != (1, 0):
			snake.speed = (-1, 0)
		elif (symb == ord('a') or symb == ord('A')) and snake.speed != (0, 1):
			snake.speed = (0, -1)
		elif (symb == ord('s') or symb == ord('S')) and snake.speed != (-1, 0):
			snake.speed = (1, 0)
		elif (symb == ord('d') or symb == ord('D')) and snake.speed != (0, -1):
			snake.speed = (0, 1)
	elif ctype == 'arrows':
		if symb == curses.KEY_UP and snake.speed != (1, 0):
			snake.speed = (-1, 0)
		elif symb == curses.KEY_LEFT and snake.speed != (0, 1):
			snake.speed = (0, -1)
		elif symb == curses.KEY_DOWN and snake.speed != (-1, 0):
			snake.speed = (1, 0)
		elif symb == curses.KEY_RIGHT and snake.speed != (0, -1):
			snake.speed = (0, 1)
	else:
		raise EngineError('wrong controls type')

def difficulty_manager(diff):
	"""Manages diffuculty"""
	if diff == 'trivial':
		return 1.0
	elif diff == 'easy':
		return 0.8
	elif diff == 'normal':
		return 0.6
	elif diff == 'hard':
		return 0.4
	elif diff == 'impossible':
		return 0.2
	else:
		raise EngineError('wrong difficulty')

def generate_food(screen, snake, field, food):
	"""Generates food for the snake"""
	_all = {(y, x) for x in range(0, field.width - 3) for y in range(0, field.height - 3)}
	possible = list(_all - set(food.keys()) - set(snake.queue))
	new = int(random() * (len(possible) + 1))
	screen.addch(possible[new][0] + 1, possible[new][1] + 1, '·')
	screen.refresh()
	food[possible[new]] = 1 + int(random() * 3)

def game(screen, new = True, save = ""):
	"""Plays the game"""
	screen.nodelay(True)
	curses.curs_set(0)
	opts = init_options()
	modifier = difficulty_manager(opts['difficulty'])
	if new:
		field = obj.Field(screen, (10, 20))
		snake = obj.Snake(screen, field, (3, 3))
		score = obj.MutableInt(1)
		food = dict()
		field.draw()
		snake.draw()
	else:
		field, snake, food, score = load(screen, save)
		field.draw()
		snake.draw()
		for fd in food:
			screen.addch(fd[0] + 1, fd[1] + 1, '·')
		screen.refresh()
	paused, running = False, True
	while snake.alive and running:
		symb = screen.getch()
		if symb == 27:
			running = False
			return score
		elif symb == ord('p') or symb == ord('P'):
			paused = [True, False][paused]
		elif symb == ord('c') or symb == ord('C'):
			save_game(field, snake, food, score)
		else:
			controls_manager(symb, opts['controls_types'], snake)	
		if not paused:
			snake.move(food, score)
			if random() < 0.1 and len(food.keys()) < 3:
				generate_food(screen, snake, field, food)
			curses.napms(int(1000 * modifier))
	return score

def new_game():
	"""Wrapper around the game"""
	return curses.wrapper(game, True)
	
def load_game():
	saves = os.listdir('save')
	save = poll(saves, 'Select the save you want to load:')
	return curses.wrapper(game, False, save)

def options():
	"""Allows to customize controls and other things"""
	clear()
	sources = read_from_file('resource/options.ini').strip().split('\n')
	fcfg = open('resource/config.ini', 'w+')
	for src in sources:
		_type, variants = src.split(': ', 1)
		variants = variants.split(', ')
		if _type == 'controls_types':
			ans = poll(variants, 'Choose your preferred type of controls:')
			fcfg.write(_type + ' ' + ans + '\n')
		if _type == 'difficulty':
			ans = poll(variants, 'Choose game diffuculty:')
			fcfg.write(_type + ' ' + ans + '\n')
	fcfg.close()
	
def exit_game():
	"""Exits"""
	print(4 * '\t' + 'Goodbye!')

def menu():
	"""Prints the menu and offers a choice"""
	clear()
	_menu = read_from_file('resource/menu.ini').strip().split('\n')
	menu_result = poll(_menu, 4 * '\t' + 'GAME MENU')
	return menu_result


