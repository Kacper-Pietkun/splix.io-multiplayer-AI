import threading
import pygame
from src.players.human_player import HumanPlayer
from src.management.game_managers.manager import Manager
from src.constants import constant
from src.network.protocol.player_serializable import PlayerSerializable
from src.network.protocol.board_serializable import BoardSerializable


# For single online multiplayer games
class NetworkGameManager(Manager):
    def __init__(self, max_fps):
        super().__init__(max_fps, None)
        self.lock = threading.Lock()
        self.current_player_id = 0
        self.has_game_started = False
        self.has_game_ended = False
        self.minimal_no_of_players_to_start = constant.MINIMAL_NUMBER_OF_PLAYER_TO_START
        self.dead_players = []

    def run(self):
        self.game_loop()

    def game_loop(self):
        while self.has_game_ended is False:
            self.clock.tick(self.max_fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.has_game_ended = True
            with self.lock:
                self.players_action(None)
                self.remove_dead_players()
                if len(self.players) == 0:
                    self.has_game_ended = True

    def register_new_player(self, client_name):
        print('register player with name: ', client_name)
        with self.lock:
            self.current_player_id += 1
            new_player = HumanPlayer(self.board, self, self.current_player_id)
            new_player.name = client_name
            self.players.append(new_player)
            returned_id = self.current_player_id
        return returned_id

    # return None if player doesn't exist
    def is_player_dead(self, player_id):
        with self.lock:
            try:
                player = next(filter(lambda el: (el.id == player_id), self.players))
                is_dead = False
            except StopIteration as e:
                is_dead = True
        return is_dead

    def remove_dead_players(self):
        self.dead_players.extend(list(filter(lambda x: x.is_dead is True, self.players)))
        super().remove_dead_players()

    def get_dead_player_score(self, player_id):
        with self.lock:
            try:
                player = next(filter(lambda el: (el.id == player_id), self.dead_players))
                score = len(player.safe_zone_positions)
            except StopIteration as e:
                return 0
        return score

    def change_player_direction(self, player_id, key_direction):
        with self.lock:
            try:
                player = next(filter(lambda el: (el.id == player_id), self.players))
                player.change_direction(key_direction)
            except StopIteration as e:
                return

    def remove_disconnected_player(self, player_id):
        with self.lock:
            self.kill_player(player_id)
            self.remove_dead_players()

    def return_serialized_data(self):
        with self.lock:
            serialized_board = BoardSerializable.from_board(self.board)
            serialized_players = []
            for player in self.players:
                serialized_players.append(PlayerSerializable.from_player(player))
        # sort serialized_players basing on their score descending
        serialized_players.sort(key=lambda el: el.score, reverse=True)
        return serialized_board, serialized_players

