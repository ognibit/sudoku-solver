import numpy as np

class SudokuSquare:
	"""Represents a DxD cell, where the symbols can occour just one time"""

	# __slots__ = ['dimension', 'symbols', 'board']

	def __init__(self, board, symbols):
		self.dimension = board.shape[0]
		self.symbols = symbols 
		self.board = board
		self.allowed = []
		self._up_to_date = False

	def calculate_allowed_symbols(self):
		"""TODO"""
		if not self._up_to_date:
			# get the symbols in use
			flat = self.board.flatten()
			# get the symbols not in use
			self.allowed = np.isin(self.symbols, flat, invert=True)	
			self._up_to_date = True

		return self.allowed

	def update(self):
		self._up_to_date = False