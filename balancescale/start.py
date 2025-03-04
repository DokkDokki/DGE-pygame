import pygame
import sys
import pymunk

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

import pygame
import pymunk
import pymunk.pygame_util
import sys
import random

from objects import draw  # Import the draw module
from objects.scale import BalanceScale  # Import BalanceScale
from objects.weight import Weight, create_initial_weights
from ui.buttons import Button
from ui.status import StatusWindow
from ui.messages import NotificationMessage
from utils import logger, constants

def main():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Balance Scale Simulation")

    # Initialize Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 981)

    # Pymunk draw options
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # --- Game Objects ---
    scale_size = 100  # Initial scale size
    scale = BalanceScale(space, (screen_width / 2, screen_height / 3), scale_size)

    # Initial weights on the left side
    initial_weights = create_initial_weights(space, scale, random.randint(1, 3))

    # --- Game state ---
    running = True
    paused = False
    small_weights = []  # Weights added by the user
    object_type = "small"  # Initial object type
    object_size = constants.SMALL_WEIGHTS[0]  # Initial object size

    # --- Logging ---
    log = logger.setup_logger()
    log.info("Simulation started")

    # --- Button Actions ---
    def start_simulation():
        nonlocal paused
        paused = False
        log.info("Simulation started")

    def stop_simulation():
        nonlocal paused
        paused = True
        log.info("Simulation stopped")

    def undo_last_action():
        nonlocal small_weights
        if small_weights:
            last_weight = small_weights.pop()
            space.remove(last_weight.body, last_weight.shape)
            log.info(f"Undo: Removed weight {last_weight.mass} kg")

    def reset_simulation():
        nonlocal small_weights, scale, initial_weights, space

        # Remove all added weights
        for weight in small_weights:
            space.remove(weight.body, weight.shape)
        small_weights = []

        # Remove the scale
        space.remove(scale.beam_body, scale.beam_shape)
        space.remove(scale.base_body, scale.base_shape)
        space.remove(scale.pivot_body, scale.pivot_shape)
        space.remove(scale.pivot_joint, scale.limit_joint)

        # Remove initial weights
        for weight in initial_weights:
            space.remove(weight.body, weight.shape)
        initial_weights = []

        # Create a new scale
        scale = BalanceScale(space, (screen_width / 2, screen_height / 3), scale_size)

        # Re-create initial weights
        initial_weights = create_initial_weights(space, scale, random.randint(1, 3))

        log.info("Simulation reset")

    # Function to set the object type
    def set_object_type(type):
        nonlocal object_type, object_size
        object_type = type
        if type == "small":
            object_size = constants.SMALL_WEIGHTS[0]
        else:
            object_size = constants.BIG_WEIGHTS[0]
        log.info(f"Object type set to {type}")

    # Function to adjust the object size
    def adjust_object_size(direction):
        nonlocal object_size
        if object_type == "small":
            sizes = constants.SMALL_WEIGHTS
        else:
            sizes = constants.BIG_WEIGHTS
        
        current_index = sizes.index(object_size)
        new_index = current_index + direction
        
        if 0 <= new_index < len(sizes):
            object_size = sizes[new_index]
            log.info(f"Object size adjusted to {object_size} kg")

    # --- UI Elements ---
    start_button = Button(100, 700, 100, 30, "Start", start_simulation)
    stop_button = Button(250, 700, 100, 30, "Stop", stop_simulation)
    undo_button = Button(400, 700, 100, 30, "Undo", undo_last_action)
    reset_button = Button(550, 700, 100, 30, "Reset", reset_simulation)

    status_window = StatusWindow(700, 600, 400, 90) # Adjusted height
    notification_message = NotificationMessage(100, 100, "Welcome to the Balance Scale Simulation!")

    # Setup Pymunk objects
    draw.setup(space, screen_width, screen_height)  # Initialize the balance scale

    # --- Main Game Loop ---
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                start_button.check_click(mouse_pos)
                stop_button.check_click(mouse_pos)
                undo_button.check_click(mouse_pos)
                reset_button.check_click(mouse_pos)

                # Add a weight on the right side with left click
                if event.button == 1:  # Left click
                    mass = object_size
                    arm_position = scale.get_arm_position("right")
                    position = (arm_position.x + random.uniform(-20, 20), arm_position.y - 20)
                    weight = Weight(space, position, mass)
                    small_weights.append(weight)
                    log.info(f"Added weight {mass} kg to the right side")

                # Add a weight on the left side with right click
                elif event.button == 3:  # Right click
                    mass = object_size
                    arm_position = scale.get_arm_position("left")
                    position = (arm_position.x + random.uniform(-20, 20), arm_position.y - 20)
                    weight = Weight(space, position, mass)
                    small_weights.append(weight)
                    log.info(f"Added weight {mass} kg to the left side")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    adjust_object_size(-1)  # Decrease size
                elif event.key == pygame.K_RIGHT:
                    adjust_object_size(1)  # Increase size
                elif event.key == pygame.K_UP:
                    set_object_type("small")  # Select small size
                elif event.key == pygame.K_DOWN:
                    set_object_type("big")  # Select big size

        # --- Drawing ---
        screen.fill(constants.WHITE)  # Clear the screen

        # Draw game objects
        scale.draw(screen, draw_options)
        for weight in initial_weights + small_weights:
            weight.draw(screen, draw_options)

        # Draw UI elements
        start_button.draw(screen)
        stop_button.draw(screen)
        undo_button.draw(screen)
        reset_button.draw(screen)

        # Calculate total weight on the right arm
        total_weight = sum(weight.mass for weight in small_weights)
        status_window.draw(screen, total_weight, object_size)

        # Draw the selected object type
        object_type_text = f"Selected Size: {object_type.capitalize()}"
        font = pygame.font.Font(None, 36)
        object_type_surface = font.render(object_type_text, True, constants.BLACK)
        screen.blit(object_type_surface, (screen_width - 250, 50))

        # Determine stabilization state
        weight_difference = abs(total_weight - sum(w.mass for w in initial_weights))
        if weight_difference < 1:
            stabilization_color = constants.GREEN
        elif weight_difference < 3:
            stabilization_color = constants.YELLOW
        else:
            stabilization_color = constants.RED

        # Draw stabilization color indicator
        pygame.draw.circle(screen, stabilization_color, (1100, 50), 20)

        notification_message.draw(screen)

        # --- Physics Update ---
        if not paused:
            draw.draw(space, screen, draw_options)  # Step the simulation

        # --- Update Display ---