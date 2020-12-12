import pygame
from .constants import WHITE, RED, BLACK, GREEN
from .checker import Checker


class Board:
    def __init__(self, win, width, height, rows, cols):
        self.width = width  # width of the window
        self.height = height  # height of the window
        self.rows = rows  # number of rows
        self.cols = cols  # number of columns
        self.win = win  # pygame window
        self.square_width, self.square_height = self.width / \
            self.cols, self.height / self.rows  # width and height of square

        # 'white' - white checker, 'black' - black checker, 0 - no checker
        self.board = [([('white' if j > 4 else 'black') if i % 2 == 1 else 0 for i in range(8)] if j % 2 == 0 else [
            ('white' if j > 4 else 'black') if i % 2 == 0 else 0 for i in range(8)]) if j < 3 or j > 4 else [0 for _ in range(8)] for j in range(8)]
        self.turn = 'white'  # who's turn is it?
        self.selected = False  # whether checker's selected

        self.__draw_board()  # drawing board
        self.__draw_checkers()  # drawing checkers

    def __draw_board(self):  # method for drawing board
        self.win.fill(BLACK)  # filling whole window with black color
        for col in range(self.cols):
            for row in range(self.rows):
                if col % 2 == row % 2:  # drawing white square if for example row == 4, col == 2
                    # window, color, (x, y, width, height)
                    pygame.draw.rect(
                        self.win, WHITE,
                        (col*self.square_width, row*self.square_height,
                         self.square_width, self.square_height))

    def __draw_checkers(self):  # method for drawing checkers
        for e1, l in enumerate(self.board):
            for e2, checker in enumerate(l):
                if checker != 0:  # there's a checker
                    # symbol of checker on self.board
                    __color = self.board[e1][e2]
                    color = WHITE if __color == 'white' else RED  # color of checker
                    Checker(self.win, color, e1, e2)  # drawing checker

    def __draw_moves(self, valid_moves):  # method for drawing the moves
        self.__draw_board()  # drawing board
        self.__draw_checkers()  # drawing checkers
        for move in valid_moves:
            if move != [] and move != None:  # there's a move
                # window, color, (x, y), radius
                pygame.draw.circle(self.win, GREEN,
                                   (move[1] * self.square_width + self.square_width // 2,
                                    move[0] * self.square_height + self.square_height // 2),
                                   self.square_height // 5)

    def get_selected_square(self, x, y):  # return row and col of mouse
        row = int(y / self.square_height)
        col = int(x / self.square_width)
        return (row, col)

    # sets self.selected and returns item
    def get_selected_square_item(self, row, col):
        # sets it to True if there's a checker on clicked square
        self.selected = True if self.turn in str(self.board[
            row][col]) else False
        return self.board[row][col]  # returns item on selected row and col

    # returns move on right side of checker
    def __traverse_right(self, item, row, col, next_=False):
        if self.turn in str(item) or next_:  # here valid checker's selected
            right = [row - 1, col +
                     1] if self.turn == 'white' else [row + 1, col + 1]  # selects right item of the ckecker
            try:
                if self.board[right[0]][right[1]] == 0:  # here left item is empty
                    if next_ and self.turn not in str(self.board[right[0] + (-1 if self.turn == 'white' else 1)][right[1] + 1]) and self.board[right[0] + (-1 if self.turn == 'white' else 1)][right[1] + 1]:
                        right_moves, left_moves = self.__traverse_right(self.board[right[0] + (-1 if self.turn == 'white' else 1)][right[1] + 1], right[0] + (-1 if self.turn == 'white' else 1), right[1] + 1), self.__traverse_left(
                            self.board[right[0] + (-1 if self.turn == 'white' else 1)][right[1] + 1], right[0] + (-1 if self.turn == 'white' else 1), right[1] + 1)
                        return right + (right_moves + left_moves if right_moves and left_moves else (right_moves if right_moves else (left_moves if left_moves else right)))
                    return right  # returns right item of the ckecker
                # searching for further moves
                elif self.board[right[0]][right[1]] != self.turn:
                    return self.__traverse_right(self.board[right[0]][right[1]], right[0], right[1], True)

            except IndexError:  # there's no right item coz it's outta the board
                return  # escapes the function

    # same as __traverse_right() but on left side lol
    def __traverse_left(self, item, row, col, next_=False):
        if self.turn in str(item) or next_:
            left = [row - 1, col -
                    1] if self.turn == 'white' else [row + 1, col - 1]
            try:
                if self.board[left[0]][left[1]] == 0:
                    if next_ and self.turn not in str(self.board[left[0] + (-1 if self.turn == 'white' else 1)][left[1] - 1]) and self.board[left[0] + (-1 if self.turn == 'white' else 1)][left[1] - 1]:
                        right_moves, left_moves = self.__traverse_right(self.board[left[0] + (-1 if self.turn == 'white' else 1)][left[1] - 1], left[0] + (-1 if self.turn == 'white' else 1), left[1] - 1), self.__traverse_left(
                            self.board[left[0] + (-1 if self.turn == 'white' else 1)][left[1] - 1], left[0] + (-1 if self.turn == 'white' else 1), left[1] - 1)
                        return right_moves + left_moves + left if right_moves and left_moves else (left_moves + left if left_moves else (right_moves + left if right_moves else left))
                    return left
                # searching for further moves
                elif self.board[left[0]][left[1]] != self.turn and not next_:
                    return self.__traverse_left(self.board[left[0]][left[1]], left[0], left[1], True)
            except IndexError:
                return

    def get_valid_moves(self, item, row, col):  # gets checker's valid moves
        valid_moves = [self.__traverse_right(
            item, row, col), self.__traverse_left(item, row, col)]  # valid moves of the ckecker
        self.__draw_moves(valid_moves)  # draws moves
        return valid_moves

    def move(self, selected_row, selected_col, new_row, new_col, valid_moves):
        self.selected = False  # nothing's selected now
        if valid_moves:  # there are valid moves of the ckecker
            new_valid_moves = []
            for move in valid_moves:
                if move and len(move) >= 2:
                    new_moves = [[move[x], move[x + 1]]
                                 for x in range(0, len(move), 2)]

                    for new_move in new_moves:
                        new_valid_moves.append(new_move)

            if [new_row, new_col] in new_valid_moves:  # there move chosen by player is valid
                self.turn = 'white' if self.turn == 'black' else 'black'  # switches self.turn
                self.board[selected_row][selected_col], self.board[new_row][
                    new_col] = self.board[new_row][new_col], self.board[selected_row][selected_col]  # switches two selected items
                self.__draw_board()  # draws board
                self.__draw_checkers()  # draws checkers
