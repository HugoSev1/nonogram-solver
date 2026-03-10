import nonoSolvFunc
import pygame

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

# Copy the board (Will be useful later)
previous_board = []
for id_i, i in enumerate(column_digits):
    previous_board.append([])
    for j in row_digits:
        previous_board[id_i].append(0)

# Make a similar array to store the working area
working_area_board = []
for id_i, i in enumerate(column_digits):
    working_area_board.append([])
    for j in row_digits:
        working_area_board[id_i].append(0)

# For the pygame display
columns_height = max(map(len, column_digits))
row_width = max(map(len, row_digits))

# How many rows there are
row_amount = 5
# Length of the whole board
board_width = 350
# Length of the tiles' side
tile_width = board_width/row_amount
# Shift from the top left corner
grid_shift = 20

# Setup for text displaying
pygame.font.init()
font = pygame.font.SysFont("Arial", int(tile_width))

# Display the board in a pygame window (for testing)
pygame.init
screen = pygame.display.set_mode((640, 640))
screen.fill((42, 43, 35))

# Display the column numbers
for i in range(len(column_digits)):
    pygame.draw.rect(screen, (148, 136, 224), pygame.Rect(
        grid_shift+(row_width*tile_width)+i*tile_width, grid_shift, tile_width, tile_width*columns_height))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(grid_shift+(row_width*tile_width)+i*tile_width,
                                                    grid_shift, tile_width, tile_width*columns_height), 3)
    for j in range(len(column_digits[i])):
        # Set the difference for alignment purposes
        empty_tiles = (columns_height-len(column_digits[i])) * tile_width

        # Display the numbers
        text_surface = font.render(str(column_digits[i][j]), False, (0, 0, 0))
        screen.blit(text_surface, (grid_shift+(row_width*tile_width) +
                    (i*tile_width) + tile_width/10, grid_shift+empty_tiles+(j*tile_width)))

# Display the row numbers
for i in range(len(row_digits)):
    pygame.draw.rect(screen, (148, 136, 224), pygame.Rect(
        grid_shift, grid_shift+(columns_height*tile_width)+i*tile_width, tile_width*row_width, tile_width))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(grid_shift, grid_shift+(
        columns_height*tile_width)+i*tile_width, tile_width*row_width, tile_width), 3)
    for j in range(len(row_digits[i])):
        # Set the difference for alignment purposes
        empty_tiles = (row_width-len(row_digits[i])) * tile_width

        # Display the numbers
        text_surface = font.render(str(row_digits[i][j]), False, (0, 0, 0))
        screen.blit(text_surface, (grid_shift+empty_tiles+(j*tile_width) +
                    tile_width/10, grid_shift+(columns_height*tile_width) + (i*tile_width)))


# Make a rectangle for the board
pygame.draw.rect(screen, (248, 236, 194), pygame.Rect(
    grid_shift+(tile_width*row_width), grid_shift+(tile_width*columns_height), board_width, board_width))

# FIRST PART: only has to be done once
# Do the lines that have only one possibility
for i in range(row_amount):
    current_line = nonoSolvFunc.doFullLine(row_amount, column_digits[i], [])
    nonoSolvFunc.fillColumn(current_line, game_board, i)
    current_line = nonoSolvFunc.doFullLine(row_amount, row_digits[i], [])
    nonoSolvFunc.fillRow(current_line, game_board, i)

# Do the remaining confirmed tiles (by the extremums)
for i in range(row_amount):
    line_index = i
    # Do columns
    for id_j, j in enumerate(column_digits[i]):
        number_index = id_j
        current_working_area = (nonoSolvFunc.limitLineArea(
            column_digits[line_index], number_index, row_amount))
        nonoSolvFunc.limitColumnArea(
            working_area_board, current_working_area, line_index)

        extremum_array = nonoSolvFunc.doExtremumConfirm(
            current_working_area, column_digits[line_index][number_index])
        nonoSolvFunc.fillColumn(extremum_array, game_board, line_index)

    # Do rows
    for id_j, j in enumerate(row_digits[i]):
        number_index = id_j
        current_working_area = (nonoSolvFunc.limitLineArea(
            row_digits[line_index], number_index, row_amount))
        nonoSolvFunc.limitRowArea(
            working_area_board, current_working_area, line_index)

        extremum_array = nonoSolvFunc.doExtremumConfirm(
            current_working_area, row_digits[line_index][number_index])
        nonoSolvFunc.fillRow(extremum_array, game_board, line_index)

# SECOND PART: Repeats until it does nothing
while previous_board != game_board:
    for id_i, i in enumerate(game_board):
        previous_board[id_i] = i.copy()
    # Complete lines with F's when all black squares on the line are found:
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.doCompleteLine(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.doCompleteLine(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Complete lines with T's if it's the only possibility with the current board configuration
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.doCompleteBlackSquares(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.doCompleteBlackSquares(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Complete what's possible when a line has only one number and F's (e.g. 3 on a row that is 00TF0 becomes 00TFF)
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.reduceSingularNumbers(
            column_digits[i], current_line)
        current_complete_array.reverse()
        current_complete_array = nonoSolvFunc.reduceSingularNumbers(
            column_digits[i], current_complete_array)
        current_complete_array.reverse()
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.reduceSingularNumbers(
            row_digits[i], current_line)
        current_complete_array.reverse()
        current_complete_array = nonoSolvFunc.reduceSingularNumbers(
            row_digits[i], current_complete_array)
        current_complete_array.reverse()
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Place tiles that can't fit elsewhere
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.tileCannotFit(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.tileCannotFit(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Check extremums that are done
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.extremumCompletion(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.extremumCompletion(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Fill the overlapping tiles
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillOverlapping(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillOverlapping(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Check the range when there's only one number
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.checkRange(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)
        
        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.checkRange(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)


# ------------------------
# Draw the tiles in Pygame
# ------------------------
for i in range(row_amount):
    for j in range(row_amount):
        if game_board[j][i] == "T":
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
                grid_shift + (tile_width*row_width) + i*tile_width + tile_width/10, grid_shift+(tile_width*columns_height) + j*tile_width + tile_width/10, tile_width - tile_width/5, tile_width - tile_width/5))
        elif game_board[j][i] == "F":
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
                grid_shift + (tile_width*row_width) + i*tile_width + tile_width/10, grid_shift+(tile_width*columns_height) + j*tile_width + tile_width/10, tile_width - tile_width/5, tile_width - tile_width/5))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
            grid_shift + (tile_width*row_width) + i*tile_width, grid_shift + (tile_width*columns_height) + j*tile_width, tile_width, tile_width), 3)

gameRunning = True
while gameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
    pygame.display.update()

pygame.quit()
