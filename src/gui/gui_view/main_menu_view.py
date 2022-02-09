import pygame_menu
from src.constants import constant
from src.gui.gui_logic.main_menu_logic import MainMenuLogic
from src.gui.gui_view.view import View


class MainMenuView(View):

    def __init__(self):
        super().__init__()
        self.logic = MainMenuLogic(my_view=self, parent_view=None)
        self.menu = pygame_menu.Menu(constant.TITLE, constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT,
                                     theme=pygame_menu.themes.THEME_DARK)

    def create_main_panel(self):
        self.menu.add.button('Single player', self.logic.open_single_player_menu)
        self.menu.add.button('Multiplayer', self.logic.open_multiplayer_menu)
        self.menu.add.button('Bots training', self.logic.open_bots_training_menu)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
