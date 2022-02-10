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
        player_name = self.my_view.client_name_object.get_value()
        name_len = len(player_name)
        if name_len < constant.PLAYER_NAME_MIN_LENGTH:
            pop_up_view = PopUpView(self.my_view, 'Warning', 'Name is too short', 'ok', None)
            pop_up_view.display_menu()
        elif name_len > constant.PLAYER_NAME_MAX_LENGTH:
            pop_up_view = PopUpView(self.my_view, 'Warning', 'Name is too long', 'ok', None)
            pop_up_view.display_menu()

        try:
            game_manager = GameManager(self.my_view.single_player_mode, constant.GAME_MAX_FPS,
                                       constant.All_BOTS_NUMBER, self.my_view.window, self.my_view, player_name)
            game_manager.run()
        except IOError as e:
            pop_up_view = PopUpView(self.my_view, 'Warning', 'You did not train any neat bots', 'ok', None)
            pop_up_view.display_menu()
