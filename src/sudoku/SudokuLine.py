import numpy as np

class SudokuLine:
	"""Represents a row or a column of the matrix"""
	# __slots__ = ['symbols', 'board']
	
	def __init__(self, board, symbols):
		self.board = board
		self.symbols = symbols
		self.allowed = []
		self._up_to_date = False

	def __setitem__(self, key, value):
		self.board[key] = value
		self.update()

	def __getitem__(self, key):
		return self.board[key]

	def calculate_allowed_symbols(self):
		"""TODO"""
		if not self._up_to_date:
			self.allowed = np.isin(self.symbols, self.board, invert=True)	
			self._up_to_date = True
		
		return self.allowed	


	def update(self):
		self._up_to_date = False
