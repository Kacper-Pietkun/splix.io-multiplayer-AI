from src.constants import constant
from src.network.client.client import Client
from src.gui.gui_view.pop_up_view import PopUpView
from src.gui.gui_logic.logic import Logic
from src.exceptions.socket_exception import SocketException
from src.exceptions.end_of_game_exception import EndOfGameException
import socket


class JoinServerMenuLogic(Logic):

    def __init__(self, my_view, parent_view):
        super().__init__(my_view, parent_view)

    def join_server(self):
        player_name = self.my_view.client_name_object.get_value()
        server_ip = self.my_view.server_ip_object.get_value()
        name_len = len(player_name)
        if name_len < constant.PLAYER_NAME_MIN_LENGTH:
            pop_up_view = PopUpView(self.my_view, 'Warning', 'Name is too short', 'ok', None)
            pop_up_view.display_menu()
        elif name_len > constant.PLAYER_NAME_MAX_LENGTH:
            pop_up_view = PopUpView(self.my_view, 'Warning', 'Name is too long', 'ok', None)
            pop_up_view.display_menu()
        else:
            try:
                self.my_view.window.print_message_box('connecting to the server...')
                client = Client(server_ip, constant.STANDARD_PORT, self.my_view.window, self)
                client.connect_tcp_to_server()
            except (ConnectionRefusedError, TimeoutError) as e:
                client.connection_udp.my_socket.close()
                pop_up_view = PopUpView(self.my_view, 'Warning', 'Cannot connect to the server', 'ok', None)
                pop_up_view.display_menu()
                return
            except (OSError, socket.gaierror) as e:
                client.connection_udp.my_socket.close()
                pop_up_view = PopUpView(self.my_view, 'Warning', 'Check whether server IP is valid', 'ok', None)
                pop_up_view.display_menu()
                return

            try:
                client.join_game(player_name)
            except (SocketException, ConnectionResetError, ConnectionAbortedError) as e:
                client.connection_tcp.my_socket.close()
                client.connection_udp.my_socket.close()
                pop_up_view = PopUpView(self.my_view, 'Connection status', 'Lost connection', 'ok', None)
                pop_up_view.display_menu()
            except EndOfGameException as e:
                client.connection_tcp.my_socket.close()
                client.connection_udp.my_socket.close()
                pop_up_view = PopUpView(self.my_view, 'You lost', 'Your score: ' + str(client.final_score), 'ok', None)
                pop_up_view.display_menu()
