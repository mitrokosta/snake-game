import source.useful as lib
from source.engine_except import EngineError


class Engine:
    """Game engine"""

    def __init__(self):
        self.running = False
        self.mode = ''
        self.mode_actions = {'menu': self.menu,
                             'new game': self.new_game,
                             'load game': self.load_game,
                             'options': self.options,
                             'exit game': self.exit}

    def launch(self):
        """Launches the engine"""

        self.running = True
        lib.message(4 * '\t' + 'Welcome to the game!', 1)
        self.mode = 'menu'

    def menu(self):
        return lib.menu()

    def new_game(self):
        score = lib.new_game()
        lib.message(4 * '\t' + 'Game over! Your score is {}.'.format(score), 5)
        return 'menu'

    def load_game(self):
        score = lib.load_game()
        lib.message(4 * '\t' + 'Game over! Your score is {}.'.format(score), 5)
        return 'menu'

    def options(self):
        lib.options()
        return 'menu'

    def exit(self):
        """Shuts down the engine"""
        self.running = False
        lib.exit_game()
        return ''

    def run(self):
        """Runs the game"""

        while self.running:
            if self.mode in self.mode_actions:
                self.mode = self.mode_actions[self.mode]()
            else:
                raise EngineError('wrong mode', self.mode)
