import numpy as np
from sudoku import SudokuBoard, from_string

SAMPLE_COL = 'quizzes'
SOLUTION_COL = 'solutions'

def _resolve(row):
	resolver = from_string(row[SAMPLE_COL])
	try:
		resolver.resolve()
	except:
		return False, row
	else:
		return resolver == row[SOLUTION_COL], row

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


if __name__ == '__main__':
	import sys
	import time
	from functools import partial

	start = time.time()

	# args: filename, number of rows
	errors, rows = from_csv_parallel(sys.argv[1], int(sys.argv[2]))

	end = time.time()
	elaps = end - start
	print(f"Finish in {elaps} sec.")
	print(len(errors), "fail in", rows, "samples")
	print("Error lines")
	# print CSV for errors on STDERR
	csv_print = partial(print, sep=',', file=sys.stderr)
	csv_print(SAMPLE_COL,SOLUTION_COL)
	for error in errors:
		csv_print(error[SAMPLE_COL], error[SOLUTION_COL])