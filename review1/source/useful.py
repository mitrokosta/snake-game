import os, curses
from time import sleep
from random import random
import source.objects as obj

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

def game(screen):
	"""Plays the game"""
	screen.nodelay(True)
	curses.curs_set(0)
	opts = init_options()
	modifier = difficulty_manager(opts['difficulty'])
	field = obj.Field(screen, screen.getmaxyx())
	field.draw()
	snake = obj.Snake(screen, field, (3, 3))
	snake.draw()
	paused, running = False, True
	score = obj.MutableInt(1)
	food = dict()
	while snake.alive and running:
		symb = screen.getch()
		if symb == 27:
			running = False
			return (snake, score)
		if symb == ord('p') or symb == ord('P'):
			paused = [True, False][paused]
		else:
			controls_manager(symb, opts['controls_types'], snake)	
		if not paused:
			snake.move(food, score)
			if random() < 0.5 and len(food.keys()) < 10:
				generate_food(screen, snake, field, food)
			curses.napms(int(1000*modifier))
	return (snake, score)

def new_game():
	"""Wrapper around the game"""
	return curses.wrapper(game)

def load_game():
	"""WIP"""
	pass
	
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


