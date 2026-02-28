import nonoSolvFunc

# Getting the coordinates of the blue box around the puzzle
puzzle_coords = nonoSolvFunc.getPuzzleCoords()

# Get the columns digits from here
column_coords = nonoSolvFunc.getColumnImage(puzzle_coords)
column_digits = nonoSolvFunc.extractColumnNumbers()

# Read the digits from the columns
row_coords = nonoSolvFunc.getRowImage(puzzle_coords)
row_digits = nonoSolvFunc.extractRowNumbers()

# Make a two-dimensional array to store the game board
game_board = []
for id_i, i in enumerate(column_digits):
    game_board.append([])
    for j in row_digits:
        game_board[id_i].append(0)
        
print(game_board)