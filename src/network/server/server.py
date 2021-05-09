import threading
import time
from src.management.network_game_manager import NetworkGameManager
from src.network.server.server_listener import ServerListener
from src.constants import constant


class Server(threading.Thread):

    def __init__(self, ip_address, port, main_menu):
        threading.Thread.__init__(self)
        self.ip_address = ip_address
        self.port = port
        self.network_game_manager = NetworkGameManager(constant.GAME_MAX_FPS)
        self.server_listener = ServerListener(ip_address, port, self.network_game_manager)
        self.main_menu = main_menu
        self.menu_pop_up = None
        self.game_thread = None

    def run(self):
        self.menu_pop_up = self.main_menu.display_pop_up('Server status', 'connected players: 0',
                                                         'close server', self.close_server)
        self.server_listener.start()
        self.wait_for_game_to_end()
        self.close_server()
        self.menu_pop_up.message_label.set_title('server is down')
        self.menu_pop_up.button.set_title('ok')

    def wait_for_game_to_end(self):
        while self.network_game_manager.has_game_ended is False:
            if self.network_game_manager.is_game_running is False and \
                    len(self.network_game_manager.players) >= self.network_game_manager.minimal_no_of_players_to_start:
                self.network_game_manager.is_game_running = True
                self.game_thread = threading.Thread(target=self.network_game_manager.run, args=())
                self.game_thread.start()
            self.menu_pop_up.message_label.set_title('waiting phase | players: ' +
                                                     str(len(self.network_game_manager.players)))
            time.sleep(0.5)
        if self.game_thread is not None:
            self.game_thread.join()

    def close_server(self):
        if self.server_listener.is_server_running is True:
            self.server_listener.is_server_running = False
            self.network_game_manager.has_game_ended = True
            self.menu_pop_up.message_label.set_title('wait for server to shut down..')
            self.menu_pop_up.button.hide()
            self.server_listener.join()
            if self.game_thread is not None:
                self.game_thread.join()
            self.menu_pop_up.button.show()


