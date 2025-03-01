import pygame

def set_caption(icon_path, caption):
    #Set the window's title
    pygame.display.set_caption('Balance Scale')
    #Set the icon
    icon = pygame.image.load(balancescale/assets/balancescale.png)
    pygame.display.set_icon(icon)