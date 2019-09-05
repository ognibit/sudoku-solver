import numpy as np
from functools import reduce
from sudoku import SudokuBoard, from_string

SAMPLE_COL = 'quizzes'
SOLUTION_COL = 'solutions'

# DEPRECATED
def _resolve(row):
	resolver = from_string(row[SAMPLE_COL])
	try:
		resolver.resolve()
	except:
		return False, row
	else:
		return resolver == row[SOLUTION_COL], row

# DEPRECATED
def from_csv(csv_filename, total_rows=10_000):
	import csv
	from tqdm import tqdm

	chuck_tqdm = max(total_rows // 1000, 1)
	counter = 0
	error_rows = []
	with open(csv_filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		with tqdm(total=total_rows, mininterval=5) as pbar:
			for sudoku_line in reader:
				correct, row = _resolve(sudoku_line)
				counter += 1
				if not correct:
					error_rows.append(row)

				if counter % chuck_tqdm == 0:
					pbar.update(chuck_tqdm)

	return error_rows, counter

# DEPRECATED
def from_csv_parallel(csv_filename, total_rows=10_000):
	import csv
	from concurrent import futures
	from tqdm import tqdm

	chuck_tqdm = max(total_rows // 1000, 1)
	counter = 0
	error_rows = []
	with open(csv_filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		with futures.ProcessPoolExecutor() as executor:
			exec_map = executor.map(_resolve, reader)

			with tqdm(total=total_rows, mininterval=5) as pbar:
				for correct, row in exec_map:
					counter += 1
					if not correct:
						error_rows.append(row)

					if counter % chuck_tqdm == 0:
						pbar.update(chuck_tqdm)

	return error_rows, counter	

dimension = 3
symbols = np.arange(1, dimension**2 +1, dtype=np.int32)

def resolve_row(quiz, solution):	
	resolver = SudokuBoard(quiz.reshape( (9,9) ), symbols, dimension)
	try:
		resolver.resolve()
	except:
		return (False, (quiz, solution))
	else:		
		correct = np.all(resolver.board == solution.reshape( (9,9) ))
		return (correct, (quiz,solution))

def resolve_matrix(matrix):	
	return [resolve_row(x[0],x[1]) for x in matrix]

def numpy_to_quiz(array):
	return reduce(lambda a, b: str(a)+str(b), array, '')

def from_numpy(numpy_filename, total_rows=10_000):
	from concurrent import futures
	from multiprocessing import cpu_count
	import itertools as it

	matrix = np.load(numpy_filename)
	print("Loaded {} rows".format(matrix.shape[0]))

	splitted = np.array_split(matrix, cpu_count())

	with futures.ProcessPoolExecutor() as executor:
	 	exec_map = executor.map(resolve_matrix, splitted)

	# exec_map is [ [(bool, tuple) ], [(bool, tuple) ], ... ]
	# flat
	chain = it.chain.from_iterable(exec_map)

	# chian = [ (bool, tuple), (bool, tuple), ...]
	error_rows = it.filterfalse(lambda v: v[0], chain)

	# error_row[1] -> list of tuples (boolean removed)
	return [error_row[1] for error_row in error_rows], matrix.shape[0]			

if __name__ == '__main__':
	import sys
	import time
	from functools import partial

	start = time.time()

	# args: filename, number of rows
	if len(sys.argv) > 2:
		errors, rows = from_numpy(sys.argv[1], int(sys.argv[2]))
	else:
		errors, rows = from_numpy(sys.argv[1])

	end = time.time()
	elaps = end - start
	print(f"Finish in {elaps} sec.")
	print(len(errors), "fail in", rows, "samples")
	print("Error lines")
	# print CSV for errors on STDERR
	csv_print = partial(print, sep=',', file=sys.stderr)	
	csv_print('quizzes','solutions')
	for error in errors:
		csv_print(numpy_to_quiz(error[0]), numpy_to_quiz(error[1]))