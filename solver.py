import nonoSolvFunc

# Getting the coordinates of the blue box around the puzzle
puzzle_coords = nonoSolvFunc.getPuzzleCoords()

# Get the columns digits from here
column_coords = nonoSolvFunc.getColumnImage(puzzle_coords)
column_digits = nonoSolvFunc.extractColumnNumbers()

# Read the digits from the columns
row_coords = nonoSolvFunc.getRowImage(puzzle_coords)
row_digits = nonoSolvFunc.extractRowNumbers()
print(column_digits)
print(row_digits)