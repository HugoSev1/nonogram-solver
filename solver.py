import nonoSolvFunc
import pygame

# Only proceed with Pygame if this is set to True (just change the value here if you want to toggle)
is_pygame_used = True

# Getting the coordinates of the blue box around the puzzle
puzzle_coords = nonoSolvFunc.getPuzzleCoords()

# Get the columns digits from here
column_coords = nonoSolvFunc.getColumnImage(puzzle_coords)
row_amount = nonoSolvFunc.findRowAmount(column_coords)

# How many rows there are
column_digits = nonoSolvFunc.extractColumnNumbers(row_amount)

# Read the digits from the columns
row_coords = nonoSolvFunc.getRowImage(puzzle_coords)
row_digits = nonoSolvFunc.extractRowNumbers(row_amount)

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

# Length of the whole board
board_width = 450
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

    # Complete limited parts of a line
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.completeLimitedLine(
            column_digits[i], current_line, row_amount)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.completeLimitedLine(
            row_digits[i], current_line, row_amount)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Extend the extremums
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.extendExtremum(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.extendExtremum(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Fill every space when possible
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillSpaces(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillSpaces(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Surround blocks
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.surroundBlocks(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.surroundBlocks(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Join tiles by removing gaps
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.joinTiles(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.joinTiles(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Join tiles by removing gaps
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillBeginning(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillBeginning(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Join tiles by removing gaps
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.crossReach(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.crossReach(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Fill singular spaces
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillOneSpace(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillOneSpace(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Fill extremums when possible
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillExtremum(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillExtremum(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Complete the beginning and / or the end when marked tiles have to be here
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.completeBeginning(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.completeBeginning(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Fill the largest part(s) when possible
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillLargest(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillLargest(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Fill after last when we can find it
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.stopAfterLastMax(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.stopAfterLastMax(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Fill before first when possible
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillBeforeBeginning(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillBeforeBeginning(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Do full line relatively
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.relFullLine(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.relFullLine(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Remove impossible situations and replace what's possible
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.removeImpossible(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.removeImpossible(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Do overlap over several parts
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.multiOverlap(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.multiOverlap(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Cross beginning if possible
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.crossBeginning(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.crossBeginning(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Separate spaces
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.separateSpaces(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.separateSpaces(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Fill spaces that can't have anything
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillImpossibleSpaces(
            column_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.fillImpossibleSpaces(
            column_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.fillImpossibleSpaces(
            row_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.fillImpossibleSpaces(
            row_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Put an F after completed tiles
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.crossAfterComplete(
            column_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.crossAfterComplete(
            column_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.crossAfterComplete(
            row_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.crossAfterComplete(
            row_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Complete what we can when spaces match the current line's numbers
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.matchSpaces(
            column_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.matchSpaces(
            column_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.matchSpaces(
            row_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.matchSpaces(
            row_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Cross tiles between the numbers on a line
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.numberSeparation(
            column_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.numberSeparation(
            column_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.numberSeparation(
            row_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.numberSeparation(
            row_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Complete the part of a line before the first marked tiles
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.completeBefore(
            column_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.completeBefore(
            column_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.completeBefore(
            row_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.completeBefore(
            row_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Cross tiles before the first number
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.crossBeforeFirst(
            column_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.crossBeforeFirst(
            column_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.crossBeforeFirst(
            row_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.crossBeforeFirst(
            row_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Complete the first space when possible
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.completeFirstSpace(
            column_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.completeFirstSpace(
            column_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.completeFirstSpace(
            row_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.completeFirstSpace(
            row_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Place two numbers in one space
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.placeTwoInSpace(
            column_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.placeTwoInSpace(
            column_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.placeTwoInSpace(
            row_digits[i][::-1], current_line[::-1])
        current_complete_array = nonoSolvFunc.placeTwoInSpace(
            row_digits[i], current_complete_array[::-1])
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

    # Do every relative function without considering the largest numbers
    for i in range(row_amount):
        # Do columns
        current_line = nonoSolvFunc.extractColFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.removeLargest(
            column_digits[i], current_line)
        nonoSolvFunc.fillColumn(current_complete_array, game_board, i)

        # Do rows
        current_line = nonoSolvFunc.extractRowFromBoard(game_board, i)
        current_complete_array = nonoSolvFunc.removeLargest(
            row_digits[i], current_line)
        nonoSolvFunc.fillRow(current_complete_array, game_board, i)

if is_pygame_used:
    # ------------------------
    # Draw the tiles in Pygame
    # ------------------------

    # The higher the number is, the larger the tile length will be displayed
    tile_length = 7.5

    for i in range(row_amount):
        for j in range(row_amount):
            if game_board[j][i] == "T":
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
                    grid_shift + (tile_width * row_width) + i * tile_width + tile_width / tile_length, grid_shift + (tile_width * columns_height) + j * tile_width + tile_width / tile_length, tile_width - tile_width / (tile_length / 2), tile_width - tile_width / (tile_length / 2)))
            elif game_board[j][i] == "F":
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
                    grid_shift + (tile_width * row_width) + i * tile_width + tile_width / tile_length, grid_shift + (tile_width * columns_height) + j * tile_width + tile_width / tile_length, tile_width - tile_width / (tile_length / 2), tile_width - tile_width / (tile_length / 2)))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
                grid_shift + (tile_width*row_width) + i*tile_width, grid_shift + (tile_width*columns_height) + j*tile_width, tile_width, tile_width), 3)

    gameRunning = True
    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
        pygame.display.update()

    pygame.quit()


# ---------------------------
# Place the tiles in the game
# ---------------------------
board_coords = nonoSolvFunc.getBoardCoords(column_coords[0], row_coords[1])
if is_pygame_used == False:
    nonoSolvFunc.placeTiles(row_amount, board_coords, game_board)
