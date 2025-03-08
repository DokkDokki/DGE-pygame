import pygame
import sys
from initialize.display import screen, background
from constants import *

# Initialize Pygame
pygame.init()

# Load and scale the center image
center_image = pygame.image.load("balancescale/assets/images/balancescale.png")
center_image = pygame.transform.scale(center_image, (200, 200))
center_image_rect = center_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

# Set up font and text
font = pygame.font.Font("balancescale/assets/fonts/Montserrat-VariableFont_wght.ttf", 60)
text = font.render("Balance Scale", True, (0, 0, 0))
text_rect = text.get_rect(midtop=(screen.get_width() // 2, 50))

# Button properties and functions
button_width = 200
button_height = 100
button_x = screen.get_width() // 2 - button_width // 2
button_y = screen.get_height() // 2 - button_height // 2 + 250

font = pygame.font.Font("balancescale/assets/fonts/Montserrat-VariableFont_wght.ttf", 48)

# Define button colors
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (0, 0, 0)

def draw_button(surface, text, x, y, width, height, color):
    pygame.draw.rect(surface, color, (x, y, width, height))
    pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height), 2)
    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)

def is_button_hovered(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)

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

        screen.blit(background, (0, 0))
        screen.blit(text, text_rect)
        screen.blit(center_image, center_image_rect)

        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        current_color = BUTTON_HOVER_COLOR if is_button_hovered(mouse_pos, button_rect) else BUTTON_COLOR
        draw_button(screen, "Start", button_x, button_y, button_width, button_height, current_color)

        pygame.display.update()

if __name__ == "__main__":
    if welcome_screen():
        import simulation
        simulation.main()
        print("Transitioning to simulation screen...")