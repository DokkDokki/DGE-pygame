import pygame
pygame.init()

from initialize import display

# Set up font and text
font = pygame.font.Font("balancescale/assets/fonts/Montserrat-VariableFont_wght.ttf", 60)
text = font.render("Kaita is gay", True, (0, 0, 0))
text_rect = text.get_rect(center=(display.width // 2, display.height // 2))