import pygame_menu
from src.constants import constant
from src.gui.gui_logic.single_player_menu_logic import SinglePlayerMenuLogic
from src.gui.gui_view.view import View


class SinglePlayerMenuView(View):

    def __init__(self, parent_view):
        super().__init__()
        self.client_name_object = None
        self.single_player_mode = constant.MODE_HEURISTIC_BOTS_ONLY
        self.logic = SinglePlayerMenuLogic(my_view=self, parent_view=parent_view)
        self.menu = pygame_menu.Menu(constant.TITLE, constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT,
                                     theme=pygame_menu.themes.THEME_DARK)

    def create_main_panel(self):
        self.client_name_object = self.menu.add.text_input('Name: ')
        self.menu.add.selector('Bots types: ', [('Heuristic', constant.MODE_HEURISTIC_BOTS_ONLY),
                                                ('   Neat   ', constant.MODE_NEAT_BOTS_ONLY),
                                                ('   Both   ', constant.MODE_BOTH_BOTS_ONLY)],
                               onchange=self.logic.change_bots)
        self.menu.add.button('Play', self.logic.play_with_bots)
        self.menu.add.button('Back', self.logic.back_to_parent_view)
