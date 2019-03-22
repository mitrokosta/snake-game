import source.useful as lib

class EngineError(Exception):
	"""Custom Exception"""
	def __init__(self, message, errors):
		super().__init__(message)

class Engine:
	"""Game engine"""
	def __init__(self):
		self.running = False
		self.mode = ''
	def launch(self):
		"""Launches the engine"""
		self.running = True
		lib.message(4 * '\t' + 'Welcome to the game!', 1)
		self.mode = 'menu'
	def exit(self):
		"""Shuts down the engine"""
		self.running = False
		self.mode = ''
		lib.exit_game()
	def run(self):
		"""Runs the game"""
		while self.running:
			if self.mode == 'menu':
				self.mode = lib.menu()
			elif self.mode == 'new game':
				score = lib.new_game()
				lib.message(4 * '\t' + 'Game over! Your score is {}.'.format(score[1]), 5)
				self.mode = 'menu'
			elif self.mode == 'load game':
				lib.load_game()
				self.mode = 'menu'
			elif self.mode == 'options':
				lib.options()
				self.mode = 'menu'
			elif self.mode == 'exit game':
				self.exit()
			else:
				raise EngineError('wrong mode', self.mode)
	
	

