import pygame
import time
import threading
from src.network.client.client_connection import ClientConnection
from src.exceptions.socket_exception import SocketException
from src.exceptions.end_of_game_exception import EndOfGameException


class Client:
    def __init__(self, server_ip, port, window, main_menu):
        self.server_ip = server_ip
        self.port = port
        self.connection = ClientConnection(server_ip, port)
        self.window = window
        self.main_menu = main_menu
        self.is_game_running = False
        self.player_id = None
        self.serialized_players = None
        self.serialized_board = None
        self.final_score = 0
        self.my_exception = None

    def join_game(self, client_name):
        try:
            self.player_id = self.connection.initial_data_exchange(client_name)
            self.waiting_phase()
            self.game_phase()
        except (SocketException, ConnectionResetError, ConnectionAbortedError) as e:
            self.connection.my_socket.close()
            self.main_menu.display_pop_up('Connection status', 'Lost connection', 'ok', None)
        except EndOfGameException as e:
            self.connection.my_socket.close()
            self.main_menu.display_pop_up('You lost', 'Your score: ' + str(self.final_score), 'ok', None)

    def waiting_phase(self):
        iteration = 0
        thread = threading.Thread(target=self.connection.listen_for_game_to_start, args=(self,))
        thread.start()
        while self.is_game_running is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.connection.my_socket.close()
                    pygame.quit()
            wait_message = 'waiting for other players'
            dots = '.'
            iteration = iteration % 4
            self.window.print_message_box(wait_message + dots * iteration)
            iteration += 1
            if self.my_exception == SocketException:
                raise SocketException
            time.sleep(0.1)

    def game_phase(self):
        while self.is_game_running:
            pressed_key = None
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pressed_key = event.key
                if event.type == pygame.QUIT:
                    self.connection.close_connection()
                    self.is_game_running = False
            self.connection.listen_for_game_data(self)
            self.connection.send_game_data((self.player_id, pressed_key))
            self.window.print_window_from_serialized(self.serialized_board, self.serialized_players)

    def raise_exception_from_other_thread(self, exception):
        self.my_exception = exception
