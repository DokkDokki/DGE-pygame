import pygame

from initialize import display

# Set up font and text
font = pygame.font.Font("balancescale/assets/fonts/Montserrat-VariableFont_wght.ttf", 60)
text = font.render("Balance Scale", True, (0, 0, 0))

# Position from top-center
text_rect = text.get_rect(midtop=(display.width // 2, 50))  # 50 pixels from the top