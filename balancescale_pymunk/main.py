import pygame
import pymunk
import sys
import random

from objects.weight import Weight, create_initial_weights
from ui.buttons import Button
from ui.status import StatusWindow
from ui.messages import NotificationMessage
from utils import logger, constants

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def main():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Balance Scale Simulation")

    # Initialize Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 981)

    # --- Game Objects ---
    scale_size = 250  # Adjust the size to change the length of the beam
    pivot_x = screen_width // 2
    pivot_y = screen_height // 3

    # Initial weights on the left side
    initial_weights = create_initial_weights(space, pivot_x, pivot_y, scale_size, random.randint(1, 3))

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
        nonlocal small_weights, initial_weights, space

        # Remove all added weights
        for weight in small_weights:
            space.remove(weight.body, weight.shape)
        small_weights = []

        # Remove initial weights
        for weight in initial_weights:
            space.remove(weight.body, weight.shape)
        initial_weights = []

        # Re-create initial weights
        initial_weights = create_initial_weights(space, pivot_x, pivot_y, scale_size, random.randint(1, 3))

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

    # Function to draw the balance scale
    def draw_balance_scale():
        # Draw the pivot
        pygame.draw.circle(screen, BLACK, (pivot_x, pivot_y), 10)

        # Draw the beam
        left_end = (pivot_x - scale_size // 2, pivot_y)
        right_end = (pivot_x + scale_size // 2, pivot_y)
        pygame.draw.line(screen, BLACK, left_end, right_end, 10)

        # Draw the left and right pans
        pan_width = 50
        pan_height = 10
        left_pan = (left_end[0] - pan_width // 2, left_end[1] + pan_height)
        right_pan = (right_end[0] - pan_width // 2, right_end[1] + pan_height)
        pygame.draw.rect(screen, BLACK, (*left_pan, pan_width, pan_height))
        pygame.draw.rect(screen, BLACK, (*right_pan, pan_width, pan_height))

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
                    position = (pivot_x + scale_size // 2 + random.uniform(-20, 20), pivot_y - 20)
                    weight = Weight(space, position, mass)
                    small_weights.append(weight)
                    log.info(f"Added weight {mass} kg to the right side")

                # Add a weight on the left side with right click
                elif event.button == 3:  # Right click
                    mass = object_size
                    position = (pivot_x - scale_size // 2 + random.uniform(-20, 20), pivot_y - 20)
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
        screen.fill(WHITE)  # Clear the screen

        # Draw the balance scale
        draw_balance_scale()

        # Draw weights
        for weight in initial_weights + small_weights:
            weight.draw(screen)

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
        object_type_surface = font.render(object_type_text, True, BLACK)
        screen.blit(object_type_surface, (screen_width - 300, 20))  # Adjusted position to top right

        # Determine stabilization state
        weight_difference = abs(total_weight - sum(w.mass for w in initial_weights))
        if weight_difference < 1:
            stabilization_color = GREEN
        elif weight_difference < 3:
            stabilization_color = constants.YELLOW
        else:
            stabilization_color = RED

        # Draw stabilization color indicator
        pygame.draw.circle(screen, stabilization_color, (screen_width - 350, 50), 20)  # Adjusted position to avoid overlap

        notification_message.draw(screen)

        # --- Physics Update ---
        if not paused:
            space.step(1 / 60.0)  # Step the simulation

        # --- Update Display ---
        pygame.display.flip()

        # --- Limit frame rate ---
        pygame.time.Clock().tick(60)

    # --- End of Game ---
    log.info("Simulation ended")
    log.info("--- System Log ---")
    log.info(logger.get_log_content())
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()