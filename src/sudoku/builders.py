import numpy as np
from .SudokuSquare import SudokuSquare
from .SudokuLine import SudokuLine

def build_squares(matrix, symbols, dimension=3):
	"""Split the matrix into a (dim x dim) list of SudokuSquare"""
	rows = []
	for row in range(dimension):
		cols = []
		row_index = row * dimension
		row_slice = slice(row_index, row_index + dimension)
		
		for col in range(dimension):
			col_index = col * dimension
			col_slice = slice(col_index, col_index + dimension)
			square = matrix[row_slice, col_slice]
			cols.append(SudokuSquare(square, symbols))

		rows.append(cols)

	return rows

def build_rows(matrix, symbols, dimension=3):

	rows = []
	for row in range(matrix.shape[0]):
		rows.append(SudokuLine(matrix[row], symbols))

	return rows

def build_columns(matrix, symbols, dimension=3):

	cols = []
	for col in range(matrix.shape[1]):
		cols.append(SudokuLine(matrix[:,col], symbols))

	return cols	
