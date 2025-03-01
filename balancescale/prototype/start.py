import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Balance Scale Simulation")

# Load images
scale_image = pygame.image.load("balancescale/assets/balancescale.png")
weight_image = pygame.image.load("balancescale/assets/logo.png")

# Scale properties
scale_x = screen_width // 2 - scale_image.get_width() // 2
scale_y = screen_height // 4
scale_weight_left = 0
scale_weight_right = 0

# Weight properties
weight_x_left = scale_x - weight_image.get_width()
weight_y_left = scale_y + scale_image.get_height() // 2
weight_x_right = scale_x + scale_image.get_width()
weight_y_right = scale_y + scale_image.get_height() // 2
weight_left = 0
weight_right = 0

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                weight_left += 1
            elif event.key == pygame.K_RIGHT:
                weight_right += 1

    # Update scale weight
    scale_weight_left = weight_left * 0.5
    scale_weight_right = weight_right * 0.5

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the scale
    screen.blit(scale_image, (scale_x, scale_y))

    # Draw the weights
    for i in range(weight_left):
        screen.blit(weight_image, (weight_x_left, weight_y_left - i * weight_image.get_height()))
    for i in range(weight_right):
        screen.blit(weight_image, (weight_x_right, weight_y_right - i * weight_image.get_height()))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()