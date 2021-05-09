import socket
import pickle
from src.network.protocol.network_protocol import NetworkProtocol
from src.exceptions.socket_exception import SocketException
from src.exceptions.end_of_game_exception import EndOfGameException


class ClientConnection:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.my_socket = self.connect_to_server()
        self.network_protocol = NetworkProtocol(self.my_socket)

    def connect_to_server(self):
        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_socket.connect((self.server_ip, self.port))
        return connection_socket

    def initial_data_exchange(self, client_name):
        if self.network_protocol.send_message(pickle.dumps(client_name)) is not None:
            raise SocketException
        pickled_data = self.network_protocol.recv_msg()
        if not pickled_data:
            raise SocketException
        return pickle.loads(pickled_data)

    def listen_for_game_to_start(self, client):
        try:
            while client.is_game_running is False:
                pickled_status = self.network_protocol.recv_msg()
                if not pickled_status:
                    raise SocketException
                status = pickle.loads(pickled_status)
                if status == 1:
                    client.is_game_running = True  # game has started
                    break
                msg = 1
                if self.network_protocol.send_message(pickle.dumps(msg)) is not None:
                    raise SocketException
        except SocketException as e:
            client.raise_exception_from_other_thread(SocketException)

    def listen_for_game_data(self, client):
        pickled_data = self.network_protocol.recv_msg()
        if not pickled_data:
            raise SocketException
        received_data = pickle.loads(pickled_data)
        if type(received_data) is tuple:
            (client.serialized_board, client.serialized_players) = received_data
        else:  # player score (int) - sent when player dies
            client.final_score = received_data
            raise EndOfGameException
        client.is_game_running = True

    def send_game_data(self, data):
        if self.network_protocol.send_message(pickle.dumps(data)) is not None:
            raise SocketException

    def close_connection(self):
        self.my_socket.close()
