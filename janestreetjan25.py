import sys
import time
import itertools

# Load a given grid
def loadGrid():
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
    return grid

# Utility function to print the solved grid
def printGrid(grid):
    # Clear the previous grid (if necessary)
    sys.stdout.write("\r" + " " * 100)  # Ensure previous content is cleared
    sys.stdout.write("\r")  # Move to the start of the line

    # Print the new grid
    for i in range(9):
        sys.stdout.write(" ".join(map(str, grid[i])) + "\n")

    sys.stdout.flush()  # Ensure the output is printed immediately

# Creates a dictionary of dictionaries given a grid {row_index: {col_index:value}}
def grid_to_dict(grid):
    location_dict = {}
    for row_idx, row in enumerate(grid):
        row_dict = {}  # Inner dictionary for this row
        for col_idx, value in enumerate(row):
            if value is not None:
                row_dict[col_idx] = value
        if row_dict:  # Only add row to location_dict if it has any non-None values
            location_dict[row_idx] = row_dict

    return location_dict

# Generate all numbers where digits are only used once
def generate_unique_numbers():
    digits_no_zero = '123456789'
    digits_with_zero = '0123456789'
    eight_digit = [int(''.join(p)) for p in itertools.permutations(digits_no_zero, 8)]
    nine_digit =  [int(''.join(p)) for p in itertools.permutations(digits_with_zero, 9)]
    return eight_digit + nine_digit

# Create a subset of the unique numbers, if you know certain required and forbidden digits
def unique_numbers_subsets(unique_numbers, location_dict, row_index):
    # Convert the location_dict to a list of required or forbidden digits and locations
    required_digits = []
    required_locations = []
    forbidden_digits = []
    forbidden_locations = []

    for row, row_value in location_dict.items():
        for col, col_value in row_value.items():
            if col_value is not None:
                if row == row_index:
                    required_digits.append(col_value)
                    required_locations.append(col)
                else:
                    forbidden_digits.append(col_value)
                    forbidden_locations.append(col)

    # Now generate the subset
    result_subset = []

    for num in unique_numbers:
        num_str = str(num)
        if len(num_str) == 8:
            num_str = '0' + num_str
        
        # Check for required digits
        valid = True
        for digit, location in zip(required_digits, required_locations):
            if num_str[location] != str(digit):
                valid = False
                break
        
        # Check if forbidden digits are not at specific locations
        for digit, location in zip(forbidden_digits, forbidden_locations):
            if num_str[location] == str(digit):
                valid = False
                break

        if valid:
            result_subset.append(num)
        
    return result_subset

# Generates a dictionary for unique numbers possible for each row, based on known digits
def generate_subsets_dict(grid, unique_numbers):
    results_dict = {}

    location_dict = grid_to_dict(grid)

    for i in range(len(grid)):
        subset = unique_numbers_subsets(unique_numbers, location_dict, i)
        results_dict[i] = subset

    return results_dict

def filter_by_gcd(numbers, gcd):
    return [num for num in numbers if num % gcd == 0]

# Approach the Sudoku solution with bitmasking and backtracking
# Bitmasks for each column/box. Row already has unique digits. 10 digits in total
col = [0] * 10
box = [0] * 10
initialized = False

# Utility function to find the box index of an element at position [i][j] in the grid
def getBox(i, j):
    return i // 3 * 3 + j // 3

# Utility function to check if a number is present in the corresponding column/box
def isSafeCell(i, j, number):
    return not (col[j] >> number) & 1 and not (box[getBox(i, j)] >> number) & 1

# Convert a number to a list of digits
def num_to_digits(num):
    num_str = str(num)
    if len(num_str) == 8:
        num_str = '0' + num_str  # Prepend a zero to make it 9 digits
    digits = [int(digit) for digit in num_str]  
    return digits  

# Utility function to check if an entire row of numbers is safe
def isSafeRow(grid, i, num):
    digits = num_to_digits(num)
    for j in range(9):
        number = digits[j]
        if grid[i][j] is None:
            if not isSafeCell(i, j, number):
                return False
    return True

# Utility function to set the initial bitmask values of the grid
def setInitialValues(grid):
    global col, box
    for i in range(9):  # Assuming a 9x9 grid
        for j in range(9):
            if grid[i][j] is not None:
                col[j] |= 1 << grid[i][j]
                box[getBox(i, j)] |= 1 << grid[i][j]

# Function to solve the grid with backtracking
def solveGrid(grid, unique_dict, i):
    # Set the initial values
    global initialized
    if not initialized:
        initialized = True
        setInitialValues(grid)
    
    # Set the row count and col_count 
    row_count = 9
    col_count = 9

    # If we have reached the end of the grid, return True
    if i == row_count:
        printGrid(grid)
        return True

    # If the current row is filled, move to the next row
    if all(cell is not None for cell in grid[i]):
        return solveGrid(grid, unique_dict, i + 1)

    # Track which columns and boxes are affected in this row
    changed_cells = []

    # Try each number from unique numbers
    for num in unique_dict[i]:
        if isSafeRow(grid, i, num):
            # Assign the num values to the grid row, and update the bitmasks
            digits = num_to_digits(num)
            for j in range(col_count):
                if grid[i][j] is None:  # Only update empty cells
                    grid[i][j] = digits[j]
                    col[j] |= 1 << digits[j]
                    box[getBox(i, j)] |= 1 << digits[j]
                    changed_cells.append((i, j, digits[j]))  # Track the changes for backtracking

            # Recursively attempt to solve the rest of the grid
            if solveGrid(grid, unique_dict, i + 1):
                return True

            # Backtrack: undo the changes made for the current row
            for cell in changed_cells:
                row, col_idx, num_val = cell
                grid[row][col_idx] = None  # Reset the cell
                col[col_idx] &= ~(1 << num_val)  # Undo bitmask update
                box[getBox(row, col_idx)] &= ~(1 << num_val)  # Undo box bitmask
    
    return False

# Function that solves the grid with incrementing the gcd
def solveGridWithGCD(grid, gcd, unique_numbers):
    # Filter the given unique numbers by the GCD
    gcd_unique_numbers = filter_by_gcd(unique_numbers, gcd)
    # Generate the unique dictionary given the known digits
    unique_dict = generate_subsets_dict(grid, gcd_unique_numbers)
    print(f'Trying GCD {gcd}') 
    if solveGrid(grid, unique_dict, 0):
        print(f'Current best GCD is {gcd}')
        return solveGridWithGCD(grid, gcd * 2 + 1, unique_numbers)
    else:
        return solveGridWithGCD(grid, gcd + 2, unique_numbers)

# Primary function to solve the puzzle
def main(gcd):
    start_time = time.time()
    print('Generating unique numbers')
    grid = loadGrid()
    unique_numbers = generate_unique_numbers()
    solveGridWithGCD(grid, gcd, unique_numbers)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to complete the function: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    main(33)
