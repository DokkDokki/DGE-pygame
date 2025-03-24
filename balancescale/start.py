import pygame
import sys
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

# Load and scale the center image
center_image = pygame.image.load("balancescale/assets/images/balancescale.png")
center_image = pygame.transform.scale(center_image, (350, 350))
center_image_rect = center_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

# Set up font and text
font = pygame.font.Font("balancescale/assets/fonts/MISHIMISHI-BLOCK.otf", 97)
full_text = "バランススケール"
text_stroke = font.render(full_text, True, (0, 0, 0))
text_rect = text_stroke.get_rect(midtop=(screen.get_width() // 2, 50))

# Create a new surface for the text with stroke
text_surface = pygame.Surface((text_rect.width + 4, text_rect.height + 4), pygame.SRCALPHA)
text_surface.fill((0, 0, 0, 0))  # Fill with transparent color

# Load the button image
button_image = pygame.image.load("balancescale/assets/images/button.png")
button_image = pygame.transform.scale(button_image, (300, 210))
button_rect = button_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 250))

# Render the button text with stroke
button_font = pygame.font.Font("balancescale/assets/fonts/MISHIMISHI-BLOCK.otf", 40)
button_text = button_font.render("スタート", True, (255, 255, 255))
button_text_stroke = button_font.render("スタート", True, (0, 0, 0))
button_text_rect = button_text.get_rect(center=(button_image.get_width() // 2, button_image.get_height() // 2))

# Create a new surface for the button text with stroke
button_text_surface = pygame.Surface((button_text_rect.width + 4, button_text_rect.height + 4), pygame.SRCALPHA)
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

def is_button_hovered(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)

def welcome_screen():
    running = True
    button_hovered = False
    text_index = 0
    text_speed = 0.1  # Adjust this value to control the speed of the text animation
    last_update_time = pygame.time.get_ticks()

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
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Change cursor back to arrow
                    loading.loading_screen()  # Call the loading screen function
                    return True

        screen.blit(background, (0, 0))
        
        # Render the text with animation
        animated_text = full_text[:text_index]
        text = font.render(animated_text, True, (255, 255, 255))
        text_stroke = font.render(animated_text, True, (0, 0, 0))
        
        text_surface.fill((0, 0, 0, 0))  # Clear the surface
        for dx, dy in [(-6, 0), (6, 0), (0, -6), (0, 6)]:
            text_surface.blit(text_stroke, (2 + dx, 2 + dy))
        text_surface.blit(text, (2, 2))
        
        screen.blit(text_surface, text_rect.topleft)
        screen.blit(center_image, center_image_rect)

        mouse_pos = pygame.mouse.get_pos()
        if is_button_hovered(mouse_pos, button_rect):
            if not button_hovered:
                hover_sound.play()
                button_hovered = True
            # Change cursor to hand cursor
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            # Increase the size of the button and lower the opacity
            hover_button_image = pygame.transform.scale(button_image, (int(300 * 1.2), int(210 * 1.2)))
            hover_button_image.set_alpha(int(255 * 0.92))  # Lower opacity by 8%
            hover_button_rect = hover_button_image.get_rect(center=button_rect.center)
            screen.blit(hover_button_image, hover_button_rect)
        else:
            if button_hovered:
                button_hovered = False
            # Change cursor to default cursor
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            screen.blit(button_image, button_rect)

        pygame.display.update()

if __name__ == "__main__":
    set_volume(0.07)  # Set initial volume to 50%
    if welcome_screen():
        print("Transitioning to simulation screen...")