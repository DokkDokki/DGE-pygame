import pygame
import sys

# Initialize Pygame
pygame.init()

# Import initialize module
from initialize import display, caption
from objects import title

#Load Background Music
#pygame.mixer.music.load('balancescale/assets/music/06052021_1_loading_screen_fresh_air_saturation.mp3')
#pygame.mixer.music.play(-1)

# Main game loop
running = True
while running:
    # Draw the background
    display.screen.blit(display.background, (0, 0))

    # Draw the text on the screen
    display.screen.blit(title.text, title.text_rect)

    # Update the display
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
# Quit pygame and exit program after the main loop ends
pygame.quit()
sys.exit()
