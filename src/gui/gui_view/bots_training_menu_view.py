import pygame_menu
from src.constants import constant
from src.gui.gui_logic.bots_training_menu_logic import BotsTrainingMenuLogic
from src.gui.gui_view.view import View


class BotsTrainingMenuView(View):

    def __init__(self, parent_view):
        super().__init__()
        self.logic = BotsTrainingMenuLogic(my_view=self, parent_view=parent_view)
        self.menu = pygame_menu.Menu(constant.TITLE, constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT,
                                     theme=pygame_menu.themes.THEME_DARK)

    def create_main_panel(self):
        self.menu.add.button('Train new NEAT bots', self.logic.train_new_neat_bots)
        self.menu.add.button('Train saved NEAT bots', self.logic.train_saved_neat_bots)
        self.menu.add.button('Back', self.logic.back_to_parent_view)
