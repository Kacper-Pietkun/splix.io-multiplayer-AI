import pygame
from src.gui.gui_view.main_menu_view import MainMenuView

if __name__ == '__main__':
    pygame.init()
    main_menu = MainMenuView()
    main_menu.display_menu()
