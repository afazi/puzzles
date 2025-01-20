import sys
import time
import itertools

# Generate all numbers with unique digits and function for filtering them by a gcd
def generate_unique_numbers():
    digits_no_zero = '123456789'
    digits_with_zero = '0123456789'
    eight_digit = [int(''.join(p)) for p in itertools.permutations(digits_no_zero, 8)]
    nine_digit =  [int(''.join(p)) for p in itertools.permutations(digits_with_zero, 9)]
    return eight_digit + nine_digit

def filter_by_gcd(numbers, gcd):
    return [num for num in numbers if num % gcd == 0]

# Approach the Sudoku solution with bitmasking and backtracking
# Bitmasks for each column/box. Row already has unique digits. 10 digits in total
col = [0] * 10
box = [0] * 10
seted = False

# Utility function to find the box index of an element at position [i][j] in the grid
def getBox(i, j):
    return i // 3 * 3 + j // 3

# Utility function to check if a number is present in the corresponding row/column/box
def isSafeCell(i, j, number):
    return not (col[j] >> number) & 1 and not (box[getBox(i, j)] >> number) & 1

# Utility function to check if an entire row of numbers is safe
def isSafeRow(i, num):
    num_str = str(num)
    if len(num_str) == 8:
        num_str = '0' + num_str  # Prepend a zero to make it 9 digits
    
    # Convert the string into a list of digits
    digits = [int(digit) for digit in num_str]  # Now `digits` will always have 9 elements
    
    # Check each column in the row for safety
    for j in range(9):  # Loop through each column in the row
        number = digits[j]  # Get the number at column j
        if not isSafeCell(i, j, number):
            return False
    return True

# Utility function to set the initial values of a Sudoku board (map the values in the bitmasks)
def setInitialValues(grid):
    global col, box
    for i in range(9):  # Assuming a 9x9 grid
        for j in range(9):
            if grid[i][j] is not None:
                col[j] |= 1 << grid[i][j]
                box[getBox(i, j)] |= 1 << grid[i][j]

# Function to solve Sudoku with backtracking
def SolveSudoku(grid, unique_numbers, i):
    global seted
    # Set the initial values
    if not seted:
        seted = True
        setInitialValues(grid)
    
    # If we have reached the end of the grid, return True
    row_count = len(grid)
    col_count = len(grid[0])
    if i == row_count:
        return True

    # If the current row is filled, move to the next row
    if all(cell is not None for cell in grid[i]):
        return SolveSudoku(grid, unique_numbers, i + 1)

    # Track which columns and boxes are affected in this row
    changed_cells = []

    # Try each number from unique numbers
    for num in unique_numbers:
        if isSafeRow(i, num):
            # Assign the num values to the grid row, and update the bitmasks
            num_str = str(num)
            if len(num_str) == 8:
                num_str = '0' + num_str  # Prepend a zero to make it 9 digits
            
            digits = [int(digit) for digit in num_str]

            # Update the grid and bitmasks for this row
            for j in range(col_count):
                if grid[i][j] is None:  # Only update empty cells
                    grid[i][j] = digits[j]
                    col[j] |= 1 << digits[j]
                    box[getBox(i, j)] |= 1 << digits[j]
                    changed_cells.append((i, j, digits[j]))  # Track this change

            # Recursively attempt to solve the rest of the grid
            if SolveSudoku(grid, unique_numbers, i + 1):
                return True

            # Backtrack: undo the changes made for the current row
            for cell in changed_cells:
                row, col_idx, num_val = cell
                grid[row][col_idx] = None  # Reset the cell
                col[col_idx] &= ~(1 << num_val)  # Undo bitmask update
                box[getBox(row, col_idx)] &= ~(1 << num_val)  # Undo box bitmask

    return False

# Utility function to print the solved grid
def printGrid(grid):
    for i in range(9):
        print(' '.join(map(str, grid[i])))


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

    start_time = time.time()
    unique_numbers = filter_by_gcd(generate_unique_numbers(),3)
    if SolveSudoku(grid, unique_numbers, 0):
        print("Sudoku solved!")
        printGrid(grid)
    else:
        print("No solution exists.")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to complete the function: {elapsed_time:.2f} seconds")
