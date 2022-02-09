import pygame_menu
from src.constants import constant
from src.gui.gui_logic.multiplayer_menu_logic import MultiplayerMenuLogic
from src.gui.gui_view.view import View


class MultiplayerMenuView(View):

    def __init__(self, parent_view):
        super().__init__()
        self.logic = MultiplayerMenuLogic(my_view=self, parent_view=parent_view)
        self.menu = pygame_menu.Menu(constant.TITLE, constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT,
                                     theme=pygame_menu.themes.THEME_DARK)

    def create_main_panel(self):
        self.menu.add.button('Join server', self.logic.open_join_server_menu)
        self.menu.add.button('Create server', self.logic.open_create_server_menu)
        self.menu.add.button('Back', self.logic.back_to_parent_view)
