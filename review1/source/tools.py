import os
import curses
from time import sleep
import datetime
from random import random
import source.objects as obj
from source.engine_except import EngineError
from enum import Enum


def read_from_file(fname):
    """Reads a file and returns its insides"""

    with open(fname, 'r') as _file:
        insides = _file.read()
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

    def lowercase(_str):
        return _str.lower().split()

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


def check_saves_folder():
    """Creates a saves folder if not present"""

    if 'save' not in os.listdir():
        os.mkdir('save')


def save_game(field, snake, food, score):
    """Saves the game to a save file"""

    def tupstr(tup):
        return ' '.join(map(str, tup[0])) + ' ' + str(tup[1])

    date = datetime.datetime.today()
    with open(date.strftime('save/%Y_%m_%d_%H_%M_%S'), 'w+') as _file:
        ls = list(map(str, (field, snake, len(food),
                  '\n'.join(list(map(tupstr, food.items()))), str(score))))
        _file.write('\n'.join(ls))


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
    is_alive = bool(content[i + 1])
    snake = obj.Snake(screen, field, (0, 0), speed, is_alive)
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

    class Speed(Enum):
        UP = (-1, 0)
        DOWN = (1, 0)
        LEFT = (0, -1)
        RIGHT = (0, 1)

    returns = {Speed.UP: Speed.DOWN,
               Speed.DOWN: Speed.UP,
               Speed.LEFT: Speed.RIGHT,
               Speed.RIGHT: Speed.LEFT}

    wasd_controls = {ord('w'): Speed.UP, ord('W'): Speed.UP,
                     ord('a'): Speed.LEFT, ord('A'): Speed.LEFT,
                     ord('s'): Speed.DOWN, ord('S'): Speed.DOWN,
                     ord('d'): Speed.RIGHT, ord('D'): Speed.RIGHT}

    arrows_controls = {curses.KEY_UP: Speed.UP,
                       curses.KEY_LEFT: Speed.LEFT,
                       curses.KEY_DOWN: Speed.DOWN,
                       curses.KEY_RIGHT: Speed.RIGHT}

    controls_types = {'wasd': wasd_controls,
                      'arrows': arrows_controls}

    if ctype in controls_types:
        controls = controls_types[ctype]
    else:
        raise EngineError('wrong controls type', ctype)

    if symb in controls and snake.speed != returns[controls[symb]].value:
        snake.speed = controls[symb].value


def difficulty_manager(diff):
    """Manages diffuculty"""

    diff_types = {'trivial': 1.0,
                  'easy': 0.8,
                  'normal': 0.6,
                  'hard': 0.4,
                  'impossible': 0.2}

    if diff in diff_types:
        return diff_types[diff]
    else:
        raise EngineError('wrong difficulty', diff)


def generate_food(screen, snake, field, food):
    """Generates food for the snake"""

    _all = {(y, x) for x in range(0, field.width - 3)
            for y in range(0, field.height - 3)}
    possible = list(_all - set(food.keys()) - set(snake.queue))
    new = int(random() * (len(possible) + 1))
    screen.addch(possible[new][0] + 1, possible[new][1] + 1, '·')
    screen.refresh()
    food[possible[new]] = 1 + int(random() * 3)


def game(screen, new=True, save=""):
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
    while snake.is_alive and running:
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
    """Interface for loading a game"""

    check_saves_folder()
    saves = os.listdir('save')
    if len(saves) == 0:
        return curses.wrapper(game, True)
    save = poll(saves, 'Select the save you want to load:')
    return curses.wrapper(game, False, save)


def options():
    """Allows to customize controls and other things"""

    clear()
    sources = read_from_file('resource/options.ini').strip().split('\n')
    with open('resource/config.ini', 'w+') as fcfg:
        for src in sources:
            _type, variants = src.split(': ', 1)
            variants = variants.split(', ')
            if _type == 'controls_types':
                ans = poll(variants, 'Choose your preferred type of controls:')
                fcfg.write(_type + ' ' + ans + '\n')
            if _type == 'difficulty':
                ans = poll(variants, 'Choose game diffuculty:')
                fcfg.write(_type + ' ' + ans + '\n')


def exit_game():
    """Exits"""

    print(4 * '\t' + 'Goodbye!')


def menu():
    """Prints the menu and offers a choice"""

    clear()
    _menu = read_from_file('resource/menu.ini').strip().split('\n')
    menu_result = poll(_menu, 4 * '\t' + 'GAME MENU')
    return menu_result
