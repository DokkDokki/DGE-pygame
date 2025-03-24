# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Balance Scale Simulation")

# Load the background image
background = pygame.image.load("balancescale/assets/images/testbackground.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Load the base image
base_image = pygame.image.load("balancescale/assets/images/Base.png")
base_image = pygame.transform.scale(base_image, (500, 500))

# Load the scale base image
scale_base_image = pygame.image.load("balancescale/assets/images/scalebase.png")
scale_base_image = pygame.transform.scale(scale_base_image, (500, 500))

# Load the left and right plate images
left_plate_image = pygame.image.load("balancescale/assets/images/plate_left.png")
left_plate_image = pygame.transform.scale(left_plate_image, (500, 500))
right_plate_image = pygame.image.load("balancescale/assets/images/plate_right.png")
right_plate_image = pygame.transform.scale(right_plate_image, (500, 500))

# Load the button image
button_image = pygame.image.load("balancescale/assets/images/button.png")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SOFT_GREEN = (153, 255, 153)
SOFT_YELLOW = (255, 255, 153)
SOFT_RED = (255, 153, 153)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (170, 170, 170)
BUTTON_TEXT_COLOR = BLACK
LEFT_WEIGHT_COLOR = (0, 0, 255)  # Blue for left weights
RIGHT_WEIGHT_COLOR = (255, 0, 0)  # Red for right weights

# Log file
log_file = open("simulation_log.txt", "w")

class BalanceScale:
    def __init__(self, position, size, vertical_scale_height=100):
        self.position = position
        self.size = size
        self.vertical_scale_height = vertical_scale_height
        self.angle = 0
        self.angular_velocity = 0
        self.left_weights = []
        self.right_weights = []
        self.history = []

    def add_weight(self, weight, side):
        if side == "left":
            weight.color = LEFT_WEIGHT_COLOR
            self.left_weights.append(weight)
        elif side == "right":
            weight.color = RIGHT_WEIGHT_COLOR
            self.right_weights.append(weight)
        self.history.append((weight, side))
        log_file.write(f"Added weight {weight.mass} kg to {side} side\n")

    def undo_last_action(self):
        if self.history:
            weight, side = self.history.pop()
            if side == "left":
                self.left_weights.remove(weight)
            elif side == "right":
                self.right_weights.remove(weight)
            log_file.write(f"Removed weight {weight.mass} kg from {side} side\n")

    def update_physics(self, dt):
        left_torque = sum(weight.mass * (self.size / 2) for weight in self.left_weights)
        right_torque = sum(weight.mass * (self.size / 2) for weight in self.right_weights)
        net_torque = right_torque - left_torque
        self.angular_velocity += (net_torque / 1000) * dt  # Adjust the divisor for sensitivity
        self.angle += self.angular_velocity * dt
        self.angle = max(min(self.angle, 45), -45)  # Limit the angle to prevent unrealistic rotation

        # Apply damping to reduce oscillations
        self.angular_velocity *= 0.99

        # If the net torque is very small, set angular velocity to zero to stabilize the scale
        if abs(net_torque) < 0.01 and abs(self.angular_velocity) < 0.01:
            self.angular_velocity = 0

        # Update weights positions
        center = pygame.math.Vector2(self.position)
        for weight in self.left_weights:
            weight.update_position(center, -self.size, self.angle)
        for weight in self.right_weights:
            weight.update_position(center, self.size, self.angle)

    def draw(self, screen):
        center = pygame.math.Vector2(self.position)
        left_arm_end = center + pygame.math.Vector2(-self.size, 0).rotate(self.angle)
        right_arm_end = center + pygame.math.Vector2(self.size, 0).rotate(self.angle)
        
        # Rotate the scale base image
        rotated_scale_base = pygame.transform.rotate(scale_base_image, -self.angle)
        
        # Get the new rect for the rotated image
        scale_base_rect = rotated_scale_base.get_rect(center=center)
        
        # Draw the rotated scale base image
        screen.blit(rotated_scale_base, scale_base_rect.topleft)
        
        # Draw the static base image
        screen.blit(base_image, (center.x - base_image.get_width() // 2, center.y - base_image.get_height() // 2))
        
        # Attach the plates to the edges of the scale base arms
        left_plate_position = center + pygame.math.Vector2(-self.size, 0).rotate(self.angle)
        right_plate_position = center + pygame.math.Vector2(self.size, 0).rotate(self.angle)
        
        # Adjust the position of the plates to ensure they are even
        left_plate_position.y += left_plate_image.get_height() / 20
        right_plate_position.y += right_plate_image.get_height() / 50
        
        left_plate_rect = left_plate_image.get_rect(center=left_plate_position)
        right_plate_rect = right_plate_image.get_rect(center=right_plate_position)
        screen.blit(left_plate_image, left_plate_rect.topleft)
        screen.blit(right_plate_image, right_plate_rect.topleft)

        # Draw each weight on the left and right sides
        for weight in self.left_weights:
            weight.draw(screen)

        for weight in self.right_weights:
            weight.draw(screen)

class Weight:
    def __init__(self, mass, position):
        self.mass = mass
        self.position = pygame.math.Vector2(position)
        self.radius = int(mass * 3)
        self.color = (0, 0, 255)  # Default color

    def update_position(self, center, arm_offset, angle):
        self.position = center + pygame.math.Vector2(arm_offset, 0).rotate(angle)
        self.position.y -= self.radius  # Adjust the position to place the weight on the scale

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

class ImageButton:
    def __init__(self, text, position, size):
        self.text = text
        self.position = position
        self.size = size
        self.image = pygame.transform.scale(button_image, size)
        self.rect = self.image.get_rect(topleft=position)
        self.font = pygame.font.Font(None, 36)
        self.hovered = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.hovered:
                self.hovered = True
                self.image = pygame.transform.scale(button_image, (int(self.size[0] * 1.1), int(self.size[1] * 1.1)))
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            if self.hovered:
                self.hovered = False
                self.image = pygame.transform.scale(button_image, self.size)
                self.rect = self.image.get_rect(topleft=self.position)
        
        screen.blit(self.image, self.rect.topleft)
        text_surf = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def main(scale_size=250, vertical_scale_height=100):
    # Create the balance scale
    scale = BalanceScale((screen_width / 2, screen_height / 3), scale_size, vertical_scale_height)

    # Game state
    running = True
    paused = True
    object_type = "small"  # Initial object type
    small_weights = [0.5, 1, 1.5, 2, 2.5]
    big_weights = [3, 5, 7, 11, 16]
    selected_weight = small_weights[0]  # Initial weight size
    notification_message = ""
    log_file.write("Simulation started\n")

    # Randomly place 1 to 3 big objects on one of the scale arms
    num_initial_weights = random.randint(1, 3)
    for _ in range(num_initial_weights):
        weight_mass = random.choice(big_weights)
        position = pygame.math.Vector2(scale.position) + pygame.math.Vector2(-scale.size / 2, 0).rotate(scale.angle)
        position.y -= weight_mass * 3  # Adjust the position to place the weight on the scale
        scale.add_weight(Weight(weight_mass, position), "left")

    # Font for displaying text
    font = pygame.font.Font(None, 36)

    # Buttons with adjusted sizes
    start_button = ImageButton("Start", (50, 700), (150, 75))
    stop_button = ImageButton("Stop", (250, 700), (150, 75))
    undo_button = ImageButton("Undo", (450, 700), (150, 75))
    reset_button = ImageButton("Reset", (650, 700), (150, 75))

    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(60) / 1000  # Time step in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif start_button.is_clicked(event):
                paused = False
                notification_message = "Simulation started"
                log_file.write("Simulation started\n")
            elif stop_button.is_clicked(event):
                paused = True
                notification_message = "Simulation stopped"
                log_file.write("Simulation stopped\n")
            elif undo_button.is_clicked(event):
                scale.undo_last_action()
                notification_message = "Last action undone"
            elif reset_button.is_clicked(event):
                scale = BalanceScale((screen_width / 2, screen_height / 3), scale_size, vertical_scale_height)
                notification_message = "System reset"
                log_file.write("System reset\n")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                center = pygame.math.Vector2(scale.position)
                if event.button == 1:  # Left click
                    position = center + pygame.math.Vector2(-scale.size / 2, 0).rotate(scale.angle)
                    position.y -= selected_weight * 3  # Adjust the position to place the weight on the scale
                    scale.add_weight(Weight(selected_weight, position), "left")
                elif event.button == 3:  # Right click
                    position = center + pygame.math.Vector2(scale.size / 2, 0).rotate(scale.angle)
                    position.y -= selected_weight * 3  # Adjust the position to place the weight on the scale
                    scale.add_weight(Weight(selected_weight, position), "right")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    object_type = "big"
                    selected_weight = big_weights[0]
                elif event.key == pygame.K_DOWN:
                    object_type = "small"
                    selected_weight = small_weights[0]
                elif event.key == pygame.K_LEFT:
                    if object_type == "small":
                        current_index = small_weights.index(selected_weight)
                        if current_index > 0:
                            selected_weight = small_weights[current_index - 1]
                    else:
                        current_index = big_weights.index(selected_weight)
                        if current_index > 0:
                            selected_weight = big_weights[current_index - 1]
                elif event.key == pygame.K_RIGHT:
                    if object_type == "small":
                        current_index = small_weights.index(selected_weight)
                        if current_index < len(small_weights) - 1:
                            selected_weight = small_weights[current_index + 1]
                    else:
                        current_index = big_weights.index(selected_weight)
                        if current_index < len(big_weights) - 1:
                            selected_weight = big_weights[current_index + 1]
                elif event.key == pygame.K_COMMA:  # "," key
                    center = pygame.math.Vector2(scale.position)
                    position = center + pygame.math.Vector2(-scale.size / 2, 0).rotate(scale.angle)
                    position.y -= selected_weight * 3  # Adjust the position to place the weight on the scale
                    scale.add_weight(Weight(selected_weight, position), "left")
                elif event.key == pygame.K_PERIOD:  # "." key
                    center = pygame.math.Vector2(scale.position)
                    position = center + pygame.math.Vector2(scale.size / 2, 0).rotate(scale.angle)
                    position.y -= selected_weight * 3  # Adjust the position to place the weight on the scale
                    scale.add_weight(Weight(selected_weight, position), "right")

        # Determine the stabilization state
        if abs(scale.angle) < 2 and abs(scale.angular_velocity) < 0.05:
            background_color = SOFT_GREEN  # Softer Green: Stabilized
        elif abs(scale.angle) < 10 and abs(scale.angular_velocity) < 0.2:
            background_color = SOFT_YELLOW  # Softer Yellow: Almost stabilized
        else:
            background_color = SOFT_RED  # Softer Red: Not close

        screen.fill(background_color)  # Clear the screen with the background color
        screen.blit(background, (0, 0))  # Draw the background image

        # Update the physics of the balance scale
        if not paused:
            scale.update_physics(dt)

        # Draw the balance scale
        scale.draw(screen)

        # Draw buttons
        start_button.draw(screen)
        stop_button.draw(screen)
        undo_button.draw(screen)
        reset_button.draw(screen)

        # Display the current selected weight
        weight_text = font.render(f"Selected Weight: {selected_weight} kg", True, BLACK)
        screen.blit(weight_text, (10, 10))

        # Display the current object type
        object_type_text = font.render(f"Object Type: {object_type.capitalize()}", True, BLACK)
        screen.blit(object_type_text, (10, 50))

        # Display the total weight on each side
        left_weight = sum(weight.mass for weight in scale.left_weights)
        right_weight = sum(weight.mass for weight in scale.right_weights)
        left_weight_text = font.render(f"Left Side: {left_weight} kg", True, BLACK)
        right_weight_text = font.render(f"Right Side: {right_weight} kg", True, BLACK)
        screen.blit(left_weight_text, (10, 90))
        screen.blit(right_weight_text, (10, 130))

        # Display the total weight/force on the arm holding the small objects
        small_side = "left" if object_type == "small" else "right"
        small_side_weight = sum(weight.mass for weight in (scale.left_weights if small_side == "left" else scale.right_weights))
        small_side_text = font.render(f"Small Side ({small_side.capitalize()}): {small_side_weight} kg", True, BLACK)
        screen.blit(small_side_text, (10, 170))

        # Display the notification message
        notification_text = font.render(notification_message, True, BLACK)
        screen.blit(notification_text, (10, 210))

        # Update the display
        pygame.display.flip()

    log_file.write("Simulation ended\n")
    log_file.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main(scale_size=250, vertical_scale_height=100)

