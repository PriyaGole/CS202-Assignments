// Sudoku_Solver

To run the code:
	1. Open terminal. Make sure you are currently in the code directory.
	2. Run python sudoku_solver.py
	3. Input the parameter k. (The sudoku with k*k rows, k*k columns and k x k sized boxes)
	4. Input the test file name without any extension. (Eg. "test1" and NOT "test1.csv" without the quotations.
		//Test files can be found in "Tests" folder
	5. The output sudoku will be saved in "Solutions" folder as "Solution_{test_file_name}.csv"and will also be displayed on the console.
		//Solutions can be found as a csv file in "Solutions" folder

INPUT FORMAT:
For test1:
	Type the parameter k: 2
	Type the file name without any extension or dot: test1

For test2:
	Type the parameter k: 2
	Type the file name without any extension or dot: test2

For test3:
	Type the parameter k: 3
	Type the file name without any extension or dot: test3

For test4:
	Type the parameter k: 3
	Type the file name without any extension or dot: test4

For test5:
	Type the parameter k: 4
	Type the file name without any extension or dot: test5

For test5:
	Type the parameter k: 5
	Type the file name without any extension or dot: test5
	

OUTPUT:
For test1:
	SATisfiable

For test2:
	unSATisfiable
	Reason: Same element occurs at the corresponding same cell in the pair

For test3:
	SATisfiable

For test4:
	unSATisfiable
	Reason: Same element occurs at the corresponding same cell in the pair

For test5:
	SATisfiable






// Sudoku_Generator

To run the code:
	1. Open terminal. Make sure you are currently in the code directory.
	2. Run python sudoku_generator.py
	3. Input the parameter k. (The sudoku with k*k rows, k*k columns and k x k sized boxes)
	4. The output sudoku will be saved in "Solutions" folder as "Solution_{k}.csv"and will also be displayed on the console.
		//Solutions can be found as a csv file in "Solutions" folder

INPUT FORMAT:
For k=2:
	Type the parameter k: 2

For k=3:
	Type the parameter k: 3

For k=4:
	Type the parameter k: 4
	