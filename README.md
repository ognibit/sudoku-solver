# sudoku-solver
Sudoku-solver it's a sandbox where I try to improve my Pythonic programming, using NumPy.

# Requirements
You need Python 3.6 and all the modules into `requirements.txt`.

# Samples
To run the script you need a CSV file like this:
```
quizzes,solutions
004300209005009001070060043006002087190007400050083000600000105003508690042910300,864371259325849761971265843436192587198657432257483916689734125713528694542916378
```
where `quizzes` is the *flatten* version of a 9x9 sudoku where 0s are the missing cells and `solutions` is the complete sodoku.

# Run
Nowadays not all the sudoku can be solved by the program, so you can find a CSV style output on standard error containing the wrong row.

```
python -m sudoku.benchmark /tmp/sudoku.csv 123 2> /tmp/sudoku_ko.csv
```

# Benchmarks
I used 1 milion sudoku found at [Kaggle](https://www.kaggle.com/bryanpark/sudoku) to benchmark the program.

The machine is and old Intel Core Duo, 4 GB of RAM, CentOS.

The best result is: 2:51:06 h, 124 errors.
