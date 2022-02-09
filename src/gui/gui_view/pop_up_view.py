import pygame_menu
from src.constants import constant
from src.gui.gui_logic.pop_up_logic import PopUpLogic
from src.gui.gui_view.view import View


class PopUpView(View):

    def __init__(self, parent_menu, title, message, button_text, callback):
        super().__init__()
        self.logic = PopUpLogic(my_view=self, parent_view=parent_menu, callback=callback)
        self.menu = pygame_menu.Menu(constant.TITLE, constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT,
                                     theme=pygame_menu.themes.THEME_DARK)
        self.title = title
        self.title_label = None

        self.message = message
        self.message_label = None

        self.button_text = button_text
        self.button_label = None

    def create_main_panel(self):
        frame = self.menu.add.frame_v(constant.WINDOW_WIDTH / 2, constant.WINDOW_HEIGHT / 4,
                                      background_color=(50, 50, 50), padding=0)
        frame_bar = self.menu.add.frame_h(constant.WINDOW_WIDTH / 2, constant.WINDOW_HEIGHT / 10,
                                          background_color=(180, 180, 180), padding=0)
        frame_content = self.menu.add.frame_v(constant.WINDOW_WIDTH / 2,
                                              6.5 * constant.WINDOW_HEIGHT / 80, padding=0)
        frame.pack(frame_bar)
        frame.pack(frame_content)

        self.title_label = self.menu.add.label(self.title, font_size=45, font_color=(255, 204, 0))
        self.message_label = self.menu.add.label(self.message, font_size=25, font_color=(255, 204, 0), padding=15)
        self.button_label = self.menu.add.button(self.button_text, self.logic.close_pop_up)

        frame_bar.pack(self.title_label, align=pygame_menu.locals.ALIGN_CENTER)
        frame_content.pack(self.message_label, align=pygame_menu.locals.ALIGN_CENTER)
        frame.pack(self.button_label, align=pygame_menu.locals.ALIGN_CENTER)
