from src.gui.gui_view.single_player_menu_view import SinglePlayerMenuView
from src.gui.gui_view.multiplayer_menu_view import MultiplayerMenuView
from src.gui.gui_view.bots_training_menu_view import BotsTrainingMenuView
from src.gui.gui_logic.logic import Logic


class MainMenuLogic(Logic):

    def __init__(self, my_view, parent_view):
        super().__init__(my_view, parent_view)

    def open_single_player_menu(self):
        single_player_view = SinglePlayerMenuView(self.my_view)
        single_player_view.display_menu()

    def open_multiplayer_menu(self):
        multiplayer_view = MultiplayerMenuView(self.my_view)
        multiplayer_view.display_menu()

    def open_bots_training_menu(self):
        bots_training_view = BotsTrainingMenuView(self.my_view)
        bots_training_view.display_menu()
