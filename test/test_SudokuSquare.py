import numpy as np
import pytest
from sudoku import SudokuSquare, build_squares

@pytest.fixture
def default_symbols():
	dimension = 3
	dim_pow = dimension ** 2
	symbols = np.arange(1, dim_pow + 1)
	return symbols

@pytest.fixture
def default_square():
	dimension = 3
	dim_pow = dimension ** 2
	board = np.zeros((dimension, dimension), dtype='int')
	symbols = np.arange(1, dim_pow + 1)
	return SudokuSquare(board, symbols)

def check_symbols(symbols, expected, mask):
	return all(np.isin(expected, symbols[mask] ))

def test_square_init(default_square):
	square = default_square	
	assert square.dimension == 3
	assert all([a == b for a, b in zip(square.symbols, [1, 2, 3, 4, 5, 6, 7, 8, 9])])	
	assert square.board.shape == (3, 3)


def test_square_allowed_symbols(default_square, default_symbols):
	square = default_square
	board = square.board
	assert check_symbols(default_symbols, [1, 2, 3, 4, 5, 6, 7, 8, 9], square.calculate_allowed_symbols())
	board[0, 1] = 1
	assert check_symbols(default_symbols, [2, 3, 4, 5, 6, 7, 8, 9], square.calculate_allowed_symbols())
	board[1, 1] = 2
	assert check_symbols(default_symbols, [3, 4, 5, 6, 7, 8, 9], square.calculate_allowed_symbols())

def test_square_allowed_symbols_9(default_symbols):
	board = np.array([
		[8, 6, 4],
		[3, 0, 5],
		[2, 7, 1]])
	square = SudokuSquare(board, default_symbols)

	assert check_symbols(default_symbols, [9], square.calculate_allowed_symbols())

def test_build_squares():
	dimension = 3
	dim_pow = dimension ** 2
	board = np.zeros((dim_pow, dim_pow), dtype='int')
	
	markers = np.arange(9).reshape((3,3))
	board[::3,::3] = markers

	symbols = np.arange(1, dim_pow + 1)
	squares = build_squares(board, symbols, dimension)
	
	assert len(squares) == 3
	assert len(squares[0]) == 3
	assert len(squares[1]) == 3
	assert len(squares[2]) == 3
	assert isinstance(squares[0][0], SudokuSquare)
	assert squares[0][0].board.shape == (3, 3)
	assert squares[0][0].board[0,0] == 0
	assert squares[1][1].board[0,0] == 4	
	assert squares[2][2].board[0,0] == 8