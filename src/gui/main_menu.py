import pygame
import pygame_menu
from src.gui.pop_up import PopUp
from src.constants import constant
from src.management.game_manager import GameManager
from src.management.neat_manager import NeatManager
from src.network.server.server import Server
from src.network.client.client import Client
from src.gui.window import Window


class MainMenu:

    def __init__(self):
        self.single_player_mode = constant.MODE_HEURISTIC_BOTS_ONLY
        self.window = Window(constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT)

        self.menu = pygame_menu.Menu(constant.TITLE, constant.WINDOW_WIDTH, constant.WINDOW_HEIGHT,
                                     theme=pygame_menu.themes.THEME_DARK)
        self.client_name_object = None
        self.create_main_panel()

    def reset_view(self):
        self.menu.clear()

    def create_main_panel(self):
        self.client_name_object = self.menu.add.text_input('Name: ')
        self.menu.add.button('Join server', self.join_server)
        self.menu.add.button('Create server', self.create_server)
        self.menu.add.button('Play with bots', self.play_with_bots)
        self.menu.add.selector('Bots types: ', [('Heuristic', constant.MODE_HEURISTIC_BOTS_ONLY),
                                                ('   Neat   ', constant.MODE_NEAT_BOTS_ONLY),
                                                ('   Both   ', constant.MODE_BOTH_BOTS_ONLY)],
                               onchange=self.change_bots)
        self.menu.add.button('Train new neat bots', self.train_new_neat_bots)
        self.menu.add.button('Train saved neat bots', self.train_saved_neat_bots)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def display_pop_up(self, title, info, button_text, callback):
        self.reset_view()
        return PopUp(self, title, info, button_text, callback)

    def display_menu(self):
        self.menu.mainloop(self.window.screen)

    def join_server(self):
        name_len = len(self.client_name_object.get_value())
        if name_len < 1 or name_len > 7:
            self.display_pop_up('Warning', 'Invalid name', 'ok', None)
        else:
            try:
                self.window.print_message_box('connecting to the server...')
                client = Client('127.0.0.1', 6464, self.window, self)
                client.join_game(self.client_name_object.get_value())
            except ConnectionRefusedError as e:
                self.display_pop_up('Warning', 'Cannot connect to the server', 'ok', None)

    def create_server(self):
        server = Server('127.0.0.1', 6464, self)
        server.start()

    def play_with_bots(self):
        try:
            game_manager = GameManager(self.single_player_mode, constant.GAME_MAX_FPS,
                                       constant.BOTS_NUMBER, self.window)
            game_manager.run()
        except IOError as e:
            self.display_pop_up('Warning', 'You did not train any neat bots', 'ok', None)

    def change_bots(self, value, difficulty):
        self.single_player_mode = difficulty

    def train_new_neat_bots(self):
        neat_manager = NeatManager(constant.TRAINING_MAX_FPS, constant.VISUALIZE_TRAINING, self.window)
        neat_manager.run()

    def train_saved_neat_bots(self):
        neat_manager = NeatManager(constant.TRAINING_MAX_FPS, constant.VISUALIZE_TRAINING, self.window)
        try:
            neat_manager.load_population()
            neat_manager.run()
        except IOError as e:
            self.display_pop_up('Warning', 'You did not save any neat bots', 'ok', None)



