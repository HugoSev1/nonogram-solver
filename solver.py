import nonoSolvFunc
import cv2
import os

# Getting the coordinates of the blue box around the puzzle
puzzle_coords = nonoSolvFunc.getPuzzleCoords()

# Get the columns part from here
column_coords = nonoSolvFunc.getColumnImage(puzzle_coords)

# Read the digits from the columns
column_digits = nonoSolvFunc.extractNumbers()
print(column_digits)