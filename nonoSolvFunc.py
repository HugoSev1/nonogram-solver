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
    color = (142, 135, 111)
    while scrsh.getpixel((xColumn, yColumn)) != color:
        yColumn += 1
    color = (42,43,35)
    while scrsh.getpixel((xColumn, yColumn)) != color:
        xColumn += 1
    column_coords.append(xColumn)
    column_coords.append(yColumn)
    
    column_img = ImageGrab.grab(bbox=(column_coords[0],column_coords[1],column_coords[2],column_coords[3]))
    column_img.save("digits-test.png")
    return column_coords


# Function that extracts the numbers shown on the Nonogram
def extractNumbers():
    extractingArray = []
    # Divides the image in 5 chunks, and save them
    img = cv2.imread("digits-test.png")
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
                digits.append((best_match, x))
        digits.sort(key=lambda x: x[1])
        result = [d[0] for d in digits]
        result.reverse()
        extractingArray.append(result)
    return extractingArray
