import pygame
from src.gui.main_menu import MainMenu

if __name__ == '__main__':
    pygame.init()
    main_menu = MainMenu()
    main_menu.display_menu()
