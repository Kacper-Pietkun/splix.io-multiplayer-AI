from src.gui.gui_logic.logic import Logic
from src.gui.gui_view.join_server_menu_view import JoinServerMenuView
from src.gui.gui_view.create_server_menu_view import CreateServerMenuView


class MultiplayerMenuLogic(Logic):

    def __init__(self, my_view, parent_view):
        super().__init__(my_view, parent_view)

    def open_join_server_menu(self):
        join_server_view = JoinServerMenuView(self.my_view)
        join_server_view.display_menu()

    def open_create_server_menu(self):
        create_server_view = CreateServerMenuView(self.my_view)
        create_server_view.display_menu()
