import threading
import socket
import selectors
from src.network.server.server_connection_tcp import ServerConnectionTCP


# We use TCP protocol to establish connection with players.
# Get theirs names, send them theirs ids
# Maintain connection during waiting for other players to connect
# Inform that game is going to be started
# After game is started, nothing more is sent through TCP, game data starts being transported via UDP
class ServerListenerTCP(threading.Thread):

    def __init__(self, ip_address, port, network_game_manager):
        threading.Thread.__init__(self)
        self.ip_address = ip_address
        self.port = port
        self.network_game_manager = network_game_manager
        self.is_server_running = True
        self.connection_threads = []

    def run(self):
        try:
            self.start_listening_for_players()
        except OSError as e:
            self.network_game_manager.has_game_ended = True

    def start_listening_for_players(self):
        print('listening...')
        print('ip address: ', self.ip_address)
        print('port: ', self.port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
            selector = selectors.DefaultSelector()
            listening_socket.bind((self.ip_address, self.port))
            listening_socket.listen(10)
            listening_socket.setblocking(False)
            selector.register(listening_socket, selectors.EVENT_READ, data=None)
            while self.is_server_running:
                events = selector.select(timeout=1)
                for key, mask in events:
                    if key.data is None:
                        connection_socket, address = key.fileobj.accept()
                        connection_socket.setblocking(True)
                        server_connection_tcp = ServerConnectionTCP(connection_socket, address,
                                                                    self.network_game_manager, self)
                        server_connection_tcp.start()  # start new thread for connected player
                        self.connection_threads.append(server_connection_tcp)
            for thread in self.connection_threads:
                thread.server_is_down_exception()
                thread.join()



