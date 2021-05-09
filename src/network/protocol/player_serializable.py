class PlayerSerializable:
    def __init__(self, x, y, player_color, name, score):
        self.x = x
        self.y = y
        self.player_color = player_color
        self.name = name
        self.score = score

    @classmethod
    def from_player(cls, player):
        return cls(player.x, player.y, player.player_color, player.name, len(player.safe_zone_positions))
