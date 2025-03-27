import pygame
import sys
import math
import loading  # Import the loading module
from initialize.display import screen, background
from constants import *

# Initialize Pygame
pygame.init()

# Load and play background music
pygame.mixer.music.load("balancescale/assets/sounds/BGM2.mp3")
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Function to adjust the volume
def set_volume(volume):
    pygame.mixer.music.set_volume(volume)

# Load and scale the center image with adjusted size and position
center_image = pygame.image.load("balancescale/assets/images/balancescale.png")
center_image = pygame.transform.scale(center_image, (500, 500))  # Increased size
center_image_rect = center_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))  # Adjusted position

# Set up font and text with optimized size
font = pygame.font.Font("balancescale/assets/fonts/MISHIMISHI-BLOCK.otf", 156)  # Slightly increased
full_text = "バランススケール"
text_stroke = font.render(full_text, True, (0, 0, 0))
text_rect = text_stroke.get_rect(midtop=(screen.get_width() // 2, 80))  # Increased top margin

# Adjust stroke size for better visibility
text_surface = pygame.Surface((text_rect.width + 8, text_rect.height + 8), pygame.SRCALPHA)
text_surface.fill((0, 0, 0, 0))  # Fill with transparent color

# Load and scale the button image with better proportions
button_image = pygame.image.load("balancescale/assets/images/button.png")
button_image = pygame.transform.scale(button_image, (400, 290))  # Adjusted size
button_rect = button_image.get_rect(center=(screen.get_width() // 2, screen.get_height() - 150))  # Adjusted position

# Render the button text with larger size
button_font = pygame.font.Font("balancescale/assets/fonts/MISHIMISHI-BLOCK.otf", 60)  # Increased size
button_text = button_font.render("スタート", True, (255, 255, 255))
button_text_stroke = button_font.render("スタート", True, (0, 0, 0))
button_text_rect = button_text.get_rect(center=(button_image.get_width() // 2, button_image.get_height() // 2))

# Create a new surface for the button text with thicker stroke
button_text_surface = pygame.Surface((button_text_rect.width + 6, button_text_rect.height + 6), pygame.SRCALPHA)
button_text_surface.fill((0, 0, 0, 0))  # Fill with transparent color

# Blit the stroke text onto the surface
for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
    button_text_surface.blit(button_text_stroke, (2 + dx, 2 + dy))

# Blit the main text onto the surface
button_text_surface.blit(button_text, (2, 2))

# Blit the text surface onto the button image
button_image.blit(button_text_surface, (button_image.get_width() // 2 - button_text_surface.get_width() // 2, button_image.get_height() // 2 - button_text_surface.get_height() // 2))

# Load sound effects
hover_sound = pygame.mixer.Sound("balancescale/assets/sounds/Hover.mp3")
click_sound = pygame.mixer.Sound("balancescale/assets/sounds/Clicked.mp3")

# Load and scale the background image to fit the screen
background_image = pygame.image.load("balancescale/assets/images/BG.png")
background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

def is_button_hovered(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)

def welcome_screen():
    # Load and scale background image
    background_image = pygame.image.load("balancescale/assets/images/BG.png")
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    # Add wave animation parameters
    wave_height = 12  # Height of the wave
    wave_speed = 400  # Speed of the wave animation

    running = True
    button_hovered = False
    text_index = 0
    text_speed = 0.1
    last_update_time = pygame.time.get_ticks()

    # Pre-calculate character widths
    char_widths = [font.render(char, True, (255, 255, 255)).get_width() for char in full_text]
    
    while running:
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > text_speed * 750:
            text_index = min(text_index + 1, len(full_text))
            last_update_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_button_hovered(mouse_pos, button_rect):
                    click_sound.play()
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    loading.loading_screen()
                    return True

        # Draw background image instead of solid color
        screen.blit(background_image, (0, 0))
        screen.blit(center_image, center_image_rect)
        
        # Animate title text
        animated_text = full_text[:text_index]
        
        # Calculate total width of visible text
        total_width = sum(char_widths[:text_index])
        start_x = (screen.get_width() - total_width) // 2
        
        # Keep track of current x position
        current_x = start_x
        
        # Draw each character
        for i, char in enumerate(animated_text):
            # Create character surfaces
            char_surface = font.render(char, True, (255, 255, 255))
            char_stroke = font.render(char, True, (0, 0, 0))
            
            # Smoother wave effect
            char_y = 80 + int(wave_height * math.sin(pygame.time.get_ticks() / wave_speed + i * 0.5))
            
            # Thicker stroke for better visibility
            for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4), (-3, -3), (3, 3), (-3, 3), (3, -3)]:
                screen.blit(char_stroke, (current_x + dx, char_y + dy))
            
            # Draw main character
            screen.blit(char_surface, (current_x, char_y))
            
            # Move x position for next character
            current_x += char_widths[i]

        # Draw button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        if is_button_hovered(mouse_pos, button_rect):
            if not button_hovered:
                hover_sound.play()
                button_hovered = True
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            scale_factor = 1.15  # Slightly reduced scale factor
            hover_button_image = pygame.transform.scale(button_image, 
                (int(320 * scale_factor), int(220 * scale_factor)))
            hover_button_image.set_alpha(240)  # Slightly more opaque
            hover_button_rect = hover_button_image.get_rect(center=button_rect.center)
            screen.blit(hover_button_image, hover_button_rect)
        else:
            if button_hovered:
                button_hovered = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            screen.blit(button_image, button_rect)

        pygame.display.update()

if __name__ == "__main__":
    set_volume(0.07)  # Set initial volume to 50%
    if welcome_screen():
        print("Transitioning to simulation screen...")