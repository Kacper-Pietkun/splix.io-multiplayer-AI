import pygame_menu
from src.constants import constant
from src.gui.gui_logic.join_server_menu_logic import JoinServerMenuLogic
from src.gui.gui_view.view import View


class JoinServerMenuView(View):

    def __init__(self, parent_view):
        super().__init__()
        self.client_name_object = None
        self.server_ip_object = None
        self.logic = JoinServerMenuLogic(my_view=self, parent_view=parent_view)
        self.menu = pygame_menu.Menu(constant.TITLE, constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT,
                                     theme=pygame_menu.themes.THEME_DARK)

    def create_main_panel(self):
        self.client_name_object = self.menu.add.text_input('Name: ')
        self.server_ip_object = self.menu.add.text_input('Server IP: ')
        self.menu.add.button('Join', self.logic.join_server)
        self.menu.add.button('Back', self.logic.back_to_parent_view)
