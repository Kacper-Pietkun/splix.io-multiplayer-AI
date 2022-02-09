from src.gui.window import Window
from src.constants import constant


class View:
    window = Window(constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT)

    def __init__(self):
        self.menu = None
        self.logic = None

    def create_main_panel(self):
        pass

    def get_view_logic(self):
        return self.logic

    def reset_view(self):
        if self.menu is not None:
            self.menu.clear()

    def display_menu(self):
        self.create_main_panel()
        self.menu.mainloop(self.window.screen)
