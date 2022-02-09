from src.constants import constant
import socket
import pickle
import threading


# We use UDP protocol to transport data during actual game.
# Receive player's id and direction it wants to go and send back whole map so client can render game's screen.
class ListenerUDP(threading.Thread):
    def __init__(self, ip_address, port, network_game_manager):
        threading.Thread.__init__(self)
        self.ip_address = ip_address
        self.port = port
        self.network_game_manager = network_game_manager
        self.sock_buffer_size = constant.MAX_UDP_PACKET_SIZE

    def run(self):
        self.start_listening()

    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            my_socket.bind((self.ip_address, self.port))
            my_socket.settimeout(1)
            while self.network_game_manager.has_game_ended is False:
                try:
                    # Receive data from any of the players
                    data, player_address = my_socket.recvfrom(self.sock_buffer_size)
                    # Unpack received data
                    (player_id, key_direction) = pickle.loads(data)

                    # Check whether player is still alive
                    if self.network_game_manager.is_player_dead(player_id):
                        # Send player information that he is dead
                        self.network_game_manager.remove_disconnected_player(player_id)
                        player_score = self.network_game_manager.get_dead_player_score(player_id)
                        my_socket.sendto(pickle.dumps(player_score), player_address)
                    else:
                        # Update direction for given player
                        self.network_game_manager.change_player_direction(player_id, key_direction)

                        # Now send back to this specific player information about the game
                        serialized_board, serialized_players = self.network_game_manager.return_serialized_data()
                        data_to_send = (serialized_board, serialized_players)
                        my_socket.sendto(pickle.dumps(data_to_send), player_address)
                except socket.timeout as e:
                    pass

