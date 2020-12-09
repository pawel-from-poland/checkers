import pygame


class Checker:
    def __init__(self, win, color, row, col):
        self.win = win
        self.win_width, self.win_height = pygame.display.get_surface().get_size()
        self.square_width, self.square_height = self.win_width // 8, self.win_height // 8
        self.color = color
        self.row = row
        self.col = col
        self.draw()

    def draw(self):
        pygame.draw.circle(self.win, self.color,
                           (self.col * self.square_width + self.square_width // 2,
                            self.row * self.square_height + self.square_height // 2),
                           self.square_height // 2 - 10)
