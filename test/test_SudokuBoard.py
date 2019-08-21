import numpy as np
import pytest

from sudoku import SudokuBoard, ConsistencyError, from_string

@pytest.fixture
def default_board():
	dimension = 3
	dim_pow = dimension ** 2
	board = np.zeros((dim_pow, dim_pow), dtype='int')
	symbols = np.arange(1, dim_pow + 1)
	return SudokuBoard(board, symbols, dimension)

def test_board_init(default_board):
	board = default_board	
	assert board.board.shape == (9,9)
	assert board.symbols.shape == (9,)
	assert len(board.squares) == 3
	assert len(board.rows) == 9
	assert len(board.columns) == 9

def test_board_getitem(default_board):
	assert default_board[4,5] == 0
	default_board.board[4,5] = 8
	assert default_board[4,5] == 8

def test_board_setitem(default_board):
	assert default_board.board[4,5] == 0
	default_board[4,5] = 8
	assert default_board.board[4,5] == 8

def test_board_symbolerror(default_board):
	with pytest.raises(ConsistencyError) as e:
		default_board[0,0] = 0
	
	with pytest.raises(ConsistencyError) as e:
		default_board[0,0] = -1

	with pytest.raises(ConsistencyError) as e:
		default_board[0,0] = 10

def test_board_consistency_square(default_board):
	with pytest.raises(ConsistencyError) as e:
		default_board[0, 0] = 1
		default_board[2, 2] = 1

def test_board_consistency_row(default_board):
	with pytest.raises(ConsistencyError) as e:
		default_board[0, 0] = 1
		default_board[0, 8] = 1

def test_board_consistency_col(default_board):
	with pytest.raises(ConsistencyError) as e:
		default_board[0, 0] = 1
		default_board[8, 0] = 1		

def test_board_equals(default_board):
	assert default_board == default_board
	assert default_board == repr(default_board)


def test_board_load_from_string():
	input = "004300209005009001070060043006002087190007400050083000600000105003508690042910300"
	board = from_string(input)	
	assert board[0, 2] == 4	
	assert board[7, 7] == 9
	assert board.symbols.shape[0] == 9

def test_board_str(default_board):
	default_board[0, 0] = 1
	default_board[8, 8] = 9
	print(default_board)
	output = """  1 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 9"""
	assert str(default_board) == output

def test_board_to_string(default_board):
	default_board[0, 0] = 1
	default_board[1, 1] = 2
	default_board[2, 2] = 3
	default_board[3, 3] = 4

	output = (""
	"100000000"
	"020000000"
	"003000000"
	"000400000"
	"000000000"
	"000000000"
	"000000000"
	"000000000"
	"000000000")
	
	assert default_board == output 


def test_other_square_indexes(default_board):
	assert default_board.other_square_indexes(0) == (1, 2)
	assert default_board.other_square_indexes(1) == (0, 2)
	assert default_board.other_square_indexes(2) == (0, 1)

	assert default_board.other_square_indexes(3) == (4, 5)
	assert default_board.other_square_indexes(4) == (3, 5)
	assert default_board.other_square_indexes(5) == (3, 4)


def test_board_resolve_0():
	board = from_string("004300209005009001070060043006002087190007400050083000600000105003508690042910300")
	board.resolve()
	assert board == "864371259325849761971265843436192587198657432257483916689734125713528694542916378"

# def test_board_real_15():
# 	board = from_string("490000000670052000080701000050210000004000300000046020000309010000520067000000032")
# 	print(board)
# 	board.resolve()
# 	assert board == "495638271671452893283791654856213749124975386937846125742369518318524967569187432"

def test_board_real_23():
	board = from_string("603000010520040036000000005400120000000506000000097003200000000390080041070000508")
	board.resolve()
	assert board == "683259714527841936941673825435128679719536482862497153258914367396785241174362598"
