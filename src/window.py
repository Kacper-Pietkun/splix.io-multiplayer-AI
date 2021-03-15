import pygame


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.surface = pygame.Surface((width, height))

    def print_window(self, board, players):
        # draw all tiles
        for i in range(0, board.width):
            for j in range(0, board.height):
                pygame.draw.rect(self.surface, board.tiles[i][j].color,
                                 (i * self.width / board.width,             # position x
                                  j * self.height / board.height,           # position y
                                  self.width / board.width,                 # width
                                  self.height / board.height))              # height
        # draw all players
        for i in range(0, len(players)):
            pygame.draw.rect(self.surface, players[i].player_color,
                             (players[i].x * self.width / board.width,      # position x
                              players[i].y * self.height / board.height,    # position y
                              int(self.width / board.width),                # width
                              int(self.width / board.width)))               # height

        # apply changes to main window
        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()
