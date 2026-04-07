import pyautogui
from PIL import ImageGrab
import cv2
pyautogui.PAUSE = 0.001

# Display an image (for debugging purposes)


def showImg(img):
    cv2.imshow("Image", img)
    cv2.waitKey()


# Function that returns the coordinates of the area to work with inside of the blue box
def getPuzzleCoords():
    puzzle_coords = []
    # Getting the top left coordinates
    color = (61, 63, 65)
    scrsh = pyautogui.screenshot()
    for x in range(200, 1500):
        for y in range(100, 1000):
            if scrsh.getpixel((x, y)) == color:
                puzzle_coords.append(x)
                puzzle_coords.append(y)
                break
        if len(puzzle_coords) > 0:
            break

    x1 = puzzle_coords[0]
    y1 = puzzle_coords[1]

    # Getting the bottom right coordinates
    for x in range(x1+1, 2500):
        if scrsh.getpixel((x, y1+1)) == color:
            puzzle_coords.append(x)
            break

    for y in range(y1+1, 2000):
        if scrsh.getpixel((x1+1, y)) == color:
            puzzle_coords.append(y)
            break

    return (puzzle_coords)


# Function that saves the image of the columns area (takes an array of 4 numbers that make two opposite corners of the area)
def getColumnImage(area_array):
    column_coords = []
    color = (248, 236, 194)
    scrsh = pyautogui.screenshot()
    for y in range(area_array[1], area_array[3]):
        for x in range(area_array[0], area_array[2]):
            if scrsh.getpixel((x, y)) == color:
                column_coords.append(x)
                column_coords.append(y)
                break
            if len(column_coords) >= 2:
                break
    xColumn = column_coords[0]
    yColumn = column_coords[1]
    color = (0, 0, 0)
    while scrsh.getpixel((xColumn, yColumn)) != color:
        yColumn += 1
    color = (28, 30, 32)
    while scrsh.getpixel((xColumn, yColumn)) != color:
        xColumn += 1
    column_coords.append(xColumn)
    column_coords.append(yColumn)

    column_img = ImageGrab.grab(
        bbox=(column_coords[0], column_coords[1], column_coords[2], column_coords[3]))
    column_img.save("column-img.png")
    return column_coords


def getRowImage(area_array):
    row_coords = []
    color = (248, 236, 194)
    scrsh = pyautogui.screenshot()
    for x in range(area_array[0], area_array[2]):
        for y in range(area_array[1], area_array[3]):
            if scrsh.getpixel((x, y)) == color:
                row_coords.append(x)
                row_coords.append(y)
                break
            if len(row_coords) >= 2:
                break
    xColumn = row_coords[0]
    yColumn = row_coords[1]
    color = (0, 0, 0)
    while scrsh.getpixel((xColumn, yColumn)) != color:
        xColumn += 1
    color = (28, 30, 32)
    while scrsh.getpixel((xColumn, yColumn)) != color:
        yColumn += 1
    row_coords.append(xColumn)
    row_coords.append(yColumn)

    row_img = ImageGrab.grab(
        bbox=(row_coords[0], row_coords[1], row_coords[2], row_coords[3]))
    row_img.save("row-img.png")
    return row_coords


# Function that returns the amount of rows / columns
def findRowAmount(coords):
    # Value that will be returned
    row_amount = 0
    scrsh = pyautogui.screenshot()
    column_color = (248, 236, 194)

    x_start = coords[0]
    y_start = coords[1]

    # Alternates between True and False depending on the color
    is_counting = True
    pyautogui.moveTo(x_start, y_start)
    for x in range(x_start, x_start + 1000):
        if scrsh.getpixel((x, y_start)) == column_color and is_counting:
            row_amount += 1
            is_counting = False

        elif scrsh.getpixel((x, y_start)) != column_color:
            is_counting = True

    return row_amount


# Best score (for recognition accuracy)
extraction_best_score = 0.7


# Function that extracts the numbers shown on the Nonogram
def extractColumnNumbers(row_amount):
    extractingArray = []
    # Divides the image in 5 chunks
    img = cv2.imread("column-img.png")
    h, w, c, = img.shape
    n_chunks = row_amount
    chunk_width = w // n_chunks

    chunks = []

    for i in range(n_chunks):
        # Separate into chunks (e.g. 5 chunks for a 5x5 Nonogram)
        start_x = i * chunk_width

        if i == n_chunks - 1:
            end_x = w
        else:
            end_x = (i + 1) * chunk_width

        chunk = img[:, start_x:end_x]
        chunks.append(chunk)

        # Detect digits
        gray = cv2.cvtColor(chunk, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        digits = []
        for cnt in contours:
            x, y, w2, h2 = cv2.boundingRect(cnt)
            roi = thresh[y:y+h2, x:x+w2]
            roi = cv2.resize(roi, (50, 50))

            best_match = None
            best_score = -1

            for digit in range(0, row_amount):
                template = cv2.imread(f"templates\\{digit}.png", 0)
                _, template = cv2.threshold(
                    template, 150, 255, cv2.THRESH_BINARY_INV)
                template = cv2.resize(template, (50, 50))
                score = cv2.matchTemplate(
                    roi, template, cv2.TM_CCOEFF_NORMED)[0][0]

                if (score > best_score):
                    best_score = score
                    best_match = digit

            if (best_score > extraction_best_score):
                digits.append((best_match, x, y, h2))
        digits.sort(key=lambda x: x[2])
        numbers = []
        if digits:
            current_group = [digits[0]]

            for i in range(1, len(digits)):
                prev_bottom = digits[i-1][2] + digits[i-1][3]
                curr_y = digits[i][2]

                # Can be adjusted
                spacing_threshold = h // 20

                if curr_y - prev_bottom < spacing_threshold:
                    current_group.append(digits[i])
                else:
                    numbers.append(current_group)
                    current_group = [digits[i]]

            numbers.append(current_group)

        # Convert grouped digits into actual numbers
        result = []

        for group in numbers:
            # Sort digits from left to right to reconstruct them (e.g. if a 10 is above a 2, make 10 from left to right after putting the 10 above the 2)
            group.sort(key=lambda x: x[1])  # x position

            number = int("".join(str(d[0]) for d in group))
            result.append(number)

        extractingArray.append(result)
    return extractingArray


# Function that extracts the numbers shown on the Nonogram (but for the rows this time)
def extractRowNumbers(row_amount):
    extractingArray = []
    # Divides the image in 5 chunks
    img = cv2.imread("row-img.png")
    h, w, c, = img.shape
    n_chunks = row_amount
    chunk_height = h // n_chunks

    chunks = []

    for i in range(n_chunks):
        # Separate into chunks (e.g. 5 chunks for a 5x5 Nonogram)
        start_y = i * chunk_height

        if i == n_chunks - 1:
            end_y = h
        else:
            end_y = (i + 1) * chunk_height

        chunk = img[start_y:end_y, :]
        chunks.append(chunk)
        # showImg(chunk)

        # Detect digits
        gray = cv2.cvtColor(chunk, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        digits = []
        for cnt in contours:
            x, y, w2, h2 = cv2.boundingRect(cnt)
            roi = thresh[y:y+h2, x:x+w2]
            roi = cv2.resize(roi, (50, 50))

            best_match = None
            best_score = -1

            for digit in range(0, row_amount):
                template = cv2.imread(f"templates\\{digit}.png", 0)
                _, template = cv2.threshold(
                    template, 150, 255, cv2.THRESH_BINARY_INV)
                template = cv2.resize(template, (50, 50))
                score = cv2.matchTemplate(
                    roi, template, cv2.TM_CCOEFF_NORMED)[0][0]

                if (score > best_score):
                    best_score = score
                    best_match = digit

            if (best_score > extraction_best_score):
                digits.append((best_match, x, w2))
        digits.sort(key=lambda x: x[1])
        numbers = []
        if digits:
            current_group = [digits[0]]

            for i in range(1, len(digits)):
                prev_right = digits[i-1][1] + digits[i-1][2]
                curr_x = digits[i][1]

                # Can be adjusted
                spacing_threshold = w // 20

                if curr_x - prev_right < spacing_threshold:
                    current_group.append(digits[i])
                else:
                    numbers.append(current_group)
                    current_group = [digits[i]]

            numbers.append(current_group)

        # Convert grouped digits into actual numbers
        result = [int("".join(str(d[0]) for d in group)) for group in numbers]

        extractingArray.append(result)
    return extractingArray


# Function that gets the board's coordinates from the browser in order to place the tiles directly
def getBoardCoords(x1, y1):
    board_coords = [x1, y1]
    color = (28, 30, 32)
    scrsh = pyautogui.screenshot()

    # Append the X at the right of the board
    for x in range(x1, x1 + 1000):
        if scrsh.getpixel((x, y1)) == color:
            board_coords.append(x)
            break

    # Append the Y at the bottom of the board
    for y in range(y1, y1 + 1000):
        if scrsh.getpixel((x1, y)) == color:
            board_coords.append(y)
            break

    return board_coords


# Function that places tiles in the browser
def placeTiles(row_amount, board_coords, game_board):
    length = board_coords[2] - board_coords[0]
    tile_length = int(length / row_amount)

    for id_i, i in enumerate(game_board):
        for id_j, j in enumerate(i):
            if j == 'T':
                pyautogui.leftClick(board_coords[0] + ((id_j + 1) * tile_length) - (
                    tile_length / 2), board_coords[1] + ((id_i + 1) * tile_length) - (tile_length / 2))


# -------------------------------------------------------------------------------------------------------------------------------------------------------
# The next functions will help in later functions
# Note: I started writing these late in the code, so some functions won't use them even when it would've been better
# -------------------------------------------------------------------------------------------------------------------------------------------------------

# This function returns the amount of spaces (e.g. the places that can contain a part of a line, separated by one or more F's)
def getSpaces(current_board_line):
    # Variable that will get returned
    spaces = []

    # Separate the spaces
    space = []
    for i in current_board_line:
        # Put the current space in the spaces list when and F is found, but keep appending to the current space otherwise
        if i == 'F' and len(space) > 0:
            spaces.append(space[:])
            space.clear()
        elif i != 'F':
            space.append(i)

    # Put the last space in the list if any is left to be put
    if len(space) > 0:
        spaces.append(space[:])

    # Return the list
    return spaces


# This function returns the minimal amount of tiles that it takes to complete a line (e.g. for [3, 1, 1, 1, 1] it returns 11)
def getMinTiles(current_line):
    tiles_sum = 0

    # Add the T tiles
    for i in current_line:
        tiles_sum += i

    # Add one F tile in between
    tiles_sum += len(current_line) - 1

    # Return the number
    return tiles_sum


# This function puts spaces (from the getSpaces function) back into the board line
def putSpacesBack(spaces, current_board_line):
    # Board that will get returned
    working_board = []

    # Make a one-dimensional list of spaces
    clean_spaces = []
    for i in spaces:
        clean_spaces.extend(i)

    for i in current_board_line:
        if i == 'F':
            working_board.append('F')
        else:
            working_board.append(clean_spaces[0])
            clean_spaces.pop(0)

    return working_board


# -------------------------------------------------------------------------------------------------------------------------------------------------------
# The next functions will be to solve the puzzle (In the arrays, "T" refers to a tile that has to be checked, "F" to a tile that has to be unchecked and 0 to a tile that has yet to be marked)
# -------------------------------------------------------------------------------------------------------------------------------------------------------

# Function that extracts a column from the board
def extractColFromBoard(board, index):
    # Create an empty array
    line_array = []

    # Put the values in the array
    for i in range(len(board)):
        line_array.append(board[i][index])

    # Return the array
    return line_array


# Function that extracts a row from the board
def extractRowFromBoard(board, index):
    return board[index]

# Function that puts an array into a column in the game board


def fillColumn(array, board, columnIndex):
    for i in range(len(board)):
        if array != None and len(array) != 0:
            if array[i] == 'T' or array[i] == 'F':
                board[i][columnIndex] = array[i]


# Function that puts an array into a row in the game board
def fillRow(array, board, rowIndex):
    for i in range(len(board)):
        if array != None and len(array) != 0:
            if array[i] == 'T' or array[i] == 'F':
                board[rowIndex][i] = array[i]


# Function that solves lines that only have one possibility
def doFullLine(width_size, current_numbers, current_line):
    current_line = []

    # Check that the sum of all affected tiles is equal to the total amount of tiles on the current line
    if sum(current_numbers) + len(current_numbers) - 1 == width_size:
        for id_i, i in enumerate(current_numbers):
            for i in range(i):
                current_line.append("T")
            if id_i + 1 != len(current_numbers):
                current_line.append("F")
        return current_line


# Function that limits the working area for each number
def limitLineArea(line, number_index, row_amount):
    area_array = []
    before_area = 0
    after_area = 0
    # When the number is the first number in the column / row
    if number_index == 0:
        for i in range(len(line[1:])):
            after_area += 1
            after_area += line[1:][i]
    # When the number is the last number in the column / row
    elif number_index == len(line) - 1:
        for i in range(len(line[1:])):
            before_area += 1
            before_area += line[i]
    # When the number is in the middle (I will work on this when doing the 10x10 part)
    else:
        pass

    # Put the values in the array
    for i in range(before_area):
        area_array.append('X')
    for i in range(row_amount - (before_area + after_area)):
        area_array.append(0)
    for i in range(after_area):
        area_array.append('X')
    return area_array


# Function that puts a limited area into a column of the board
def limitColumnArea(board, working_area, line_index):
    for i in range(len(working_area)):
        if board[i][line_index] == 0:
            board[i][line_index] = working_area[i]


# Function that puts a limited area into a row of the board
def limitRowArea(board, working_area, line_index):
    for i in range(len(working_area)):
        if board[line_index][i] == 0:
            board[line_index][i] = working_area[i]


# Function that returns an array with the confirmed extremums
def doExtremumConfirm(working_array, number):
    current_working_array = []
    full_array = []
    final_array = []
    # Makes a smaller array to work with
    for i in working_array:
        if i == 0:
            current_working_array.append(i)

    # Checks confirmed tiles
    for i in range(-number, number):
        current_working_array[i] += 1
    append_offset = 0

    # Makes the full array with the updated numbers
    for i in working_array:
        if i == 0:
            full_array.append(current_working_array[append_offset])
            append_offset += 1
        else:
            full_array.append(0)
    # Makes the final array
    for i in full_array:
        if i == 2:
            final_array.append('T')
        else:
            final_array.append(0)
    return final_array


# Function that completes with F's when the full black squares are found
def doCompleteLine(current_line, current_board_line):
    # Complete array that will be returned
    complete_array = []

    # Sum of the digits of the line
    line_sum = sum(current_line)

    # Sum of the black tiles that are currently checked on the board
    on_board_sum = current_board_line.count('T')

    # If the line is completed, fill the remaining squares with F's
    if line_sum == on_board_sum:
        for i in range(len(current_board_line)):
            if current_board_line[i] == 'T':
                complete_array.append('T')
            else:
                complete_array.append('F')
    else:
        return current_board_line

    return complete_array


# Function that fills black squares when the only tiles left should be black squares
def doCompleteBlackSquares(current_line, current_board_line):
    # Complete array that will be returned
    complete_array = []

    # Highest possibility of black squares with current board configuration
    max_possible_black = 0

    # Adds 1 whenever a black square is / can be placed
    for i in current_board_line:
        if i == 0 or i == 'T':
            max_possible_black += 1

    # If the amount of possible black squares matches the sum of the numbers in the current line, then all of the remaining squares will be marked as 'T'
    if sum(current_line) == max_possible_black:
        for i in current_board_line:
            if i == 0:
                complete_array.append('T')
            else:
                complete_array.append(i)

        return complete_array

    else:
        return current_board_line


# Function that completes what's possible when a line has only one number and F's (e.g. 3 on a row that is 00TF0 becomes TTTF0)
def reduceSingularNumbers(current_line, current_board_line):
    working_array = []
    is_black_square_met = False
    is_crossed_square_met = False
    if len(current_line) == 1:
        for i in current_board_line:
            if i == 'T':
                is_black_square_met = True
                working_array.append(i)
            elif i == 'F':
                working_array.append(i)
                if is_black_square_met:
                    is_crossed_square_met = True
            elif i == 0:
                if is_crossed_square_met:
                    working_array.append('F')
                else:
                    working_array.append(0)

    else:
        return current_board_line
    return working_array


# Function that finds where a tile can't fit (e.g. a "2" can't go where inside 0 but can in 000 so it goes somewhere in the last 3 tiles of 0F000)
def tileCannotFit(current_line, current_board_line):
    # Base array
    working_array = []

    # Portion of the array
    array_part = []

    # Array that gets returned
    final_array = []

    if 'T' in current_board_line:
        return current_board_line
    else:
        for i in current_board_line:
            if i == 0:
                array_part.append(i)
            elif i == 'F':
                working_array.append(array_part[:])
                working_array.append(['F'])
                array_part.clear()

        working_array.append(array_part[:])

        for i in working_array:
            if min(current_line) > len(i):
                for id_j, j in enumerate(i):
                    i[id_j] = 'F'

        for i in working_array:
            final_array.extend(i)

        return final_array


# Function that finds when the first or last part of a line is completed
def extremumCompletion(current_line, current_board_line):
    # An array that contains what we want to have in order to keep the function going
    theoretical_array_first = []
    theoretical_array_last = []
    for i in range(current_line[0]):
        theoretical_array_first.append('T')

    for i in range(current_line[-1]):
        theoretical_array_last.append('T')

    if current_board_line[0:current_line[0]] == theoretical_array_first:
        current_board_line[current_line[0]] = 'F'
    elif current_board_line[-current_line[-1]:] == theoretical_array_last:
        current_board_line[-current_line[-1]-1] = 'F'

    return current_board_line


# Function that puts black squares on tiles that have 100% probability (i.e. a relative use of the extremum function when all the possibilites overlap)
def fillOverlapping(current_line, current_board_line):
    # Return the board line if it's already done
    if 0 not in current_board_line:
        return current_board_line

    # The board that will be modified
    working_board = current_board_line[:]

    # The F's at the beginning
    board_beginning = []

    # The final board
    final_board = []

    if len(current_line) == 1 and 0 in working_board:
        while working_board[0] == 'F':
            working_board.pop(0)
            board_beginning.append("F")

        # Initial board (with the original T's)
        initial_board = working_board[:]

        working_board.clear()
        for i in range(len(initial_board)):
            working_board.append(0)

        for i in range(-current_line[0], current_line[0]):
            working_board[i] += 1

        for id_i, i in enumerate(working_board):
            if i >= 2 or initial_board[id_i] == 'T':
                working_board[id_i] = 'T'

            else:
                working_board[id_i] = initial_board[id_i]

        final_board.extend(board_beginning)
        final_board.extend(working_board)

        return final_board

    else:
        return current_board_line


# Function that checks when there can't be any black tile when there's only one number (e.g. with just a 3, 02000 becomes 020XX)
def checkRange(current_line, current_board_line):
    # Only proceed when there's only one number in the line
    if len(current_line) == 1 and 'T' in current_board_line:
        # The tile where the black tile is found
        current_tile = 0

        working_board = current_board_line[:]

        # Do forward
        for id_i, i in enumerate(working_board):
            if i == 'T':
                current_tile = id_i
                break

        last_tile = min(current_tile + current_line[0], len(working_board))
        for i in range(current_tile + 1, last_tile):
            if i <= len(current_board_line) and working_board[i] == 0:
                working_board[i] = 'X'

        # Do backwards
        for i in range(-len(working_board), -1):
            if working_board[i] == 'T':
                current_tile = i
                break

        for i in range(current_tile - current_line[0], current_tile):
            if i >= -len(current_board_line) and working_board[i] == 0:
                working_board[i] = 'X'

        # Put the F's in the board and restaure the other 0's, then return it
        for id_i, i in enumerate(working_board):
            if i == 0:
                working_board[id_i] = 'F'
            elif i == 'X':
                working_board[id_i] = 0

        return working_board

    else:
        return current_board_line


# Function that completes lines in a limited area
def completeLimitedLine(current_line, current_board_line, row_amount):
    working_board = []
    final_array = []
    default_board = current_board_line[:]

    # Repeat the function for every number in the line
    for id_n, n in enumerate(current_line):
        current_number = n
        final_array.clear()
        working_board.clear()

        # Not using the current board disposition (e.g. XX000 instead of XXFT0)
        current_working_area = limitLineArea(current_line, id_n, row_amount)

        # Puts the limited current area in the limited working area
        for id_i, i in enumerate(current_working_area):
            if i == 0:
                working_board.append(default_board[id_i])

        # Check tiles when they are the only possible ones
        if current_number == working_board.count('T') + working_board.count(0):
            for id_i, i in enumerate(working_board):
                if i == 0:
                    working_board[id_i] = 'T'

        # Put everything back in a final array:
        for i in range(row_amount):
            if current_working_area[i] == 'X':
                final_array.append(default_board[i])
                working_board.insert(0, 'X')
            elif current_working_area[i] == 0:
                final_array.append(working_board[i])

        default_board = final_array[:]

    # Return the array after everything is done
    return final_array


# Extend an extremum (e.g. [3] that has the line T000000000 becomes TTT0000000)
def extendExtremum(current_line, current_board_line):
    # Check the full part that can change (e.g. 0T0 for [3] to make it 0TT)
    checking_area_first = []
    checking_area_last = []
    final_array = current_board_line[:]
    # Only start when a 'T' is found
    is_black_tile_found = False

    for i in range(current_line[0]):
        checking_area_first.append(current_board_line[i])

    for i in range(current_line[-1]):
        checking_area_last.append(current_board_line[-i-1])

    # Do first
    if 'T' in checking_area_first:
        for id_i, i in enumerate(checking_area_first):
            if is_black_tile_found and i == 0:
                checking_area_first[id_i] = 'T'
            elif i == 'T':
                is_black_tile_found = True

    # Do last
    is_black_tile_found = False

    if 'T' in checking_area_last:
        for id_i, i in enumerate(checking_area_last):
            if is_black_tile_found and i == 0:
                checking_area_last[id_i] = 'T'
            elif i == 'T':
                is_black_tile_found = True

    # Put the values in the board
    for id_i, i in enumerate(checking_area_first):
        final_array[id_i] = i

    for id_i, i in enumerate(checking_area_last):
        final_array[-id_i - 1] = i

    return final_array


# Function that fills every "space" (e.g. with 0TF000FFFF, fill the 0T and the 000 if possible)
def fillSpaces(current_line, current_board_line):
    # Return if the line is already done
    if 0 not in current_board_line or 'F' not in current_board_line or len(current_line) < 2:
        return current_board_line

    # Array that will get returned
    final_array = []

    # Gets every combination of the sum of two numbers in a row (e.g. [1,3,2] gives [4,5])
    line_combinations = []

    # Array that places the spaces one by one
    current_space = []

    # Array that contains all the spaces
    spaces = []

    # To separate the spaces
    is_counting = True

    for i in range(len(current_line)-1):
        line_combinations.append(current_line[i]+current_line[i+1])

    for i in current_board_line:
        if i == 'F' and is_counting:
            is_counting = False
            spaces.append(current_space[:])
            current_space.clear()

        elif is_counting:
            current_space.append(0)

        elif i != 'F':
            is_counting = True
            current_space.append(0)

    if len(current_space) > 0:
        spaces.append(current_space[:])

    # Only proceed if there can't be two sets of tiles in one space
    max_space = len(max(spaces, key=len))
    min_set = min(line_combinations) + 1

    if max_space >= min_set or len(current_line) != len(spaces):
        return current_board_line

    # Now proceed (filling overlapping tiles with 100% rate)
    for i in range(len(current_line)):
        for j in range(current_line[i]):
            spaces[i][j] += 1
            spaces[i][-j-1] += 1

    for i in spaces:
        for id_j, j in enumerate(i):
            if j == 2:
                i[id_j] = 'T'

            else:
                i[id_j] = 0

    # One-dimensional array of spaces
    clean_spaces = []
    for i in spaces:
        clean_spaces.extend(i)

    # Put the values back in the original array
    for id_i, i in enumerate(current_board_line):
        if i == 0:
            final_array.append(clean_spaces[0])
            clean_spaces.pop(0)

        elif i == 'T':
            final_array.append('T')
            clean_spaces.pop(0)

        else:
            final_array.append("F")

    return final_array


# Function that puts F's around blocks of T's that can't be longer (e.g. if 1 is the max, 0T0 becomes FTF)
def surroundBlocks(current_line, current_board_line):
    # Takes max value of line
    max_value = max(current_line)

    # Separate every block of tiles
    current_block = []
    blocks = []
    for i in current_board_line:
        if i == 'T':
            current_block.append(i)
        else:
            if len(current_block) > 0:
                blocks.append(current_block[:])
            current_block.clear()
            current_block.append(i)
            if len(current_block) > 0:
                blocks.append(current_block[:])
            current_block.clear()

    if len(current_block) > 0:
        blocks.append(current_block)

    # Surround blocks whenever possible
    for id_i, i in enumerate(blocks):
        if 'T' in i:
            if len(i) == max_value:
                if id_i > 0:
                    blocks[id_i-1] = 'F'
                if id_i < len(blocks) - 1:
                    blocks[id_i+1] = 'F'

    # Return final array
    final_array = []
    for i in blocks:
        final_array.extend(i)

    return final_array


# Function that fills a gap between two black tiles (e.g. with 3, 00T0T becomes 00TTT)
def joinTiles(current_line, current_board_line):
    # Board that we work with
    working_board = current_board_line[:]
    # Only proceed when there's only one number in the line and there's at least two tiles to join
    if len(current_line) == 1 and working_board.count('T') >= 2:
        # Fill the gap when true
        is_currently_filling = False

        for id_i, i in enumerate(working_board):
            if i == 'T' and is_currently_filling == False:
                is_currently_filling = True
            elif i == 0 and is_currently_filling:
                working_board[id_i] = 'T'
            elif i == 'T' and is_currently_filling and 'T' not in working_board[id_i + 1:]:
                is_currently_filling = False

        return working_board

    # Return the original board if there's more than one number in the line
    else:
        return current_board_line


# Function that completes the beginning (e.g. with 3, FTTT000000 becomes FTTTF00000)
def fillBeginning(current_line, current_board_line):
    # Return the original board if the line is done
    if 0 not in current_board_line:
        return current_board_line

    # Board that we'll work with
    working_board = current_board_line[:]

    # Used to compare later
    empty_part = []
    marked_part = []
    for i in range(current_line[0]):
        marked_part.append('T')
        empty_part.append(0)

    for i in range(2):
        for i in range(len(working_board) - current_line[0]):
            if 'F' not in working_board[i:i+current_line[0]] and 0 in working_board[i:i+current_line[0]]:
                break

            elif working_board[i:i+current_line[0]] == marked_part:
                working_board[i+current_line[0]] = 'F'
                break

        current_line.reverse()
        working_board.reverse()

    return working_board


# Function that puts F's when there's only one number and it can't go further (e.g. with [6], 0TTTTT0000 becomes 0TTTTT0FFF)
def crossReach(current_line, current_board_line):
    # Return the original board when there's no reason to proceed
    if 0 not in current_board_line or 'T' not in current_board_line:
        return current_board_line

    # Only proceed when there's only one number in the current line
    if len(current_line) > 1:
        return current_board_line

    else:
        # Board that we'll work with
        working_board = current_board_line[:]

        # Do it twice (forward and backwards)
        for i in range(2):
            # Subsection of the board
            sub_board = []

            for id_i, i in enumerate(working_board):
                if i == 'T':
                    sub_board.append(working_board[:id_i])
                    sub_board.append(working_board[id_i:id_i+current_line[0]])
                    sub_board.append(working_board[id_i+current_line[0]:])
                    break

            for id_i, i in enumerate(sub_board[1]):
                if i == 0:
                    sub_board[1][id_i] = 'X'

            working_board.clear()
            for i in sub_board:
                working_board.extend(i)

            working_board.reverse()

        # Put the F's and restaure the 0's
        for id_i, i in enumerate(working_board):
            if i == 0:
                working_board[id_i] = 'F'

            elif i == 'X':
                working_board[id_i] = 0

        return working_board


# Function that fills what's possible when there's only one space (e.g. with [2], FF000FFFFF becomes FF0T0FFFFF)
def fillOneSpace(current_line, current_board_line):
    # Return the original board when there's more than one number in the line or the line is full
    if len(current_line) > 1 or 0 not in current_board_line:
        return current_board_line

    # Make a default board that removes the T's
    unmarked_board = current_board_line[:]
    for id_i, i in enumerate(unmarked_board):
        if i == 'T':
            unmarked_board[id_i] = 0

    # To separate each part of the board line
    board_chunk = []

    # See how many empty spaces there are
    empty_counter = 0

    # Board that contains every chunk
    working_board = []

    # Clean (one-dimensional) version of the above board
    clean_working_board = []

    # Board that will get returned
    final_board = []

    for id_i, i in enumerate(unmarked_board[:-1]):
        board_chunk.append(i)
        if i != unmarked_board[id_i + 1]:
            working_board.append(board_chunk[:])
            board_chunk.clear()

    # Put the rest
    working_board.append(board_chunk)
    working_board.append(unmarked_board[-1:])

    for i in working_board:
        if 0 in i:
            empty_counter += 1

    # Only proceed if there's only one space
    if empty_counter != 1:
        return current_board_line
    else:
        # Place the numbers
        for i in working_board:
            if 0 not in i:
                continue
            else:
                for j in range(current_line[0]):
                    if i[j] != 0:
                        i[j] = 0
                    i[j] += 1
                    i[-j-1] += 1

    # Put the T's
    for i in working_board:
        if 1 not in i and 2 not in i:
            continue
        else:
            for id_j, j in enumerate(i):
                if j > 1:
                    i[id_j] = 'T'
                else:
                    i[id_j] = 0

    for i in working_board:
        clean_working_board.extend(i)

    for i in range(len(current_board_line)):
        if current_board_line[i] == 'T':
            final_board.append(current_board_line[i])
        else:
            final_board.append(clean_working_board[i])

    return final_board


# Function that fills an extremum that can be completed
def fillExtremum(current_line, current_board_line):
    # Board that we'll work with
    working_board = current_board_line[:]

    # Line that we'll work with
    working_line = current_line[:]

    # Board full of T's of the first number's length
    marked_board = []

    for i in range(2):
        for i in range(working_line[0]):
            marked_board.append('T')

        for i in range(len(working_board)):
            if working_board[i] == 0:
                break
            elif working_board[i] == 'T':
                working_board[i:i+working_line[0]] = marked_board
                if i + working_line[0] < len(working_board):
                    working_board[i+working_line[0]] = 'F'
                break

        marked_board.clear()
        working_board.reverse()
        working_line.reverse()

    return working_board


# Function that completes the beginning when possible (e.g. with [2], 0TF0000000 becomes TTF0000000)
def completeBeginning(current_line, current_board_line):
    # Working board
    working_board = []

    # Copy of the original board (Will be modified later)
    original_board = current_board_line[:]

    # Copy of current line
    working_line = current_line[:]

    # Do forward and backwards
    for i in range(2):
        for i in original_board:
            if i == 'F':
                break
            else:
                working_board.append(i)

        if len(working_board) == working_line[0] and 'T' in working_board:
            for id_i, i in enumerate(working_board):
                original_board[id_i] = 'T'

        original_board.reverse()
        working_line.reverse()
        working_board.clear()

    return original_board


# Function that fills the largest number if there's only one space for it (e.g. with [2, 4], 00FF00T0F0 becomes 00FFTTTTF0)
def fillLargest(current_line, current_board_line):
    # Max value in line
    max_value = max(current_line)

    # Copy of the original board
    original_board = current_board_line[:]

    # Working board
    working_board = []

    # Unsegmented working board
    clean_working_board = []

    # Board that will get returned
    final_board = []

    # Individual spaces
    space = []

    # Spaces length (e.g. for [[0, 0], [], [0, 0, 'T', 0], [0]] we get [2, 0, 4, 1])
    spaces_length = []

    # Place the spaces in the working board
    for i in original_board:
        if i == 'F':
            working_board.append(space[:])
            space.clear()
        else:
            space.append(i)

    working_board.append(space[:])

    # Put the values in spaces_length
    for i in working_board:
        spaces_length.append(len(i))

    if current_line.count(max_value) == spaces_length.count(max_value) and max_value == max(spaces_length):
        for i in working_board:
            if len(i) == max_value:
                for id_j, j in enumerate(i):
                    i[id_j] = 'T'
    else:
        return current_board_line

    for i in working_board:
        clean_working_board.extend(i)

    for i in original_board:
        if i == 'F':
            final_board.append('F')
        else:
            final_board.append(clean_working_board[0])
            clean_working_board.pop(0)

    return final_board


# Function that places F's after the largest if it's put as the last (e.g. with [1, 2] 00FTTFF000 becomes 00FTTFFFFF)
def stopAfterLastMax(current_line, current_board_line):
    # Board that we'll work with
    working_board = current_board_line[:]

    # Copy of the current line
    working_line = current_line[:]

    # Individual spaces
    current_space = []

    # Fully marked array with a length of max number in line
    marked_array = []
    for i in range(max(working_line)):
        marked_array.append('T')

    # Put T's in an array
    marked_tiles = []
    for i in current_board_line:
        if i == 'T':
            current_space.append(i)
        else:
            if len(current_space) > 0:
                marked_tiles.append(current_space[:])
                current_space.clear()

    for i in range(2):
        if marked_tiles.count(marked_array) == working_line.count(max(working_line)) and working_line[-1] == max(working_line):
            for id_i, i in enumerate(working_board):
                if working_board[-id_i - 1] == 'T':
                    break
                else:
                    working_board[-id_i - 1] = 'F'

        working_line.reverse()
        working_board.reverse()

    return working_board


# Function that fills the beginning of a line when the first number is done (e.g. with [1, 4], F0FTFTT000 becomes FFFTFTT000)
def fillBeforeBeginning(current_line, current_board_line):
    # Board that we'll work with
    working_board = current_board_line[:]

    # Board that we'll try to find (will be filled later)
    theoretical_board = []

    # Board full of F's of same length as the board above (will be filled later)
    crossed_board = []

    # Working line
    working_line = current_line[:]

    if len(working_line) > 1:
        # Do forward and backwards
        for n in range(2):
            if working_line[0] == working_line[1]:
                # Clear everything and do backwards
                working_line.reverse()
                working_board.reverse()
                theoretical_board.clear()
                crossed_board.clear()
                continue
            else:
                # Fill the theoretical board
                theoretical_board.append('F')
                for i in range(working_line[0]):
                    theoretical_board.append('T')
                theoretical_board.append('F')

                # Fill the crossed board
                for i in range(len(theoretical_board)):
                    crossed_board.append('F')

                for i in range(len(working_board) - len(theoretical_board) + 1):
                    if working_board[i:i + len(theoretical_board)] == theoretical_board:
                        for i in range(len(working_board[0:i])):
                            working_board[i] = 'F'
                    elif working_board[i] == 'T':
                        break

            # Clear everything and do backwards
            working_line.reverse()
            working_board.reverse()
            theoretical_board.clear()
            crossed_board.clear()

    return working_board


# Relative equivalent of doFullLine (e.g. with [4, 1, 1] FTTTTF000F becomes FTTTTFTFTF)
def relFullLine(current_line, current_board_line):
    # Board that we'll work with
    working_board = current_board_line[:]

    # Line that we'll work with
    working_line = current_line[:]

    # Slice to remove the F's at the extremums
    crossed_beginning = 0
    crossed_end = len(working_board) - 1
    while working_board[crossed_beginning] == 'F':
        crossed_beginning += 1

    while working_board[crossed_end] == 'F':
        crossed_end -= 1

    sliced_board = working_board[crossed_beginning:crossed_end + 1]

    # Board that will be filled later
    changed_slice = []

    # Only proceed when possible
    if len(sliced_board) == sum(current_line) + len(current_line) - 1 and 'T' not in current_board_line:
        for i in range(len(current_line)-1):
            if i % 2 == 0:
                working_line.insert(i+1, 0)
    else:
        return current_board_line

    # Fill the board
    for i in working_line:
        if i == 0:
            changed_slice.append('F')
        else:
            for j in range(i):
                changed_slice.append('T')

    # Put the changed board back in the working board
    working_board[crossed_beginning:crossed_end + 1] = changed_slice

    return working_board


# Function that puts F's when T's would have created an impossible line (e.g. with [1, 4] F0FT0TTT0F tries F0FTTTTT0F but becomes F0FTFTTT0F because the line contains 5 T's and 4 is the max)
def removeImpossible(current_line, current_board_line):
    # Board that we'll work with
    working_board = current_board_line[:]

    # Put the T's in a list and verify
    marked_array = []
    current_space = []

    for id_i, i in enumerate(working_board):
        # Put a T in the board at the desired index
        working_board[id_i] = 'T'

        for j in working_board:
            if j == 'T':
                current_space.append('T')
            elif len(current_space) > 0:
                marked_array.append(current_space[:])
                current_space.clear()

        # Put the last one if there's some left
        if len(current_space) > 0:
            marked_array.append(current_space[:])
            current_space.clear()

        # Change the board if needed
        if len(marked_array) > 0:
            if len(max(marked_array, key=len)) > max(current_line):
                working_board[id_i] = 'F'
            else:
                working_board[id_i] = current_board_line[id_i]
        else:
            working_board[id_i] = current_board_line[id_i]

        # Reset before looping
        marked_array.clear()
        current_space.clear()

    return working_board


# Function that checks overlapping tiles for several numbers in a row (e.g. for [2, 2] 000000 becomes 0T00T0)
def multiOverlap(current_line, current_board_line):
    # Trim the beginning of the board
    first_not_crossed = 0
    for i in range(len(current_board_line)):
        if i != 'F':
            first_not_crossed = i
            break

    # Trim the end of the board
    last_not_crossed = 0
    for i in range(len(current_board_line)):
        if 'T' not in current_board_line[i:] and 0 not in current_board_line[i:]:
            last_not_crossed = i
            break

    # Original working board
    original_working_board = current_board_line[first_not_crossed:last_not_crossed]

    # Board that we'll work with (empty version of the original one)
    working_board = []

    for i in original_working_board:
        working_board.append(0)

    # Don't continue if there's any F in the working board or if the whole line is already done
    if 'F' in working_board or 0 not in current_board_line:
        return current_board_line

    # Smallest board with the current line numbers
    smallest_board = []

    # Final board that will be put in the returned board
    final_board = []

    # Fill from the beginning
    for i in current_line:
        for j in range(i):
            smallest_board.append(1)
        smallest_board.append(0)

    # Remove the last zero
    smallest_board.pop(-1)

    # Highest amount of times the smallest board can be put in the working board
    highest_amount = len(working_board) - len(smallest_board) + 1

    # Place the numbers in the working board
    for i in range(highest_amount):
        for j in range(len(smallest_board)):
            working_board[i + j] += smallest_board[j]

    # Place the numbers in the final board
    for i in range(len(working_board)):
        if working_board[i] != highest_amount:
            final_board.append(original_working_board[i])
        else:
            final_board.append('T')

    # Board that will get returned
    returned_board = current_board_line[:]

    # Put the final board in the returned board
    returned_board[first_not_crossed:last_not_crossed] = final_board

    # Return that board
    return returned_board


# Function that puts F's in the beginning if needed (e.g. with [2], 0F00000000 becomes FF00000000)
def crossBeginning(current_line, current_board_line):
    # Board that we'll work with
    working_board = current_board_line[:]

    # Line that we'll work with
    working_line = current_line[:]

    # Check if there's place at the beginning of the board for the first number
    for n in range(2):
        if 'F' in working_board[:working_line[0]]:
            # Place the F tiles
            for id_i, i in enumerate(working_board[:working_line[0]]):
                if i != 'F':
                    working_board[id_i] = 'F'
                else:
                    break

        # Do it a second time from the end
        working_line.reverse()
        working_board.reverse()

    # Return the working board
    return working_board


# Function that considers that when there's two spaces and the whole thing doesn't fit in one, then the first number is in the first space and the last number is in the last space (e.g. for [3, 1, 1, 1, 1] and 00000F00T000000, the 3 goes in the first space and returns 00T00F00T000000)
def separateSpaces(current_line, current_board_line):
    # Only keep going if the line has at least two numbers
    if len(current_line) < 2:
        return current_board_line

    # Get the variables
    spaces = getSpaces(current_board_line)
    min_tiles_sum = getMinTiles(current_line)

    # Largest space's length
    max_space_len = len(max(spaces, key=len))

    # Only proceed if there's two spaces and not everything can fit in one space
    if len(spaces) != 2 or min_tiles_sum <= max_space_len:
        return current_board_line

    # Fill the spaces
    spaces[0] = fillOverlapping(current_line[0:1], spaces[0])
    spaces[1] = fillOverlapping(current_line[-1:], spaces[1])

    spaces[0] = surroundBlocks(current_line[0:-1], spaces[0])
    spaces[1] = surroundBlocks(current_line[1:], spaces[1])

    # Board that will get returned
    working_board = putSpacesBack(spaces, current_board_line)

    return working_board


# Function that fills spaces where nothing can fit with F's
def fillImpossibleSpaces(current_line, current_board_line):
    spaces = getSpaces(current_board_line)

    # Only keep going if there's at least two spaces and the line isn't already done
    if len(spaces) < 2 or 0 not in current_board_line:
        return current_board_line

    # Just filling the easy empty spaces
    for i in spaces:
        if len(i) < min(current_line):
            for id_j, j in enumerate(i):
                i[id_j] = 'F'

    # Do the trickier ones
    # Index of the first number in current_line that can fit in the smallest space
    first_fit = 0
    for id_i, i in enumerate(current_line):
        if i <= len(min(spaces, key=len)):
            first_fit = id_i
            break

    # Line that we'll work with
    working_line = current_line[:first_fit]

    # Sliced working board
    sliced_board = []

    # Board until the first smallest space
    for i in spaces:
        if i == min(spaces, key=len):
            break
        else:
            sliced_board.extend(i)
            sliced_board.extend('F')

    # Remove the F at the end
    if len(sliced_board) > 0:
        sliced_board = sliced_board[:-1]

    # Count how many numbers can fit
    fit_counter = 0

    # Fill the first empty space if the beginning can't fit
    for i in working_line:
        for id_j, j in enumerate(sliced_board):
            if 'F' not in sliced_board[id_j:id_j + i]:
                fit_counter += 1
                for id_k, k in enumerate(sliced_board[:id_j + 1]):
                    sliced_board[id_k] = 'F'

    if fit_counter < len(working_line):
        for i in spaces:
            # Put F's in the space if it has to be F's
            if i == min(spaces, key=len):
                for id_j, j in enumerate(i):
                    i[id_j] = 'F'

    # Board that will get returned
    final_board = putSpacesBack(spaces, current_board_line)

    return final_board


# Function that puts an F if everything from before is already filled (e.g. for [1, 3, 1, 1, 3] TFFFTTTFT00FTTT becomes TFFFTTTFTF0FTTT)
def crossAfterComplete(current_line, current_board_line):
    # Board that we'll work with
    working_board = []

    # Index where the F will be put
    cross_index = 0

    for id_i, i in enumerate(current_board_line):
        if i == 0:
            working_board = current_board_line[:id_i]
            cross_index = id_i
            break

    # Only keep going if necessary and possible
    if 0 not in current_board_line or len(working_board) == 0 or working_board[-1] == 'F':
        return current_board_line

    # Count the spaces in the working board
    spaces = getSpaces(working_board)

    # List that has the length of each space
    spaces_length = []
    for i in spaces:
        spaces_length.append(len(i))

    # Current line up until now
    working_line = current_line[:len(spaces)]

    # Put the F in the board that will get returned
    final_board = current_board_line[:]
    if spaces_length == working_line:
        final_board[cross_index] = 'F'

    return final_board


# Function that detects when each number goes in each space and completes what it can (e.g. with [4, 3] 00000000TF00TT0 will return...)
def matchSpaces(current_line, current_board_line):
    spaces = getSpaces(current_board_line)
    # Return the original board if the line is completed or if there aren't as many spaces as numbers on the line
    if 0 not in current_board_line or len(current_line) != len(spaces):
        return current_board_line

    # Check if there's at least a T in each space, return the original board otherwise
    for i in spaces:
        if 'T' not in i:
            return current_board_line

    # Now complete what we can on the line
    for id_i, i in enumerate(spaces):
        spaces[id_i] = joinTiles(current_line[id_i:id_i + 1], spaces[id_i])
        spaces[id_i] = extendExtremum(
            current_line[id_i:id_i + 1], spaces[id_i])
        spaces[id_i] = fillExtremum(current_line[id_i:id_i + 1], spaces[id_i])
        spaces[id_i] = crossReach(current_line[id_i:id_i + 1], spaces[id_i])

    # Put the spaces in a board that will get returned
    working_board = putSpacesBack(spaces, current_board_line)

    return working_board


# Function that finds when two numbers can't exist for one or more tiles, then puts an F in those tiles (e.g. for 7, 5 0TTTTTT000TTTT0 becomes 0TTTTTT0F0TTTT0)
def numberSeparation(current_line, current_board_line):
    # Make sure that the two lines correspond to both numbers instead of just one that hasn't been completed
    # For that, we first delimit the extremum of T's
    first_marked = 0
    for id_i, i in enumerate(current_board_line):
        if i == 'T':
            first_marked = id_i
            break

    last_marked = 0
    for id_i, i in enumerate(current_board_line):
        if 'T' not in current_board_line[id_i:]:
            last_marked = id_i
            break

    # Board that we'll work with
    working_board = current_board_line[first_marked:last_marked]

    # Now, we only proceed if all of that is long enough to not just be parts of only one of the two numbers and if there are exactly two numbres in the current line
    if len(working_board) <= max(current_line) or len(current_line) != 2:
        return current_board_line

    # Put the F's where they can be
    for id_i, i in enumerate(working_board[current_line[0]:len(working_board) - current_line[1]]):
        working_board[current_line[0] + id_i] = 'F'

    # Board that will get returned
    final_board = current_board_line[:]
    for id_i, i in enumerate(final_board[first_marked:last_marked]):
        final_board[first_marked + id_i] = working_board[id_i]

    return final_board


# Function that finds a part of the line and completes what comes before when possible (e.g. with [1, 1, 2, 3] 0000TT000000000 becomes TFTFTT000000000)
def completeBefore(current_line, current_board_line):
    # Only proceed if the line hasn't been completed
    if 0 not in current_board_line:
        return current_board_line

    # Find the first marked tiles
    # First of those tiles
    first_tile = 0
    for id_i, i in enumerate(current_board_line):
        if i == 'T':
            first_tile = id_i
            break

    # Stop here if first_tile is the first tile of the line
    if first_tile == 0:
        return current_board_line

    # Last of those tiles
    last_tile = 0
    for id_i, i in enumerate(current_board_line[first_tile:]):
        if i != 'T':
            last_tile = first_tile + id_i
            break
        elif id_i == len(current_board_line[first_tile:]) - 1:
            last_tile = first_tile + id_i + 1

    # List for those tiles
    first_tiles = current_board_line[first_tile:last_tile]

    # Line until the first marked tiles can appear
    working_line = []

    # Find he earliest where this can appear
    for id_i, i in enumerate(current_line[1:]):
        if i >= len(first_tiles):
            working_line = current_line[:id_i]

    # Least amount of tiles that the beginning can take
    beginning_min = sum(working_line) + len(working_line)

    # Beginning of the board that will get updated
    updated_board = []
    for i in range(first_tile):
        updated_board.append(0)

    # If there's just enough place to put the first tiles, place them, otherwise return the original board
    if first_tile == beginning_min:
        updated_board[:-1] = relFullLine(working_line, updated_board[:-1])
    else:
        return current_board_line

    # Place an F at the end
    updated_board[-1] = 'F'

    # Board that will get returned
    final_board = current_board_line[:]
    final_board[:first_tile] = updated_board

    return final_board


# Function that puts F's at the beginning when the first number can't be there
def crossBeforeFirst(current_line, current_board_line):
    # Board that we'll work with
    working_board = current_board_line[:current_line[0] * 2]

    # Find the index of the first T in the current line
    first_marked = 0

    for id_i, i in enumerate(working_board):
        if i == 'T':
            first_marked = id_i
            break

    # Find the index of the last T in this segment
    last_marked = 0
    for id_i, i in enumerate(working_board[first_marked:]):
        if i != 'T':
            last_marked = id_i + first_marked
            break

    # Only proceed if either isn't 0
    if first_marked == 0 or last_marked == 0:
        return current_board_line

    # Last possible index to place an F
    last_cross = last_marked - current_line[0] - 1

    # Board that will get returned
    final_board = current_board_line[:]

    # Place the F's
    while last_cross >= 0:
        final_board[last_cross] = 'F'
        last_cross -= 1

    return final_board


# Function that removes the largest number if it's already done, and repeats the function
# Note : it will also remove the first and / or last if they can't be elsewhere
def removeLargest(current_line, current_board_line):
    # Final board
    final_board = []

    working_array = current_board_line[:]
    working_line = current_line[:]
    black_tile_groups = []

    # Stop the while when it changes nothing
    previous_line = []

    # Check the first and last
    marked_area = []
    empty_area = []
    checked_area = []

    while previous_line != working_line:
        previous_line = working_line[:]
        for i in range(2):
            # Where the marked cases are located
            marked_tile_spot = 0

            # Will become true if the part in question exists in the board line
            is_marked_present = False

            for i in range(working_line[0]):
                marked_area.append('T')
                empty_area.append(0)

            # Find if the searched part is here
            for id_i, i in enumerate(working_array):
                if working_array[id_i:id_i+working_line[0]] == marked_area:
                    checked_area = working_array[:id_i]
                    marked_tile_spot = id_i
                    is_marked_present = True
                    break

            if set(empty_area).issubset(checked_area) == False and is_marked_present and len(working_line) >= 2:
                for id_i, i in enumerate(working_array[marked_tile_spot:marked_tile_spot + working_line[0]]):
                    working_array[id_i + marked_tile_spot] = 'F'

                working_line.pop(0)

            working_array.reverse()
            working_line.reverse()

            marked_area.clear()
            empty_area.clear()
            checked_area.clear()

    # Remove everything that we can
    while previous_line != working_line:
        previous_line = working_line[:]
        black_tiles_counter = 0
        for i in current_board_line:
            if i == 'T':
                black_tiles_counter += 1
            else:
                if black_tiles_counter > 0:
                    black_tile_groups.append(black_tiles_counter)
                    black_tiles_counter = 0

        # Include the last one
        if black_tiles_counter > 0:
            black_tile_groups.append(black_tiles_counter)

        # Return the original board if there's no black squares
        if len(black_tile_groups) == 0:
            return current_board_line

        # Only remove if max value appears as much on the board as it exists in the line
        if max(working_line) == max(black_tile_groups):
            if working_line.count(max(working_line)) == black_tile_groups.count(max(black_tile_groups)):
                for i in range(len(working_array) - max(working_line) + 1):
                    current_section = working_array[i:i+max(working_line)]
                    if 'T' in current_section and 'F' not in current_section and 0 not in current_section:
                        # Mark unnecessary tiles with 'F'
                        for i in range(i, i+max(working_line)):
                            working_array[i] = 'F'
                        working_line.remove(max(working_line))
                        if len(working_line) < 1:
                            return current_board_line

    # Return the original board line if the working line is the same as the default line
    if working_line == current_line:
        return current_board_line

    # Do all relative functions otherwise
    working_array = doCompleteLine(working_line, working_array)
    working_array = doCompleteBlackSquares(working_line, working_array)
    working_array = reduceSingularNumbers(working_line, working_array)
    working_array.reverse()
    working_array = reduceSingularNumbers(working_line, working_array)
    working_array.reverse()
    working_array = tileCannotFit(working_line, working_array)
    working_array = extremumCompletion(working_line, working_array)
    working_array = fillOverlapping(working_line, working_array)
    working_array = checkRange(working_line, working_array)
    working_array = completeLimitedLine(
        working_line, working_array, len(working_array))
    working_array = extendExtremum(working_line, working_array)
    working_array = fillSpaces(working_line, working_array)
    working_array = surroundBlocks(working_line, working_array)
    working_array = joinTiles(working_line, working_array)
    working_array = fillBeginning(working_line, working_array)
    working_array = crossReach(working_line, working_array)
    working_array = fillOneSpace(working_line, working_array)
    working_array = fillExtremum(working_line, working_array)
    working_array = completeBeginning(working_line, working_array)
    working_array = fillLargest(working_line, working_array)
    working_array = stopAfterLastMax(working_line, working_array)
    working_array = fillBeforeBeginning(working_line, working_array)
    working_array = relFullLine(working_line, working_array)
    working_array = removeImpossible(working_line, working_array)
    working_array = multiOverlap(working_line, working_array)
    working_array = crossBeginning(working_line, working_array)
    working_array = separateSpaces(working_line, working_array)
    working_array = fillImpossibleSpaces(working_line, working_array)
    working_array = crossAfterComplete(working_line, working_array)
    working_array = matchSpaces(working_line, working_array)
    working_array = numberSeparation(working_line, working_array)
    working_array = completeBefore(working_line, working_array)
    working_array = crossBeforeFirst(working_line, working_array)

    for i in range(len(current_board_line)):
        if current_board_line[i] == 'T':
            final_board.append('T')
        else:
            final_board.append(working_array[i])

    return final_board
