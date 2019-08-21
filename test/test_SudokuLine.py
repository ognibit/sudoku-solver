import numpy as np
import pytest

from sudoku import SudokuLine, build_rows, build_columns

@pytest.fixture
def default_line():
	dimension = 3
	dim_pow = dimension ** 2
	board = np.zeros(dim_pow, dtype='int')
	symbols = np.arange(1, dim_pow + 1)
	return SudokuLine(board, symbols)

@pytest.fixture
def default_symbols():
	dimension = 3
	dim_pow = dimension ** 2
	symbols = np.arange(1, dim_pow + 1)
	return symbols

def check_symbols(symbols, expected, mask):
	return all(np.isin(expected, symbols[mask] ))

def test_line_init(default_line):
	row = default_line	
	assert all([a == b for a, b in zip(row.symbols, [1, 2, 3, 4, 5, 6, 7, 8, 9])])	
	assert row.board.shape == (9,)

def test_allowed_symbols(default_line, default_symbols):
	row = default_line
	board = row.board
	assert check_symbols(default_symbols, [1,2,3,4,5,6,7,8,9], row.calculate_allowed_symbols())
	row[1] = 1		
	assert check_symbols(default_symbols, [2,3,4,5,6,7,8,9], row.calculate_allowed_symbols())
	row[1] = 8
	assert check_symbols(default_symbols, [1,2,3,4,5,6,7,9], row.calculate_allowed_symbols())
	row[8] = 2
	assert check_symbols(default_symbols, [1,3,4,5,6,7,9], row.calculate_allowed_symbols())


def test_build_rows():
	dimension = 3
	dim_pow = dimension ** 2
	board = np.zeros((dim_pow, dim_pow), dtype='int')
	
	markers = np.arange(9)
	board[:,0] = markers

	symbols = np.arange(1, dim_pow + 1)
	rows = build_rows(board, symbols, dimension)
	
	assert len(rows) == 9
	assert isinstance(rows[0], SudokuLine)
	assert rows[0].board.shape == (9,)
	assert rows[0].board[0] == 0
	assert rows[5].board[0] == 5
	assert rows[8].board[0] == 8

def test_build_columns():
	dimension = 3
	dim_pow = dimension ** 2
	board = np.zeros((dim_pow, dim_pow), dtype='int')
	
	markers = np.arange(9)
	board[0,:] = markers

	symbols = np.arange(1, dim_pow + 1)
	cols = build_columns(board, symbols, dimension)
	
	assert len(cols) == 9
	assert isinstance(cols[0], SudokuLine)
	assert cols[0].board.shape == (9,)
	assert cols[0].board[0] == 0
	assert cols[5].board[0] == 5
	assert cols[8].board[0] == 8