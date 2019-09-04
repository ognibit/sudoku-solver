import numpy as np

class SudokuLine:
	"""Represents a row or a column of the matrix"""
	
	def __init__(self, board, symbols):
		self.board = board
		self.symbols = symbols
		self.allowed = []

	def __setitem__(self, key, value):
		self.board[key] = value

	def __getitem__(self, key):
		return self.board[key]

	def calculate_allowed_symbols(self):
		"""Checks which symbol is 'free' for this line
		Returns
		=========
		numpy.array of boolean. True is allowed
		"""
		self.allowed = np.isin(self.symbols, self.board, invert=True)	
		return self.allowed	
