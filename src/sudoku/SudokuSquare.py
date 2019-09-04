import numpy as np

class SudokuSquare:
	"""Represents a DxD cell, where the symbols can occour just one time"""

	def __init__(self, board, symbols):
		self.dimension = board.shape[0]
		self.symbols = symbols 
		self.board = board
		self.allowed = []

	def calculate_allowed_symbols(self):
		"""Checks which symbol is 'free' for this square
		Returns
		=========
		numpy.array of boolean. True is allowed
		"""

		flat = self.board.flatten()
		# get the symbols not in use
		self.allowed = np.isin(self.symbols, flat, invert=True)	
		return self.allowed
