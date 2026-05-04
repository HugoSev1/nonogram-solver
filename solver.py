import nonoSolvFunc
import pygame
import os
import copy

# Only proceed with Pygame if this is set to True (just change the value here if you want to toggle)
is_pygame_used = True

# Do a double-check on the lines in case the character detection goes wrong
double_check_line = True

# Use the files in the save_files folder to load a game if True
use_save_file = True

# Character to put to end the board when double-checking
end_char = '/'

# Width of the board in Python (mutable)
pygame_width = [790]

# Color  of the lines when highlighting a tile in Pygame
highlight_color = (198, 186, 255)

# Highligted tile
highlighted_tile = []


# Place the lines in Pygame
def setPygame():
    screen.fill((42, 43, 35))

    # Update width
    board_width = pygame_width[0]
    tile_width = board_width/row_amount
    font = pygame.font.SysFont("Arial", int(tile_width * 2 / 3))

    # Display the column numbers
    for i in range(len(column_digits)):
        pygame.draw.rect(screen, (148, 136, 224), pygame.Rect(
            grid_shift+(row_width*tile_width)+i*tile_width, grid_shift, tile_width, tile_width*columns_height))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(grid_shift+(row_width*tile_width)+i*tile_width,
                                                        grid_shift, tile_width, tile_width*columns_height), 3)

        # Highlight if prompted
        if len(highlighted_tile) == 2:
            if highlighted_tile[0] == i:
                pygame.draw.rect(screen, highlight_color, pygame.Rect(
                    grid_shift+(row_width*tile_width)+i*tile_width, grid_shift, tile_width, tile_width*columns_height))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(grid_shift+(row_width*tile_width)+i*tile_width,
                                                            grid_shift, tile_width, tile_width*columns_height), 3)

        for j in range(len(column_digits[i])):
            # Set the difference for alignment purposes
            empty_tiles = (
                columns_height-len(column_digits[i])) * tile_width

            # Display the numbers
            text_surface = font.render(
                str(column_digits[i][j]), False, (0, 0, 0))
            screen.blit(text_surface, (grid_shift+(row_width*tile_width) +
                        (i*tile_width) + tile_width/10, grid_shift+empty_tiles+(j*tile_width)))

    # Display the row numbers
    for i in range(len(row_digits)):
        pygame.draw.rect(screen, (148, 136, 224), pygame.Rect(
            grid_shift, grid_shift+(columns_height*tile_width)+i*tile_width, tile_width*row_width, tile_width))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(grid_shift, grid_shift+(
            columns_height*tile_width)+i*tile_width, tile_width*row_width, tile_width), 3)

        # Highlight if prompted
        if len(highlighted_tile) == 2:
            if highlighted_tile[1] == i:
                pygame.draw.rect(screen, highlight_color, pygame.Rect(
                    grid_shift, grid_shift+(columns_height*tile_width)+i*tile_width, tile_width*row_width, tile_width))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(grid_shift, grid_shift+(
                    columns_height*tile_width)+i*tile_width, tile_width*row_width, tile_width), 3)

        for j in range(len(row_digits[i])):
            # Set the difference for alignment purposes
            empty_tiles = (row_width-len(row_digits[i])) * tile_width

            # Display the numbers
            text_surface = font.render(
                str(row_digits[i][j]), False, (0, 0, 0))
            screen.blit(text_surface, (grid_shift+empty_tiles+(j*tile_width) +
                        tile_width/10, grid_shift+(columns_height*tile_width) + (i*tile_width)))

    # Make a rectangle for the board
    pygame.draw.rect(screen, (248, 236, 194), pygame.Rect(
        grid_shift+(tile_width*row_width), grid_shift+(tile_width*columns_height), board_width, board_width * (col_amount / row_amount)))


# Initializing the game (get values, etc.)
try:
    # Getting the coordinates of the blue box around the puzzle
    puzzle_coords = nonoSolvFunc.getPuzzleCoords()

    # Get the columns digits from here
    column_coords = nonoSolvFunc.getColumnImage(puzzle_coords)
    row_amount = nonoSolvFunc.findRowAmount(column_coords)

    # How many rows there are
    save_folder = os.listdir("save_files")

    # Check the save folder if we want to use it
    if use_save_file:
        if "column-digits.txt" not in save_folder:
            column_digits = nonoSolvFunc.extractColumnNumbers(row_amount)
            with open('save_files/column-digits.txt', 'w+') as f:
                for line in column_digits:
                    for number in line:
                        f.write(f"{number} ")
                    f.write('\n')
        else:
            column_digits = []
            coldigit_file = open('save_files/column-digits.txt', 'r')
            for line in coldigit_file.readlines():
                column_digits.append((line.split(' ')))
            for i in column_digits:
                for id_j, j in enumerate(i):
                    try:
                        i[id_j] = int(j)
                    except:
                        i.remove(i[id_j])

    else:
        column_digits = nonoSolvFunc.extractColumnNumbers(row_amount)

    # Read the digits from the rows
    row_coords = nonoSolvFunc.getRowImage(puzzle_coords)
    col_amount = nonoSolvFunc.findColAmount(row_coords)

    # Check the save folder if we want to use it
    if use_save_file:
        if "row-digits.txt" not in save_folder:
            row_digits = nonoSolvFunc.extractRowNumbers(col_amount)
            with open('save_files/row-digits.txt', 'w+') as f:
                for line in row_digits:
                    for number in line:
                        f.write(f"{number} ")
                    f.write('\n')
        else:
            row_digits = []
            rowdigit_file = open('save_files/row-digits.txt', 'r')
            for line in rowdigit_file.readlines():
                row_digits.append((line.split(' ')))
            for i in row_digits:
                for id_j, j in enumerate(i):
                    try:
                        i[id_j] = int(j)
                    except:
                        i.remove(i[id_j])

    else:
        row_digits = nonoSolvFunc.extractRowNumbers(col_amount)

    # Make a two-dimensional array to store the game board
    if use_save_file and 'board' in os.listdir('save_files'):
        # Version from the txt file
        unfiltered_game_board = []

        # Clean version
        game_board = []

        backup_index = len(os.listdir('save_files/board'))

        # If there's no backup, create an empty board
        if backup_index == 0:
            for i in range(col_amount):
                game_board.append([])
                for j in range(row_amount):
                    game_board[i].append(0)
        else:
            board_file = open(f'save_files/board/{backup_index - 1}.txt')
            for line in board_file.readlines():
                unfiltered_game_board.append((line.split(' ')))

            # Cleaning
            for id_i, i in enumerate(unfiltered_game_board):
                game_board.append([])
                for j in i:
                    if j == 'T' or j == 'F':
                        game_board[id_i].append(str(j))
                    elif j == '0':
                        game_board[id_i].append(int(j))

    else:
        game_board = []
        for i in range(col_amount):
            game_board.append([])
            for j in column_digits:
                game_board[i].append(0)

    # Copy the board (Will be useful later)
    previous_board = []
    for i in range(col_amount):
        previous_board.append([])
        for j in column_digits:
            previous_board[i].append(0)

    # Make a similar array to store the working area
    working_area_board = []
    for i in range(col_amount):
        working_area_board.append([])
        for j in row_digits:
            working_area_board[i].append(0)

    # For the pygame display
    columns_height = max(map(len, column_digits))
    row_width = max(map(len, row_digits))

    # Length of the whole board
    board_width = pygame_width[0]
    # Length of the tiles' side
    tile_width = board_width/row_amount
    # Shift from the top left corner
    grid_shift = 20

    if is_pygame_used:
        # Setup for text displaying
        pygame.font.init()
        font = pygame.font.SysFont("Arial", int(tile_width))

        # Display the board in a pygame window (for testing)
        pygame.init
        screen = pygame.display.set_mode((1000, 1000))
        screen.fill((42, 43, 35))
        setPygame()
except:
    print("An error occured while initializing.")


# FIRST PART: only has to be done once
# Do the lines that have only one possibility
def beginSolve():
    for i in range(row_amount):
        current_line = nonoSolvFunc.doFullLine(
            col_amount, column_digits[i], [])
        nonoSolvFunc.fillColumn(current_line, game_board, i)

    for i in range(col_amount):
        current_line = nonoSolvFunc.doFullLine(row_amount, row_digits[i], [])
        nonoSolvFunc.fillRow(current_line, game_board, i)

    # Do the remaining confirmed tiles (by the extremums)
# Do columns
    for i in range(row_amount):
        line_index = i
        for id_j, _ in enumerate(column_digits[i]):
            number_index = id_j
            current_working_area = (nonoSolvFunc.limitLineArea(
                column_digits[line_index], number_index, col_amount))
            nonoSolvFunc.limitColumnArea(
                working_area_board, current_working_area, line_index)

            extremum_array = nonoSolvFunc.doExtremumConfirm(
                current_working_area, column_digits[line_index][number_index])
            nonoSolvFunc.fillColumn(extremum_array, game_board, line_index)

# Do rows
    for i in range(col_amount):
        line_index = i
        for id_j, _ in enumerate(row_digits[i]):
            number_index = id_j
            current_working_area = (nonoSolvFunc.limitLineArea(
                row_digits[line_index], number_index, row_amount))
            nonoSolvFunc.limitRowArea(
                working_area_board, current_working_area, line_index)

            extremum_array = nonoSolvFunc.doExtremumConfirm(
                current_working_area, row_digits[line_index][number_index])
            nonoSolvFunc.fillRow(extremum_array, game_board, line_index)

    # Complete lines with T's if it's the only possibility with the current board configuration
# Do columns
    for i in range(row_amount):
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.doConfirmedTiles(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

# Do rows
    for i in range(col_amount):
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.doConfirmedTiles(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)


# SECOND PART: Repeats until it does nothing
def repeatSolve():
    while previous_board != game_board:
        for id_i, i in enumerate(game_board):
            previous_board[id_i] = i.copy()
        # Complete lines with F's when all black squares on the line are found:
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.doCompleteLine(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.doCompleteLine(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Complete lines with T's if it's the only possibility with the current board configuration
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.doCompleteBlackSquares(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.doCompleteBlackSquares(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Complete what's possible when a line has only one number and F's (e.g. 3 on a row that is 00TF0 becomes 00TFF)
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.reduceSingularNumbers(
                column_digits[i], current_line)
            current_complete_array.reverse()
            current_complete_array = nonoSolvFunc.reduceSingularNumbers(
                column_digits[i], current_complete_array)
            current_complete_array.reverse()
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.reduceSingularNumbers(
                row_digits[i], current_line)
            current_complete_array.reverse()
            current_complete_array = nonoSolvFunc.reduceSingularNumbers(
                row_digits[i], current_complete_array)
            current_complete_array.reverse()
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Place tiles that can't fit elsewhere
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.tileCannotFit(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.tileCannotFit(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Check extremums that are done
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.extremumCompletion(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.extremumCompletion(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Fill the overlapping tiles
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillOverlapping(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillOverlapping(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Check the range when there's only one number
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.checkRange(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.checkRange(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Complete limited parts of a line
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.completeLimitedLine(
                column_digits[i], current_line, col_amount)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.completeLimitedLine(
                row_digits[i], current_line, row_amount)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Extend the extremums
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.extendExtremum(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.extendExtremum(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Fill every space when possible
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillSpaces(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillSpaces(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Surround blocks
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.surroundBlocks(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.surroundBlocks(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Join tiles by removing gaps
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.joinTiles(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.joinTiles(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Join tiles by removing gaps
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillBeginning(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillBeginning(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Join tiles by removing gaps
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.crossReach(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.crossReach(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Fill singular spaces
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillOneSpace(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillOneSpace(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Fill extremums when possible
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillExtremum(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillExtremum(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Complete the beginning and / or the end when marked tiles have to be here
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.completeBeginning(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.completeBeginning(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Fill the largest part(s) when possible
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillLargest(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillLargest(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Fill after last when we can find it
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.stopAfterLastMax(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.stopAfterLastMax(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Fill before first when possible
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillBeforeBeginning(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillBeforeBeginning(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Do full line relatively
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.relFullLine(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.relFullLine(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Remove impossible situations and replace what's possible
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.removeImpossible(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.removeImpossible(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Do overlap over several parts
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.multiOverlap(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.multiOverlap(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Cross beginning if possible
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.crossBeginning(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.crossBeginning(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Separate spaces
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.separateSpaces(
                column_digits[i], current_line)
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.separateSpaces(
                row_digits[i], current_line)
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Fill spaces that can't have anything
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillImpossibleSpaces(
                column_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.fillImpossibleSpaces(
                column_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.fillImpossibleSpaces(
                row_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.fillImpossibleSpaces(
                row_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Put an F after completed tiles
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.crossAfterComplete(
                column_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.crossAfterComplete(
                column_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.crossAfterComplete(
                row_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.crossAfterComplete(
                row_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Complete what we can when spaces match the current line's numbers
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.matchSpaces(
                column_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.matchSpaces(
                column_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.matchSpaces(
                row_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.matchSpaces(
                row_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Cross tiles between the numbers on a line
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.numberSeparation(
                column_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.numberSeparation(
                column_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.numberSeparation(
                row_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.numberSeparation(
                row_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Complete the part of a line before the first marked tiles
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.completeBefore(
                column_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.completeBefore(
                column_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.completeBefore(
                row_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.completeBefore(
                row_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Cross tiles before the first number
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.crossBeforeFirst(
                column_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.crossBeforeFirst(
                column_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.crossBeforeFirst(
                row_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.crossBeforeFirst(
                row_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Complete the first space when possible
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.completeFirstSpace(
                column_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.completeFirstSpace(
                column_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.completeFirstSpace(
                row_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.completeFirstSpace(
                row_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Place two numbers in one space
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.placeTwoInSpace(
                column_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.placeTwoInSpace(
                column_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.placeTwoInSpace(
                row_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.placeTwoInSpace(
                row_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Complete the first number of the line when its segment is directly followed by a cross
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.completeFirstBeforeCross(
                column_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.completeFirstBeforeCross(
                column_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.completeFirstBeforeCross(
                row_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.completeFirstBeforeCross(
                row_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Check the tile of the same index as the first number of the line
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.crossFirstOfSpace(
                column_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.crossFirstOfSpace(
                column_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.crossFirstOfSpace(
                row_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.crossFirstOfSpace(
                row_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)

        # Do every relative function without considering the largest numbers
        # Do columns
        for i in range(row_amount):
            current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.removeLargest(
                column_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.removeLargest(
                column_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        for i in range(col_amount):
            current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
            current_complete_array = nonoSolvFunc.removeLargest(
                row_digits[i][::-1], current_line[::-1])
            current_complete_array = nonoSolvFunc.removeLargest(
                row_digits[i], current_complete_array[::-1])
            nonoSolvFunc.fillRow(current_complete_array, game_board, i)
        
        # NOTE: problem with removeLargest, see board file 205.txt in the save files


# Update Pygame visually
def updatePygame():
    board_width = pygame_width[0]
    tile_width = board_width/row_amount
    for i in range(row_amount):
        for j in range(col_amount):
            if game_board[j][i] == "T":
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
                    grid_shift + (tile_width * row_width) + i * tile_width + tile_width / tile_length, grid_shift + (tile_width * columns_height) + j * tile_width + tile_width / tile_length, tile_width - tile_width / (tile_length / 2), tile_width - tile_width / (tile_length / 2)))
            elif game_board[j][i] == "F":
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
                    grid_shift + (tile_width * row_width) + i * tile_width + tile_width / tile_length, grid_shift + (tile_width * columns_height) + j * tile_width + tile_width / tile_length, tile_width - tile_width / (tile_length / 2), tile_width - tile_width / (tile_length / 2)))
            elif game_board[j][i] == 0:
                pygame.draw.rect(screen, (248, 236, 194), pygame.Rect(
                    grid_shift + (tile_width * row_width) + i * tile_width + tile_width / tile_length, grid_shift + (tile_width * columns_height) + j * tile_width + tile_width / tile_length, tile_width - tile_width / (tile_length / 2), tile_width - tile_width / (tile_length / 2)))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
                grid_shift + (tile_width * row_width) + i * tile_width, grid_shift + (tile_width * columns_height) + j * tile_width, tile_width, tile_width), 3)


# Things that will be working in both Pygame windows (the manual line changer and the game solver)
def commonPygame(e: pygame.Event, w: list):
    if e.type == pygame.KEYDOWN:
        # Zoom in
        if event.key == pygame.K_KP_PLUS:
            w[0] += 50
        # Zoom out
        elif event.key == pygame.K_KP_MINUS:
            w[0] -= 50
        setPygame()


# Place the tiles in-game in the browser
def placeIngame():
    board_coords = nonoSolvFunc.getBoardCoords(column_coords[0], row_coords[1])
    nonoSolvFunc.placeTiles(row_amount, board_coords, game_board)


try:
    # Let the user change the board numbers if they are incorrect
    if is_pygame_used and double_check_line:
        gameRunning = True
        while gameRunning:
            for event in pygame.event.get():
                # Things that are in common for both Pygame windows
                commonPygame(event, pygame_width)
                board_width = pygame_width[0]
                tile_width = board_width/row_amount

                # Detect left click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Tile that has been clicked
                    clicked_tile = [int((pygame.mouse.get_pos()[0] - (grid_shift + (tile_width * row_width))) // (board_width / row_amount)),
                                    int((pygame.mouse.get_pos()[1] - (grid_shift + (tile_width * columns_height))) // (board_width / row_amount))]

                    # Only proceed if we clicked a line (and not the board)
                # Do rows
                    if clicked_tile[0] >= -row_width and clicked_tile[0] < 0 and clicked_tile[1] >= 0 and clicked_tile[1] < col_amount:
                        board = []
                        value = ''
                        print(
                            f"What will be the new value of {row_digits[clicked_tile[1]]}, the #{clicked_tile[1] + 1} row?")
                        while value != end_char:
                            value = input(f'Enter an integer:')
                            if value != end_char and value != '':
                                board.append(int(value))
                        row_digits[clicked_tile[1]] = board
                # Do columns
                    if clicked_tile[0] >= 0 and clicked_tile[0] < row_amount and clicked_tile[1] >= -columns_height and clicked_tile[1] < 0:
                        board = []
                        value = ''
                        print(
                            f"What will be the new value of {column_digits[clicked_tile[0]]}, the #{clicked_tile[0] + 1} row?")
                        while value != end_char:
                            value = input(f'Enter an integer:')
                            if value != end_char and value != '':
                                board.append(int(value))
                        column_digits[clicked_tile[0]] = board
                    setPygame()

                if event.type == pygame.QUIT:
                    # Save the lines if using a save file is set to True
                    if use_save_file:
                        # Do columns
                        with open('save_files/column-digits.txt', 'w+') as f:
                            for line in column_digits:
                                for number in line:
                                    f.write(f"{number} ")
                                f.write('\n')

                    # Do rows
                        with open('save_files/row-digits.txt', 'w+') as f:
                            for line in row_digits:
                                for number in line:
                                    f.write(f"{number} ")
                                f.write('\n')

                    try:
                        # Do the beginning of the solve
                        beginSolve()
                        repeatSolve()

                        # Save the first intsance of the board if the save option is used
                        if use_save_file:
                            if "board" not in save_folder:
                                os.makedirs('save_files/board')
                                with open('save_files/board/0.txt', 'w+') as f:
                                    for line in game_board:
                                        for tile in line:
                                            f.write(f"{tile} ")
                                        f.write('\n')
                            elif len(os.listdir('save_files/board')) == 0:
                                with open('save_files/board/0.txt', 'w+') as f:
                                    for line in game_board:
                                        for tile in line:
                                            f.write(f"{tile} ")
                                        f.write('\n')

                        gameRunning = False
                    except:
                        print(
                            "An error occured while trying to begin the solve. Please make sure that the numbers for the lines are correct.")
                        for i in game_board:
                            for id_j, _ in enumerate(i):
                                i[id_j] = 0

            pygame.display.update()
        pygame.quit()
except:
    print("An error occured during the manual line changer.")
    gameRunning = False

# Display in Pygame
try:
    if is_pygame_used:
        # ------------------------
        # Draw the tiles in Pygame
        # ------------------------

        # The higher the number is, the larger the tile length will be displayed
        tile_length = 7.5

        gameRunning = True
        # Setup for text displaying
        pygame.font.init()
        font = pygame.font.SysFont("Arial", int(tile_width))

        # Display the board in a pygame window
        pygame.init
        screen = pygame.display.set_mode((1000, 1000))
        screen.fill((42, 43, 35))
        setPygame()

        while gameRunning:
            updatePygame()
            board_width = pygame_width[0]
            tile_width = board_width/row_amount

            for event in pygame.event.get():
                # Things that are in common for both Pygame windows
                commonPygame(event, pygame_width)

                # Detect left click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Tile that has been clicked
                    clicked_tile = [int((pygame.mouse.get_pos()[0] - (grid_shift + (tile_width * row_width))) // (board_width / row_amount)),
                                    int((pygame.mouse.get_pos()[1] - (grid_shift + (tile_width * columns_height))) // (board_width / row_amount))]

                    # Only update the board when the clicked position is in the board
                    if clicked_tile[0] >= 0 and clicked_tile[0] < row_amount and clicked_tile[1] >= 0 and clicked_tile[1] < col_amount:
                        # State of this tile (0 by default, T for a black square, or F for a red square that corresponds to a cross in-game in the browser)
                        tile_state = game_board[clicked_tile[1]
                                                ][clicked_tile[0]]

                        # Left click on a black tile
                        if tile_state == 'T' and event.button == 1:
                            game_board[clicked_tile[1]][clicked_tile[0]] = 0
                        # Left click on a non-black tile
                        if tile_state != 'T' and event.button == 1:
                            game_board[clicked_tile[1]][clicked_tile[0]] = 'T'
                        # Right click on a red tile
                        if tile_state == 'F' and event.button == 3:
                            game_board[clicked_tile[1]][clicked_tile[0]] = 0
                        # Left click on a non-red tile
                        if tile_state != 'F' and event.button == 3:
                            game_board[clicked_tile[1]][clicked_tile[0]] = 'F'

                # Do all the functions when R is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    try:
                        board_before = copy.deepcopy(game_board)
                        repeatSolve()
                        # Make a backup if the game changed
                        if board_before != game_board:
                            backup_index = len(os.listdir('save_files/board'))
                            with open(f'save_files/board/{backup_index}.txt', 'w+') as f:
                                for line in game_board:
                                    for tile in line:
                                        f.write(f"{tile} ")
                                    f.write('\n')
                        backup_index = len(os.listdir('save_files/board'))
                    # If an error occured, use a backup if using save files, restart otherwise
                    except:
                        if use_save_file and 'board' in os.listdir('save_files'):
                            print(
                                "An error occured. The game will use the latest backup. If the error persists, remove backup files as they may contain mistakes in the game's progress.")

                            # Use the latest backup
                            backup_index = len(os.listdir('save_files/board'))
                            # Version from the txt file
                            unfiltered_game_board = []

                            # Clean version
                            game_board = []

                            # If there's no file in the backup folder, restart the game
                            if backup_index == 0:
                                if backup_index == 0:
                                    for i in range(row_amount):
                                        game_board.append([])
                                        for j in range(row_amount):
                                            game_board[i].append(0)
                                beginSolve()
                                repeatSolve()
                                with open('save_files/board/0.txt', 'w+') as f:
                                    for line in game_board:
                                        for tile in line:
                                            f.write(f"{tile} ")
                                        f.write('\n')

                            else:
                                board_file = open(
                                    f'save_files/board/{backup_index - 1}.txt')
                                for line in board_file.readlines():
                                    unfiltered_game_board.append(
                                        (line.split(' ')))

                                # Cleaning
                                for id_i, i in enumerate(unfiltered_game_board):
                                    game_board.append([])
                                    for j in i:
                                        if j == 'T' or j == 'F':
                                            game_board[id_i].append(str(j))
                                        elif j == '0':
                                            game_board[id_i].append(int(j))

                        else:
                            print("An error occured. The game will restart.")
                            for id_i, i in enumerate(game_board):
                                for id_j, j in enumerate(i):
                                    game_board[id_i][id_j] = 0
                            beginSolve()
                            repeatSolve()

                # Check every tile that can't work and switch if we can
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    # Becomes True when a tile is being switched
                    is_tile_found = False

                    current_board = copy.deepcopy(game_board)
                    for id_i, i in enumerate(game_board):
                        if is_tile_found:
                            break
                        for id_j, j in enumerate(game_board[id_i]):
                            if j == 0:
                                game_board[id_i][id_j] = 'T'
                                try:
                                    repeatSolve()
                                    game_board = copy.deepcopy(current_board)
                                except:
                                    game_board = copy.deepcopy(current_board)
                                    game_board[id_i][id_j] = 'F'
                                    current_board = copy.deepcopy(game_board)
                                    print(id_i)
                                    print(id_j)
                                    print("-------------")
                                    is_tile_found = False

                                game_board[id_i][id_j] = 'F'
                                try:
                                    repeatSolve()
                                    game_board = copy.deepcopy(current_board)
                                except:
                                    game_board = copy.deepcopy(current_board)
                                    game_board[id_i][id_j] = 'T'
                                    current_board = copy.deepcopy(game_board)
                                    print(id_i)
                                    print(id_j)
                                    print("-------------")
                                    is_tile_found = False

                # Check every tile that can't work and switch if we can
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    # Hovered tile
                    highlighted_tile = [int((pygame.mouse.get_pos()[0] - (grid_shift + (tile_width * row_width))) // (board_width / row_amount)),
                                        int((pygame.mouse.get_pos()[1] - (grid_shift + (tile_width * columns_height))) // (board_width / row_amount))]
                    setPygame()

                # Make a savestate
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    try:
                        savestate = copy.deepcopy(game_board)
                        print("A savestate has successfully been made.")
                    except:
                        print("Failed to make a savestate.")

                # Load the last savestate
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    try:
                        game_board = copy.deepcopy(savestate)
                        print("The last savestate has successfully been loaded.")
                    except:
                        print(
                            "Failed to load the savestate. Please make sure that you made a savestate by pressing S.")

                # Use another backup with the left and right arrows
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        try:
                            if event.key == pygame.K_LEFT and backup_index > 0:
                                backup_index -= 1
                            elif event.key == pygame.K_RIGHT and backup_index < len(os.listdir('save_files/board')):
                                backup_index += 1

                            # Version from the txt file
                            unfiltered_game_board = []

                            # Clean version
                            game_board = []

                            # If there's no file in the backup folder, restart the game
                            if backup_index == 0:
                                if backup_index == 0:
                                    for i in range(col_amount):
                                        game_board.append([])
                                        for j in range(row_amount):
                                            game_board[i].append(0)
                                beginSolve()
                                repeatSolve()
                                with open('save_files/board/0.txt', 'w+') as f:
                                    for line in game_board:
                                        for tile in line:
                                            f.write(f"{tile} ")
                                        f.write('\n')

                            else:
                                board_file = open(
                                    f'save_files/board/{backup_index - 1}.txt')
                                for line in board_file.readlines():
                                    unfiltered_game_board.append(
                                        (line.split(' ')))

                                # Cleaning
                                for id_i, i in enumerate(unfiltered_game_board):
                                    game_board.append([])
                                    for j in i:
                                        if j == 'T' or j == 'F':
                                            game_board[id_i].append(str(j))
                                        elif j == '0':
                                            game_board[id_i].append(int(j))
                        except:
                            pass

                # Place in-game in the browser when P is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    placeIngame()
                    gameRunning = False

                if event.type == pygame.QUIT:
                    gameRunning = False
            pygame.display.update()
        pygame.quit()
except:
    print("An error occured while trying to display the board in Pygame.")


# ---------------------------
# Place the tiles in the game
# ---------------------------
if is_pygame_used == False:
    board_coords = nonoSolvFunc.getBoardCoords(column_coords[0], row_coords[1])
    nonoSolvFunc.placeTiles(row_amount, board_coords, game_board)
