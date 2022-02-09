import threading
import time
from src.management.game_managers.network_game_manager import NetworkGameManager
from src.network.server.server_listener import ServerListener
from src.constants import constant


class Server(threading.Thread):

    def __init__(self, ip_address, port, my_view):
        threading.Thread.__init__(self)
        self.ip_address = ip_address
        self.port = port
        self.network_game_manager = NetworkGameManager(constant.GAME_MAX_FPS)
        self.server_listener = ServerListener(ip_address, port, self.network_game_manager)
        self.my_view = my_view
        self.game_thread = None
        self.lock_close_server = threading.Lock()

    def run(self):
        self.server_listener.start()
        self.wait_for_game_to_end()
        self.close_server()

        self.my_view.title_label.set_title('Server is down')
        self.my_view.server_ip_label.set_title('')
        self.my_view.number_of_players.set_title('')
        self.my_view.button_label.set_title('ok')

    def wait_for_game_to_end(self):
        while self.network_game_manager.has_game_ended is False:
            if self.network_game_manager.is_game_running is False and \
                    len(self.network_game_manager.players) >= self.network_game_manager.minimal_no_of_players_to_start:
                self.network_game_manager.is_game_running = True
                self.game_thread = threading.Thread(target=self.network_game_manager.run, args=())
                self.game_thread.start()
            number_of_players = len(self.network_game_manager.players)
            self.my_view.number_of_players.set_title('Connected players: ' + str(number_of_players))
            time.sleep(0.5)
        if self.game_thread is not None:
            self.game_thread.join()

    def close_server(self):
        self.lock_close_server.acquire()
        if self.server_listener.is_server_running is True:
            self.server_listener.is_server_running = False
            self.network_game_manager.has_game_ended = True
            self.my_view.title_label.set_title('Wait for server to shut down...')
            self.my_view.button_label.hide()
            self.server_listener.join()
            if self.game_thread is not None:
                self.game_thread.join()
            self.my_view.button_label.show()
        self.lock_close_server.release()


