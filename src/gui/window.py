import pygame
from src.constants import constant


class Window:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT))
        self.surface = pygame.Surface((width, height))
        self.text_font = pygame.font.SysFont("monospace", 15)

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

    def print_window_from_serialized(self, serialized_board, serialized_players):
        tile_width = self.width / serialized_board.width
        tile_height = self.height / serialized_board.height
        for i in range(0, serialized_board.width):
            for j in range(0, serialized_board.height):
                pygame.draw.rect(self.surface, serialized_board.tiles_colors[i][j],
                                 (i * tile_width,       # position x
                                  j * tile_height,      # position y
                                  tile_width,           # width
                                  tile_height))         # height
        # draw all players (without their names)
        for i in range(0, len(serialized_players)):
            pygame.draw.rect(self.surface, serialized_players[i].player_color,
                             (serialized_players[i].x * tile_width,     # position x
                              serialized_players[i].y * tile_height,    # position y
                              tile_width,                               # width
                              tile_height))                             # height

        # apply changes to main window
        self.screen.blit(self.surface, (0, 0))

        # draw player names
        for i in range(0, len(serialized_players)):
            label = self.text_font.render(serialized_players[i].name, True, (255, 255, 255))
            self.screen.blit(label, (serialized_players[i].x * tile_width + int(tile_width / 2) -
                                     tile_width / 2 * len(serialized_players[i].name)/2,  # position x
                                     serialized_players[i].y * tile_height - int(tile_height)))  # position y

        # draw player's score
        for i in range(0, len(serialized_players)):
            label = self.text_font.render(str(i + 1) + '. ' + serialized_players[i].name + ' - ' +
                                          str(serialized_players[i].score), True, (0, 0, 0))
            self.screen.blit(label, (self.width - self.width / 5,  # position x
                                     self.height / 50 + i * tile_height))  # position y

        pygame.display.update()

    def print_message_box(self, text):
        self.surface.fill((40, 41, 35))

        message_box_width = 300
        message_box_height = 200
        border_size = 10
        pygame.draw.rect(self.surface,
                         (77, 38, 0),                                           # color
                         (constant.WINDOW_WIDTH / 2 - message_box_width / 2,    # position x
                          constant.WINDOW_HEIGHT / 2 - message_box_height / 2,  # position y
                          message_box_width,                                    # width
                          message_box_height))                                  # height
        pygame.draw.rect(self.surface,
                         (255, 153, 51),                                                        # color
                         (constant.WINDOW_WIDTH / 2 - message_box_width / 2 + border_size,      # position x
                          constant.WINDOW_HEIGHT / 2 - message_box_height / 2 + border_size,    # position y
                          message_box_width - 2 * border_size,                                  # width
                          message_box_height - 2 * border_size))                                # height
        self.screen.blit(self.surface, (0, 0))
        label = self.text_font.render(text, True, (0, 0, 0))
        self.screen.blit(label, (constant.WINDOW_WIDTH / 2 - 120, constant.WINDOW_HEIGHT / 2))
        pygame.display.update()
