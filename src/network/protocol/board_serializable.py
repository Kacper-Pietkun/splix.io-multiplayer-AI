class BoardSerializable:
    def __init__(self, width, height, tiles_colors):
        self.width = width
        self.height = height
        self.tiles_colors = tiles_colors

    @classmethod
    def from_board(cls, board):
        tiles_colors = []
        for i in range(0, board.width):
            tiles_colors.append([])
            for j in range(0, board.height):
                tiles_colors[i].append(board.tiles[i][j].color)
        return cls(board.width, board.height, tiles_colors)
