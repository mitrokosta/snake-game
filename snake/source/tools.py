import os
from time import sleep


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


def make_folder(fname):
    """Creates a folder (unless present)"""

    if fname not in os.listdir():
        os.mkdir(fname)


def list_folder(fname):
    """Creates a folder (unless present) and lists its contents"""

    make_folder(fname)
    return os.listdir(fname)
