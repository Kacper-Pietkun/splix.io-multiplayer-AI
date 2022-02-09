import socket
import pickle
from src.network.protocol.network_protocol import NetworkProtocol
from src.exceptions.socket_exception import SocketException
from src.exceptions.end_of_game_exception import EndOfGameException


class ClientConnectionTCP:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.my_socket = None
        self.network_protocol = None

    def connect_to_server(self, client):
        try:
            self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.my_socket.connect((self.server_ip, self.port))
            self.network_protocol = NetworkProtocol(self.my_socket)
            client.has_connected = True
        except ConnectionRefusedError as e:
            client.raise_exception_from_other_thread(ConnectionRefusedError)
        except TimeoutError as e:
            client.raise_exception_from_other_thread(TimeoutError)
        except socket.gaierror as e:
            client.raise_exception_from_other_thread(socket.gaierror)

    def initial_data_exchange(self, client_name):
        if self.network_protocol.send_message(pickle.dumps(client_name)) is not None:
            raise SocketException
        pickled_data = self.network_protocol.recv_msg()
        if not pickled_data:
            raise SocketException
        return pickle.loads(pickled_data)

    def listen_for_game_to_start(self, client):
        try:
            while client.has_game_started is False:
                pickled_status = self.network_protocol.recv_msg()
                if not pickled_status:
                    raise SocketException
                status = pickle.loads(pickled_status)
                if status == 1:
                    client.has_game_started = True  # game has started
                    break
                msg = 1
                if self.network_protocol.send_message(pickle.dumps(msg)) is not None:
                    raise SocketException
        except SocketException as e:
            client.raise_exception_from_other_thread(SocketException)

    def check_server_status(self, client):
        msg = 1
        try:
            while True:
                if not self.network_protocol.recv_msg():
                    raise SocketException
                if self.network_protocol.send_message(pickle.dumps(msg)) is not None:
                    raise SocketException
        except (SocketException, ConnectionResetError, ConnectionAbortedError) as e:
            client.raise_exception_from_other_thread(e)

    def close_connection(self):
        self.my_socket.close()
