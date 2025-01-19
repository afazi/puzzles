import math

N = 9  # 9x9 grid

# Bitmasks for each row/column/box
row = [0] * N
col = [0] * N
box = [0] * N
seted = False

# Utility function to find the box index of an element at position [i][j] in the grid
def getBox(i, j):
    return i // 3 * 3 + j // 3

# Utility function to check if a number is present in the corresponding row/column/box
def isSafe(i, j, number):
    return not (row[i] >> number) & 1 and not (col[j] >> number) & 1 and not (box[getBox(i, j)] >> number) & 1

# Utility function to set the initial values of a Sudoku board (map the values in the bitmasks)
def setInitialValues(grid):
    global row, col, box
    for i in range(N):
        for j in range(N):
            if grid[i][j] is not None:  # Only update the bitmask for non-'None' entries
                row[i] |= 1 << grid[i][j]
                col[j] |= 1 << grid[i][j]
                box[getBox(i, j)] |= 1 << grid[i][j]

# Function to calculate the GCD of a list of 9-digit numbers (rows of the Sudoku grid)
def calculate_gcd_of_rows(grid):
    rows = [int(''.join(map(str, grid[i]))) for i in range(N)]
    gcd = rows[0]
    for num in rows[1:]:
        gcd = math.gcd(gcd, num)
    return gcd

# Function to find the next empty cell ('None') in the grid
def find_next_cell(grid):
    for i in range(N):
        for j in range(N):
            if grid[i][j] is None:  # Find the first 'None'
                return i, j
    return None  # Return None if no empty cell is found

# Function to solve Sudoku with MRV heuristic and track the best solution based on GCD
def SolveSudoku(grid, solutions, max_gcd=0, best_solution=None, first_solution_gcd=None):
    global seted  # Correct: declare 'seted' as global before use
    if not seted:
        seted = True
        setInitialValues(grid)

    # Find the next cell to fill
    cell = find_next_cell(grid)
    
    if not cell:
        # If no empty cells are left, we have a solution
        current_gcd = calculate_gcd_of_rows(grid)
        if best_solution is None or current_gcd > max_gcd:
            max_gcd = current_gcd
            best_solution = [row[:] for row in grid]  # Save the current best solution
        return max_gcd, best_solution

    i, j = cell
    
    # Try all numbers from 0 to 9
    for nr in range(10):  
        if isSafe(i, j, nr):
            grid[i][j] = nr
            row[i] |= 1 << nr
            col[j] |= 1 << nr
            box[getBox(i, j)] |= 1 << nr

            # Check GCD of rows as you fill
            if i == 1 and j == N-1:  
                first_two_gcd = math.gcd(
                    int(''.join(map(str, grid[0]))),
                    int(''.join(map(str, grid[1])))
                )
                if first_solution_gcd is not None and first_two_gcd < first_solution_gcd:
                    row[i] &= ~(1 << nr)
                    col[j] &= ~(1 << nr)
                    box[getBox(i, j)] &= ~(1 << nr)
                    grid[i][j] = None
                    continue

            max_gcd, best_solution = SolveSudoku(grid, solutions, max_gcd, best_solution, first_solution_gcd)

            # Backtrack: remove nr from bitmasks and try another number
            row[i] &= ~(1 << nr)
            col[j] &= ~(1 << nr)
            box[getBox(i, j)] &= ~(1 << nr)

        # Reset the current cell if no valid number was found
        grid[i][j] = None

    return max_gcd, best_solution

# Utility function to print the solved grid
def printGrid(grid):
    for i in range(N):
        print(' '.join(map(str, grid[i])))

# Driver code
if __name__ == '__main__':
    grid = [
        [None, None, None, None, None, None, None, 2, None],
        [None, None, None, None, None, None, None, None, 5],
        [None, 2, None, None, None, None, None, None, None],
        [None, None, 0, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, 2, None, None, None, None, None],
        [None, None, None, None, 0, None, None, None, None],
        [None, None, None, None, None, 2, None, None, None],
        [None, None, None, None, None, None, 5, None, None]
    ]

    first_solution_gcd = None
    solutions = []
    max_gcd, first_solution = SolveSudoku(grid, solutions)

    if first_solution:
        first_solution_gcd = calculate_gcd_of_rows(first_solution)
        print(f"First solution found with GCD: {first_solution_gcd}")
        printGrid(first_solution)
    else:
        print("No solution exists")
        first_solution_gcd = 0

    solutions = []
    max_gcd, best_solution = SolveSudoku(grid, solutions, max_gcd=first_solution_gcd, best_solution=first_solution, first_solution_gcd=first_solution_gcd)

    if best_solution:
        print(f"Best solution with GCD: {max_gcd}")
        printGrid(best_solution)
    else:
        print("No better solution found")
