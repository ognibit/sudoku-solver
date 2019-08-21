import numpy as np
from functools import reduce
import random
from .builders import build_squares, build_rows, build_columns

class ConsistencyError(Exception):
	pass

class DeadLockError(Exception):
	pass	

def from_string(input_str, dimension=3):
	"""Build a SudokuBoard from a 81 chars string"""
	symbols = np.arange(1, dimension**2 +1, dtype=np.int32)
	quiz = np.array(list(input_str), dtype=np.int32)
	quiz = quiz.reshape( (9,9) )
	sudoku_board = SudokuBoard(quiz, symbols, dimension)
	return sudoku_board

class SudokuBoard:

	# STATES
	START = 0
	APPLY_CONSTR = 1
	CHECK_COMPLETED = 2
	DONE = 3
	DEADLOCK = 4

	# __slots__ = ['symbols', 'dimension', 'board', 'squares', 'rows', 'columns','_state']
	def __init__(self, board, symbols, dimension):
		self._state = 'unresolved'
		self._previous_board = None
		self.symbols = symbols
		self.dimension = dimension
		dim_pow = dimension ** 2
		self.board = board

		self.squares = build_squares(self.board, self.symbols)
		self.rows = build_rows(self.board, self.symbols)
		self.columns = build_columns(self.board, self.symbols)

	def __getitem__(self, key):
		return self.board[key]	

	def __repr__(self):
		flat = self.board.flatten()
		# +2 is for the []
		dim = flat.shape[0] + 2		
		# [1:-1] to remove the []
		return np.array2string(flat, separator='', max_line_width=dim)[1:-1]

	def __str__(self):
		return np.array2string(self.board).replace('[',' ').replace(']','')

	def __eq__(self, other):
		if self.__class__ == other.__class__:
			return np.all( np.equal(self.board, self.board) )
		elif isinstance(other, str):
			return repr(self) == other
		else:
			return repr(self) == repr(other)

	def get_square(self, row, col):
		square_row = row // self.dimension
		square_col = col // self.dimension		
		return self.squares[square_row][square_col]

	def calculate_allowed_symbols(self, row, col):
		allowed_square = self.get_square(row, col).calculate_allowed_symbols() 
		allowed_row = self.rows[row].calculate_allowed_symbols()
		allowed_col = self.columns[col].calculate_allowed_symbols()
		allowed_symbols = allowed_square & allowed_row & allowed_col
		return self.symbols[allowed_symbols]

	def apply_constraints(self):
		at_least_one_found = False

		for row, col in np.argwhere(self.board == 0):				
			allowed_symbols = self.calculate_allowed_symbols(row, col)
			
			if allowed_symbols.shape[0] == 1:
				self.board[row, col] = allowed_symbols[0]
				self.get_square(row, col).update()
				self.rows[row].update()
				self.columns[col].update()	
				at_least_one_found = True	

		return at_least_one_found

	def other_square_indexes(self, index):
		"""Get the other column/row indexes of the square where the input index is in"""
		parts = index // self.dimension		
		start = parts*self.dimension
		end = start + self.dimension
		return  tuple(x for x in range(start, end) if x != index)

	def apply_deductions(self):
		applied = False

		for row, col in np.argwhere(self.board == 0):				
			allowed_symbols = self.calculate_allowed_symbols(row, col)
			allowed_symbols = set(allowed_symbols)
			# when this function is called, it's sure that len(allowed_symbols) > 1
			
			other_rows = self.other_square_indexes(row)
			other_rows_allowed = [self.calculate_allowed_symbols(r, col) for r in other_rows if self.board[r, col] == 0]

			other_cols = self.other_square_indexes(col)
			other_cols_allowed = [self.calculate_allowed_symbols(row, c) for c in other_cols if self.board[row, c] == 0]

			# if there's a symbol allowed only for this cell, it can be set
			deductions = allowed_symbols.difference(*other_rows_allowed, *other_cols_allowed)

			if len(deductions) == 1:
				self.board[row, col] = deductions.pop()
				self.get_square(row, col).update()
				self.rows[row].update()
				self.columns[col].update()	
				applied = True						

		return applied

	def resolve(self):
		exit_loop = False
		state = self.START

		while not exit_loop:
			if state == self.START:
				state = self.APPLY_CONSTR

			if state == self.APPLY_CONSTR:
				applied_constraints = self.apply_constraints()
				if not applied_constraints:
					state = self.CHECK_COMPLETED
				# else keep appling constraints

			if state == self.CHECK_COMPLETED:
				if np.any(self.board == 0):
					applied_dedutions = self.apply_deductions()
					if applied_dedutions:
						state = self.APPLY_CONSTR
					else:
						state = self.DEADLOCK
				else:
					state = self.DONE

			if state == self.DONE:
				exit_loop = True			

			if state == self.DEADLOCK:
				exit_loop = True
				raise DeadLockError(self)

		return self

	def __setitem__(self, key, value):
		index_row, index_col = key

		square = self.get_square(index_row, index_col)
		if value not in self.calculate_allowed_symbols(index_row, index_col):
			raise ConsistencyError

		self.board[key] = value
		square.update()
		self.rows[index_row].update()
		self.columns[index_col].update()			