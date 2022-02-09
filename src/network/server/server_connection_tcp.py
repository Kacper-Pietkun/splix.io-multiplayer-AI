import threading
import pickle
import time
import ctypes
from src.network.protocol.network_protocol import NetworkProtocol
from src.constants import constant
from src.exceptions.socket_exception import SocketException


# We use TCP to establish first connection with the player
# receive player's name
# send player's id to the player
# After the game starts, we check every second whether connection has not been broken
class ServerConnectionTCP(threading.Thread):

    def __init__(self, my_socket, address, network_game_manager, server_listener):
        threading.Thread.__init__(self)
        self.my_socket = my_socket
        self.address = address
        self.network_game_manager = network_game_manager
        self.server_listener = server_listener
        self.network_protocol = None
        self.handled_player_id = None

    def run(self):
        try:
            self.handle_connection()
        except (SocketException, ConnectionResetError, ConnectionAbortedError) as e:
            self.network_game_manager.remove_disconnected_player(self.handled_player_id)
            print("Client disconnected unexpectedly: ", self.address)
        except SystemExit as e:
            self.network_game_manager.remove_disconnected_player(self.handled_player_id)
            print("closing server on purpose:", self.address)

    def handle_connection(self):
        with self.my_socket as socket:
            self.is_there_place_for_a_new_client()
            self.network_protocol = NetworkProtocol(socket)
            print('Connected by: ', self.address)

            self.initial_data_exchange()

            # waiting for the minimal number of players to start the game
            while self.network_game_manager.has_game_started is False:
                self.check_client_status()
                time.sleep(0.1)

            self.inform_player_about_starting_the_game()
            # The game has started from now on player will communicate with server via UDP protocol in order
            # to get the information about the game
            # However we use TCP to check if the connection has not been broken
            while True:
                self.check_client_status()
                time.sleep(0.5)

    def is_there_place_for_a_new_client(self):
        if len(self.network_game_manager.players) >= constant.MULTIPLAYER_MAX_NO_OF_PLAYERS:
            raise SocketException

    def initial_data_exchange(self):
        client_name = pickle.loads(self.network_protocol.recv_msg())
        if not client_name:
            raise SocketException
        self.handled_player_id = self.network_game_manager.register_new_player(client_name)
        if self.network_protocol.send_message(pickle.dumps(self.handled_player_id)) is not None:
            raise SocketException

    # when player is waiting for the game to start
    # server and client exchange meaningless information to confirm that the connection has not been broken
    def check_client_status(self):
        msg = 0
        if self.network_protocol.send_message(pickle.dumps(msg)) is not None:
            raise SocketException
        if not self.network_protocol.recv_msg():
            raise SocketException

    def inform_player_about_starting_the_game(self):
        msg = 1
        if self.network_protocol.send_message(pickle.dumps(msg)) is not None:
            raise SocketException

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def server_is_down_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
