import pygame
import sys

# Initialize Pygame
pygame.init()

from initialize import display, caption
from objects import title

# Load and scale the center image
center_image = pygame.image.load("balancescale/assets/images/balancescale.png")
# Adjust the size as needed - for example 200x200 pixels
center_image = pygame.transform.scale(center_image, (200, 200))
# Get the rect for centering
center_image_rect = center_image.get_rect(center=(display.width // 2, display.height // 2))

# Set up font and text
font = pygame.font.Font("balancescale/assets/fonts/Montserrat-VariableFont_wght.ttf", 60)
text = font.render("Balance Scale", True, (0, 0, 0))

# Position from top-center
text_rect = text.get_rect(midtop=(display.width // 2, 50))  # 50 pixels from the top

# -----------------------------------------------------------------------------
# Button properties and functions
# -----------------------------------------------------------------------------
button_width = 200
button_height = 100
button_x = display.width // 2 - button_width // 2
button_y = display.height // 2 - button_height // 2 + 250
button_color = (200, 200, 200)  # Light gray
button_hover_color = (150, 150, 150)  # Darker gray
button_text_color = (0, 0, 0)  # Black

# Font setup for button
font = pygame.font.Font("balancescale/assets/fonts/Montserrat-VariableFont_wght.ttf", 48)

def draw_button(surface, text, x, y, width, height, color):
    pygame.draw.rect(surface, color, (x, y, width, height))
    pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height), 2)  # Button border
    
    text_surface = font.render(text, True, button_text_color)
    text_rect = text_surface.get_rect(center=(x + width//2, y + height//2))
    surface.blit(text_surface, text_rect)

def is_button_hovered(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)

# -----------------------------------------------------------------------------
# Welcome screen function
# -----------------------------------------------------------------------------
def welcome_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                if is_button_hovered(mouse_pos, button_rect):
                    return True

        # Draw background
        display.screen.blit(display.background, (0, 0))
        
        # Draw the "Balance Scale" text
        display.screen.blit(text, text_rect)
        
        # Draw the center image
        display.screen.blit(center_image, center_image_rect)

        # Draw button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        current_color = button_hover_color if is_button_hovered(mouse_pos, button_rect) else button_color
        draw_button(display.screen, "Start", button_x, button_y, button_width, button_height, current_color)

        pygame.display.update()

if __name__ == "__main__":
    if welcome_screen():
        import main
        main.main()
        print("Transitioning to game screen...")