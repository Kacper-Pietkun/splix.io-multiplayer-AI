import socket
import pickle
from src.exceptions.end_of_game_exception import EndOfGameException
from src.constants import constant


class ClientConnectionUDP:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_socket.settimeout(1)

    # Listen for information about the game
    def listen_for_game_data(self, client):
        try:
            received_message = self.my_socket.recvfrom(constant.MAX_UDP_PACKET_SIZE)
            received_data = pickle.loads(received_message[0])
            if type(received_data) is tuple:
                (client.serialized_board, client.serialized_players) = received_data
            else:  # player score (int) - sent when player dies
                client.final_score = received_data
                raise EndOfGameException
        except socket.timeout as e:
            pass

    # send to udp server information about player's id and pressed key
    def send_game_data(self, data):
        self.my_socket.sendto(pickle.dumps(data), (self.server_ip, self.port))
