import pygame
import sys

# Initialize Pygame
pygame.init()

# Import initialize module
from initialize import display, caption

# Set up font and text
font = pygame.font.Font("balancescale/assets/fonts/Montserrat-VariableFont_wght.ttf", 60)
text = font.render("Kaita is gay", True, (0, 0, 0))
text_rect = text.get_rect(center=(display.width // 2, display.height // 2))

#Load Background Music
pygame.mixer.music.load('balancescale/assets/music/06052021_1_loading_screen_fresh_air_saturation.mp3')
pygame.mixer.music.play(-1)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background
    display.screen.blit(display.background, (0, 0))

    # Draw the text on the screen
    display.screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()