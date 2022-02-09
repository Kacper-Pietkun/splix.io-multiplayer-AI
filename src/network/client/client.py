import sys
import socket
import pygame
import time
import threading
from src.network.client.client_connection_tcp import ClientConnectionTCP
from src.network.client.client_connection_udp import ClientConnectionUDP
from src.exceptions.socket_exception import SocketException
from src.exceptions.end_of_game_exception import EndOfGameException


class Client:
    def __init__(self, server_ip, port, window, my_view):
        self.server_ip = server_ip
        self.port = port
        self.window = window
        self.my_view = my_view
        self.has_game_started = False
        self.player_id = None
        self.serialized_players = None
        self.serialized_board = None
        self.final_score = 0
        self.my_exception = None
        self.connection_udp = ClientConnectionUDP(server_ip, port)
        self.connection_tcp = ClientConnectionTCP(server_ip, port)
        self.has_connected = False

    def connect_tcp_to_server(self):
        iteration = 0
        thread = threading.Thread(target=self.connection_tcp.connect_to_server, args=(self,))
        thread.start()
        while self.has_connected is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.display_waiting_box(iteration)
            iteration += 1
            if self.my_exception == ConnectionRefusedError or\
                    self.my_exception == TimeoutError or \
                    self.my_exception == socket.gaierror:
                raise self.my_exception
            time.sleep(0.1)

    def join_game(self, client_name):
        self.player_id = self.connection_tcp.initial_data_exchange(client_name)
        self.waiting_phase()
        # game has started; from now on communicate via UDP;
        # however do not close TCP connection because it will be used
        # to make sure that the connection has not been broken
        thread = threading.Thread(target=self.connection_tcp.check_server_status, args=(self,))
        thread.start()
        self.game_phase()

    def waiting_phase(self):
        iteration = 0
        thread = threading.Thread(target=self.connection_tcp.listen_for_game_to_start, args=(self,))
        thread.start()
        while self.has_game_started is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.has_game_started = True  # in order to kill thread
                    thread.join()
                    self.connection_tcp.my_socket.close()
                    pygame.quit()
                    sys.exit()
            self.display_waiting_box(iteration)
            iteration += 1
            if self.my_exception == SocketException:
                raise SocketException
            time.sleep(0.1)

    def game_phase(self):
        while self.has_game_started:
            pressed_key = None
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pressed_key = event.key
                if event.type == pygame.QUIT:
                    self.connection_tcp.close_connection()
                    pygame.quit()
                    sys.exit()
            self.connection_udp.send_game_data((self.player_id, pressed_key))
            self.connection_udp.listen_for_game_data(self)
            self.window.print_window_from_serialized(self.serialized_board, self.serialized_players)
            if self.my_exception is not None:
                raise self.my_exception

    def display_waiting_box(self, iteration):
        wait_message = 'waiting for other players'
        dots = '.'
        iteration = iteration % 4
        self.window.print_message_box(wait_message + dots * iteration)

    # other threads use this function to raise exception in this thread
    def raise_exception_from_other_thread(self, exception):
        self.my_exception = exception
