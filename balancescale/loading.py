import pygame
import time
from initialize.display import screen, background

def loading_screen():
    # Initialize Pygame
    pygame.init()

    # Background color
    screen.fill((0, 0, 255))  # Clear the screen with blue color
    
    # Set up font and text
    font = pygame.font.Font("balancescale/assets/fonts/MISHIMISHI-BLOCK.otf", 97)
    text = font.render("ローディング", True, (255, 255, 255))
    text_stroke = font.render("ローディング", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Create a new surface for the text with stroke
    text_surface = pygame.Surface((text_rect.width + 4, text_rect.height + 4), pygame.SRCALPHA)
    text_surface.fill((0, 0, 0, 0))  # Fill with transparent color

    # Blit the stroke text onto the surface
    for dx, dy in [(-6, 0), (6, 0), (0, -6), (0, 6)]:
        text_surface.blit(text_stroke, (2 + dx, 2 + dy))

    # Blit the main text onto the surface
    text_surface.blit(text, (2, 2))

    # Animation loop for 3 seconds
    start_time = time.time()
    while time.time() - start_time < 4.3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.blit(background, (0, 0))
        screen.blit(text_surface, text_rect.topleft)
        pygame.display.update()

    # Transition to simulation
    import simulation
    simulation.main()