import pygame
import time
import math
from initialize.display import screen, background

def loading_screen():
    # Initialize Pygame
    pygame.init()

    # Background color
    screen.fill((0, 0, 255))

    # Set up font and text with increased size
    font = pygame.font.Font("balancescale/assets/fonts/MISHIMISHI-BLOCK.otf", 192)
    characters = list("ローディング")
    char_surfaces = []
    char_strokes = []
    
    # Create individual character surfaces
    for char in characters:
        char_text = font.render(char, True, (255, 255, 255))
        char_stroke = font.render(char, True, (0, 0, 0))
        char_surfaces.append(char_text)
        char_strokes.append(char_stroke)

    # Calculate total width of text
    total_width = sum(surface.get_width() for surface in char_surfaces)
    spacing = 15  # Increased spacing for larger text
    total_width += spacing * (len(characters) - 1)
    
    # Set up animation parameters
    char_bounce_offsets = [0] * len(characters)
    wave_speed = 2.0  # Controls the speed of the wave
    wave_amplitude = 40  # Controls the height of the bounce
    wave_frequency = 1.5  # Controls how spread out the wave is

    # Animation loop
    start_time = time.time()
    while time.time() - start_time < 6.0:
        current_time = time.time() - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Clear screen and draw background
        screen.blit(background, (0, 0))
        
        # Calculate starting X position to center the text
        start_x = (screen.get_width() - total_width) // 2
        current_x = start_x

        # Update and render each character
        for i in range(len(characters)):
            # Calculate wave offset using sine function
            phase = (current_time * wave_speed) - (i / wave_frequency)
            char_bounce_offsets[i] = abs(math.sin(phase)) * wave_amplitude

            # Draw character stroke with increased thickness
            for dx, dy in [(-8, 0), (8, 0), (0, -8), (0, 8)]:
                pos = (current_x + dx, 
                      screen.get_height()//2 - char_strokes[i].get_height()//2 + dy - char_bounce_offsets[i])
                screen.blit(char_strokes[i], pos)

            # Draw main character
            pos = (current_x,
                  screen.get_height()//2 - char_surfaces[i].get_height()//2 - char_bounce_offsets[i])
            screen.blit(char_surfaces[i], pos)

            # Move to next character position
            current_x += char_surfaces[i].get_width() + spacing

        pygame.display.flip()
        pygame.time.delay(16)

    # Transition to simulation
    import simulation
    simulation.main()