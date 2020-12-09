import pygame
from checkers.constants import *
from checkers.board import Board

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Checkers')


def main():
    clock = pygame.time.Clock()

    b = Board(WIN, WIDTH, HEIGHT, ROWS, COLS)  # drawing board and checkers

    run = True
    while run:
        clock.tick(FPS)  # running at 60 FPS

        # checking if user did anything
        for event in pygame.event.get():
            # user closed window, breaking the loop
            run = False if event.type == pygame.QUIT else True
            if event.type == pygame.MOUSEBUTTONDOWN:  # user clicked
                if not b.selected:  # checking if a checker isn't already selected
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    global row, col, valid_moves  # they will be used in else statement
                    # getting row and col of the selected square
                    row, col = b.get_selected_square(mouse_x, mouse_y)
                    # checking what's in the selected square
                    item = b.get_selected_square_item(row, col)
                    valid_moves = b.get_valid_moves(
                        item, row, col)  # getting valid moves
                else:  # here checker is selected already
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    b.move(row, col, *b.get_selected_square(mouse_x,
                                                            mouse_y), valid_moves)  # YAY! Used an unpacking operator!

        pygame.display.update()  # updating all changes onto the screen

    pygame.quit()


main()
