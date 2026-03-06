import pyautogui
from PIL import ImageGrab
import cv2

# Display an image (for debugging purposes)


def showImg(img):
    cv2.imshow("Image", img)
    cv2.waitKey()

# Function that returns the coordinates of the area to work with inside of the blue box


def getPuzzleCoords():
    puzzle_coords = []
    # Getting the top left coordinates
    color = (133, 163, 224)
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
    for x in range(x1+1, 1500):
        if scrsh.getpixel((x, y1+1)) == color:
            puzzle_coords.append(x)
            break

    for y in range(y1+1, 1000):
        if scrsh.getpixel((x1+1, y)) == color:
            puzzle_coords.append(y)
            break

    x2 = puzzle_coords[2]
    y2 = puzzle_coords[3]
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
    color = (42, 43, 35)
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
    color = (42, 43, 35)
    while scrsh.getpixel((xColumn, yColumn)) != color:
        yColumn += 1
    row_coords.append(xColumn)
    row_coords.append(yColumn)

    row_img = ImageGrab.grab(
        bbox=(row_coords[0], row_coords[1], row_coords[2], row_coords[3]))
    row_img.save("row-img.png")
    return row_coords


# Function that extracts the numbers shown on the Nonogram
def extractColumnNumbers():
    extractingArray = []
    # Divides the image in 5 chunks
    img = cv2.imread("column-img.png")
    h, w, c, = img.shape
    n_chunks = 5
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

            for digit in range(1, 5):
                template = cv2.imread(f"templates\\{digit}.png", 0)
                _, template = cv2.threshold(
                    template, 150, 255, cv2.THRESH_BINARY_INV)
                template = cv2.resize(template, (50, 50))
                score = cv2.matchTemplate(
                    roi, template, cv2.TM_CCOEFF_NORMED)[0][0]

                if (score > best_score):
                    best_score = score
                    best_match = digit

            if (best_score > 0.7):
                digits.append((best_match, y))
        digits.sort(key=lambda x: x[1])
        result = [d[0] for d in digits]
        extractingArray.append(result)
    return extractingArray


# Function that extracts the numbers shown on the Nonogram (but for the rows this time)
def extractRowNumbers():
    extractingArray = []
    # Divides the image in 5 chunks
    img = cv2.imread("row-img.png")
    h, w, c, = img.shape
    n_chunks = 5
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

            for digit in range(1, 5):
                template = cv2.imread(f"templates\\{digit}.png", 0)
                _, template = cv2.threshold(
                    template, 150, 255, cv2.THRESH_BINARY_INV)
                template = cv2.resize(template, (50, 50))
                score = cv2.matchTemplate(
                    roi, template, cv2.TM_CCOEFF_NORMED)[0][0]

                if (score > best_score):
                    best_score = score
                    best_match = digit

            if (best_score > 0.7):
                digits.append((best_match, x))
        digits.sort(key=lambda x: x[1])
        result = [d[0] for d in digits]
        extractingArray.append(result)
    return extractingArray


# The next functions will be to solve the puzzle (In the arrays, "T" refers to a tile that has to be checked, and "F" to a tile that has to be unchecked)

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

    return working_array
