import pygame_menu
from src.constants import constant
from src.gui.gui_logic.create_server_menu_logic import CreateServerMenuLogic
from src.gui.gui_view.view import View


class CreateServerMenuView(View):

    def __init__(self, parent_view):
        super().__init__()
        self.logic = CreateServerMenuLogic(my_view=self, parent_view=parent_view)
        self.menu = pygame_menu.Menu(constant.TITLE, constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT,
                                     theme=pygame_menu.themes.THEME_DARK)
        self.title_label = None
        self.server_ip_label = None
        self.number_of_players = None
        self.button_label = None

    def create_main_panel(self):
        frame = self.menu.add.frame_v(constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT / 2,
                                      background_color=(50, 50, 50), padding=0)
        frame_bar = self.menu.add.frame_h(constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT / 8,
                                          background_color=(180, 180, 180), padding=0)
        frame_content = self.menu.add.frame_v(constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT / 4, padding=30)
        frame.pack(frame_bar)
        frame.pack(frame_content)

        self.title_label = self.menu.add.label('Server is running', font_size=45, font_color=(255, 204, 0))
        self.server_ip_label = self.menu.add.label('Server IP: ' + self.logic.get_server_ip(), font_size=25, font_color=(255, 204, 0),
                                                   padding=15)
        self.number_of_players = self.menu.add.label('Connected players: 0', font_size=25, font_color=(255, 204, 0),
                                                     padding=15)
        self.button_label = self.menu.add.button('shut down', self.logic.close_server)

        frame_bar.pack(self.title_label, align=pygame_menu.locals.ALIGN_CENTER)
        frame_content.pack(self.server_ip_label, align=pygame_menu.locals.ALIGN_CENTER)
        frame_content.pack(self.number_of_players, align=pygame_menu.locals.ALIGN_CENTER)
        frame.pack(self.button_label, align=pygame_menu.locals.ALIGN_CENTER)

        self.logic.create_server()
