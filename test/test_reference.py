import numpy as np
import pytest

from sudoku import SudokuLine, build_rows, build_columns
from sudoku import SudokuSquare, build_squares

def test_reference():
	dimension = 3
	dim_pow = dimension ** 2
	board = np.zeros((dim_pow, dim_pow), dtype='int')
	symbols = np.arange(1, dim_pow + 1)
	squares = build_squares(board, symbols, dimension)
	rows = build_rows(board, symbols, dimension)
	cols = build_columns(board, symbols, dimension)

	assert squares[0][0].board[0,0] == 0
	assert rows[0].board[0] == 0
	assert cols[0].board[0] == 0

	board[0,0] = 1

	assert squares[0][0].board[0,0] == 1
	assert rows[0].board[0] == 1
	assert cols[0].board[0] == 1

	board[0][1] = 2

	assert squares[0][0].board[0,1] == 2
	assert rows[0].board[1] == 2
	assert cols[1].board[0] == 2

	board[1][0] = 3

	assert squares[0][0].board[1,0] == 3
	assert rows[1].board[0] == 3
	assert cols[0].board[1] == 3	

	board[4][3] = 4

	assert squares[1][1].board[1,0] == 4
	assert rows[4].board[3] == 4
	assert cols[3].board[4] == 4
