import nonoSolvFunc
import cv2
import os

# Coordinates to make the image from the screen
puzzle_coords = nonoSolvFunc.getPuzzleCoords()
column_coords = nonoSolvFunc.getColumnImage(puzzle_coords)

# Import digit templates from 1 to 9 (0 can't exist in a Nonogram, so we don't need a template for it)
digit_templates = {}
for file in os.listdir("./templates"):
    if file.endswith(".png") and file[0].isdigit():
        digit = file.split(".")[0]
        digit_templates[digit] = cv2.imread(file, 0)

column_digits = nonoSolvFunc.extractNumbers()
print(column_digits)