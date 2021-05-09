import pygame_menu
from src.constants import constant


class PopUp:

    def __init__(self, parent_menu, title, info, button_text, callback):
        self.parent_menu = parent_menu
        self.callback = callback

        self.frame = self.parent_menu.menu.add.frame_v(constant.WINDOW_WIDTH / 2, constant.WINDOW_HEIGHT / 4,
                                                       background_color=(50, 50, 50), padding=0)
        self.frame_bar = self.parent_menu.menu.add.frame_h(constant.WINDOW_WIDTH / 2, constant.WINDOW_HEIGHT / 10,
                                                           background_color=(180, 180, 180), padding=0)
        self.frame_content = self.parent_menu.menu.add.frame_v(constant.WINDOW_WIDTH / 2,
                                                               6.5 * constant.WINDOW_HEIGHT / 80, padding=0)
        self.frame.pack(self.frame_bar)
        self.frame.pack(self.frame_content)

        self.title_label = self.parent_menu.menu.add.label(title, font_size=45, font_color=(255, 204, 0))
        self.message_label = self.parent_menu.menu.add.label(info, font_size=25, font_color=(255, 204, 0), padding=15)
        self.button = self.parent_menu.menu.add.button(button_text, self.close_pop_up)

        self.frame_bar.pack(self.title_label, align=pygame_menu.locals.ALIGN_CENTER)
        self.frame_content.pack(self.message_label, align=pygame_menu.locals.ALIGN_CENTER)
        self.frame.pack(self.button, align=pygame_menu.locals.ALIGN_CENTER)

    def close_pop_up(self):
        if self.callback is not None:
            self.callback()
        self.parent_menu.reset_view()
        self.parent_menu.create_main_panel()
