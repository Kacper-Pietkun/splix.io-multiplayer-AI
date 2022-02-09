from src.management.game_managers.game_manager import GameManager
from src.constants import constant
from src.gui.gui_logic.logic import Logic
from src.gui.gui_view.pop_up_view import PopUpView


class SinglePlayerMenuLogic(Logic):
    def __init__(self, my_view, parent_view):
        super().__init__(my_view, parent_view)

    def change_bots(self, value, mode):
        self.my_view.single_player_mode = mode

    def play_with_bots(self):
        try:
            game_manager = GameManager(self.my_view.single_player_mode, constant.GAME_MAX_FPS,
                                       constant.All_BOTS_NUMBER, self.my_view.window, self.my_view)
            game_manager.run()
        except IOError as e:
            pop_up_view = PopUpView(self.my_view, 'Warning', 'You did not train any neat bots', 'ok', None)
            pop_up_view.display_menu()
