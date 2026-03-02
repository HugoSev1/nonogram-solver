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
test_board = []
screen = pygame.display.set_mode((640, 640))
screen.fill((42, 43, 35))
for i in range(row_amount):
    test_board.append([])
    for j in range(row_amount):
        test_board[i].append(0)

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

# Do the lines that have only one possibility
for i in range(row_amount):
    current_line = nonoSolvFunc.doFullLine(row_amount, column_digits[i], [])
    nonoSolvFunc.fillColumn(current_line, game_board, i)
    current_line = nonoSolvFunc.doFullLine(row_amount, row_digits[i], [])
    nonoSolvFunc.fillRow(current_line, game_board, i)

# Draw the tiles
for i in range(row_amount):
    for j in range(row_amount):
        if game_board[j][i] == "T":
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
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
