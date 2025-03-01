import pygame
def display_init(display_size):
    #Initialize the module
    pygame.init()

    #Set up the display and window's title
    screen = pygame.display.set_mode(display_size[0], display_size[1])
    return screen