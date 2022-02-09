import socket
from src.constants import constant
from src.network.server.server import Server
from src.gui.gui_logic.logic import Logic


class CreateServerMenuLogic(Logic):

    def __init__(self, my_view, parent_view):
        super().__init__(my_view, parent_view)
        self.address_ip = '127.0.0.1'
        self.port = constant.STANDARD_PORT
        self.server = None
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            self.address_ip = s.getsockname()[0]

    def create_server(self):
        self.server = Server(self.address_ip, self.port, self.my_view)
        self.server.start()

    def close_server(self):
        if self.server is not None:
            self.server.close_server()
            self.back_to_parent_view()

    def get_server_ip(self):
        return self.address_ip
