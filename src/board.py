import constant


class Board:
    def __init__(self, width, height, player_spawn_size):
        self.width = width
        self.height = height
        self.player_spawn_size = player_spawn_size
        self.tiles = []
        for i in range(0, width):
            self.tiles.append([])
            for j in range(0, height):
                self.tiles[i].append(self.Tile())

    # Board consists of a large number of tiles
    class Tile:
        def __init__(self):
            self.owner_id = 0  # neutral tile, doesn't belong to any player
            self.color = constant.BOARD_TILE_NEUTRAL_COLOR
            self.is_trail = False

    # Every time players draws a position for his spawn, it needs to be checked whether that position is available
    def can_create_player_spawn(self, x, y):
        for i in range(x, x + self.player_spawn_size):
            for j in range(y, y + self.player_spawn_size):
                if j >= self.height or i >= self.width or self.tiles[i][j].owner_id != 0:
                    return False
        return True

    # After checking whether drawn position is available, player's spawn can be spawned on that area
    def create_player_spawn(self, player_id, player_tile_color, x, y):
        for i in range(x, x + self.player_spawn_size):
            for j in range(y, y + self.player_spawn_size):
                self.tiles[i][j].owner_id = player_id
                self.tiles[i][j].color = player_tile_color

    # It rewrites information that given tile is currently containing
    # for instance, if a player moves on this tile, then we change tiles owner id, color and whether it is a trail...
    def change_tile_information(self, player, x, y, is_trail):
        self.tiles[x][y].owner_id = player.id
        self.tiles[x][y].is_trail = is_trail
        if is_trail is True:
            self.tiles[x][y].color = player.trail_color
        else:
            self.tiles[x][y].color = player.tile_color

    def get_tile_information(self, x, y):
        return self.tiles[x][y]

    # We create an array which will contain a fragment of the original tiles array, but it will store only player's id
    # Thanks to this array, we will be able to determine which tiles should be colored, when player will
    # connect a trail to his zone
    def fill_zone(self, player):
        help_tiles = []
        # + 3 because we want to have 1 column and 1 row padding on each side of the array
        for i in range(0, player.max_pos_x - player.min_pos_x + 3):
            help_tiles.append([])
            for j in range(0, player.max_pos_y - player.min_pos_y + 3):
                help_tiles[i].append(0)  # 0 means that it is a neutral tile

        # rewrite original data to help array
        for i in range(1, player.max_pos_x - player.min_pos_x + 2):
            for j in range(1, player.max_pos_y - player.min_pos_y + 2):
                help_tiles[i][j] = self.tiles[player.min_pos_x + i - 1][player.min_pos_y + j - 1].owner_id

        # fill array to determine the zone, which was marked by player
        self.start_filling_array(help_tiles, player.id, 0, 0)

        # color rest of the tiles that are in the zone
        for i in range(1, player.max_pos_x - player.min_pos_x + 2):
            for j in range(1, player.max_pos_y - player.min_pos_y + 2):
                if help_tiles[i][j] != -1:
                    self.change_tile_information(player, player.min_pos_x + i - 1,
                                                 player.min_pos_y + j - 1, is_trail=False)

    def start_filling_array(self, help_tiles, player_id, x, y):
        stack_positions = [(x, y)]
        while len(stack_positions) != 0:
            pos_x, pos_y = stack_positions.pop()
            if pos_x < 0 or pos_y < 0 or pos_x >= len(help_tiles) or pos_y >= len(help_tiles[0]):
                continue
            if help_tiles[pos_x][pos_y] == player_id or help_tiles[pos_x][pos_y] == -1:
                continue
            help_tiles[pos_x][pos_y] = -1
            stack_positions.append((pos_x+1, pos_y))
            stack_positions.append((pos_x-1, pos_y))
            stack_positions.append((pos_x, pos_y+1))
            stack_positions.append((pos_x, pos_y-1))

    # Triggered when player dies
    # Make all of player's tiles neutral
    def clear_player_tiles(self, player):
        for i in range(player.min_pos_x, player.max_pos_x + 1):
            for j in range(player.min_pos_y, player.max_pos_y + 1):
                if i < 0 or i >= self.width or j < 0 or j >= self.height:
                    continue
                if self.tiles[i][j].owner_id == player.id:
                    self.tiles[i][j].owner_id = 0
                    self.tiles[i][j].is_trail = False
                    self.tiles[i][j].color = constant.BOARD_TILE_NEUTRAL_COLOR
