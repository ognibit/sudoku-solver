import sys
import numpy as np

def from_csv_to_numpy(csv_filename, numpy_filename):
	array_list = []
	with open(csv_filename, 'r') as csvfile:
		# skip header
		next(csvfile)
		 
		for line in csvfile:
			[quiz, solution] = line.split(',')
			# remove \n
			solution = solution[:-1]
			# to numpy			
			quiz_array = np.array(list(quiz), dtype=np.int32)
			solution_array = np.array(list(solution), dtype=np.int32)
			numpy_row = np.array([quiz_array, solution_array])
			array_list.append(numpy_row)
	
	numpy_content = np.array(array_list)
	np.save(numpy_filename, numpy_content)

if __name__ == '__main__':
	print("From CSV to binary numpy")
	from_csv_to_numpy(sys.argv[1], sys.argv[2])