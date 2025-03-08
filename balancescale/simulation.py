import pygame
import random
import sys
from datetime import datetime

class Scale:
    def __init__(self, size):
        self.size = size
        self.left_arm = []
        self.right_arm = []
        self.left_arm_weight = 0
        self.right_arm_weight = 0
        self.angle = 0
        self.angular_velocity = 0
        self.status = "Not close"
        self.log = []

    def add_weight(self, weight, side):
        if side == 'left':
            self.left_arm.append(weight)
            self.left_arm_weight += weight
        elif side == 'right':
            self.right_arm.append(weight)
            self.right_arm_weight += weight
        self.update_physics()
        self.update_status()

    def update_physics(self):
        torque_left = self.left_arm_weight * self.size
        torque_right = self.right_arm_weight * self.size
        net_torque = torque_right - torque_left
        self.angular_velocity += net_torque / 1000  # Adjust the divisor for sensitivity
        self.angle += self.angular_velocity
        self.angle = max(min(self.angle, 45), -45)  # Limit the angle to prevent unrealistic rotation

    def update_status(self):
        if abs(self.left_arm_weight - self.right_arm_weight) < 1:
            self.status = "Stabilized"
        elif abs(self.left_arm_weight - self.right_arm_weight) < 3:
            self.status = "Almost stabilized"
        else:
            self.status = "Not close"

    def draw(self, surface):
        # Draw the scale base
        pygame.draw.rect(surface, (0, 0, 0), (450, 290, 100, 20))  # Shortened base
        # Draw the scale arms with rotation
        center = pygame.math.Vector2(500, 300)
        left_arm_end = center + pygame.math.Vector2(-self.size * 50, 0).rotate(self.angle)  # Shortened arms
        right_arm_end = center + pygame.math.Vector2(self.size * 50, 0).rotate(self.angle)  # Shortened arms
        pygame.draw.line(surface, (0, 0, 0), center, left_arm_end, 5)
        pygame.draw.line(surface, (0, 0, 0), center, right_arm_end, 5)
        # Draw the supporting frame
        pygame.draw.line(surface, (0, 0, 0), (500, 300), (500, 400), 5)

        # Draw the weights
        for i, weight in enumerate(self.left_arm):
            weight_pos = center + pygame.math.Vector2(-self.size * 25, 0).rotate(self.angle)
            pygame.draw.circle(surface, (0, 0, 255), weight_pos, int(weight * 3))  # Smaller weight balls
        for i, weight in enumerate(self.right_arm):
            weight_pos = center + pygame.math.Vector2(self.size * 25, 0).rotate(self.angle)
            pygame.draw.circle(surface, (0, 0, 255), weight_pos, int(weight * 3))  # Smaller weight balls

        font = pygame.font.Font(None, 36)
        left_weight_text = font.render(f"Left Weight: {self.left_arm_weight} kg", True, (0, 0, 0))
        right_weight_text = font.render(f"Right Weight: {self.right_arm_weight} kg", True, (0, 0, 0))
        surface.blit(left_weight_text, (10, 50))
        surface.blit(right_weight_text, (10, 90))

    def draw_status(self, surface):
        # Draw the status
        font = pygame.font.Font(None, 36)
        status_text = font.render(f"Status: {self.status}", True, (0, 0, 0))
        surface.blit(status_text, (10, 10))

    def log_activity(self, activity):
        self.log.append(f"{datetime.now()}: {activity}")

    def save_log(self):
        with open("balancescale_log.txt", "w") as file:
            for entry in self.log:
                file.write(entry + "\n")

class Object:
    def __init__(self, weight, side):
        self.weight = weight
        self.side = side
        self.x = 450 if side == 'left' else 550
        self.y = 250

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, 255), (self.x, self.y), int(self.weight * 3))  # Smaller weight balls

def create_random_objects():
    big_weights = [3, 5, 7, 11, 16]
    small_weights = [0.5, 1, 1.5, 2, 2.5]
    objects = []

    # Add 1 to 3 big objects to the left arm
    for _ in range(random.randint(1, 3)):
        weight = random.choice(big_weights)
        objects.append(Object(weight, 'left'))

    return objects

def draw_button(surface, text, x, y, width, height, color):
    pygame.draw.rect(surface, color, (x, y, width, height))
    pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height), 2)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)

def main():
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Balance Scale Simulation")

    scale = Scale(size=50)  # Adjusted size for shorter arms
    objects = create_random_objects()

    button_width = 150
    button_height = 50
    button_x = 10
    button_y = 500
    button_color = (200, 200, 200)
    button_hover_color = (150, 150, 150)

    selected_weight = 0.5
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scale.save_log()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    scale.log_activity("Simulation started")
                    # Add logic to start the simulation
                elif button_x <= mouse_pos[0] <= button_x + button_width and button_y + 60 <= mouse_pos[1] <= button_y + 60 + button_height:
                    scale.log_activity("Simulation stopped")
                    # Add logic to stop the simulation
                elif button_x <= mouse_pos[0] <= button_x + button_width and button_y + 120 <= mouse_pos[1] <= button_y + 120 + button_height:
                    scale.log_activity("Undo last action")
                    # Add logic to undo the last action
                elif button_x <= mouse_pos[0] <= button_x + button_width and button_y + 180 <= mouse_pos[1] <= button_y + 180 + button_height:
                    scale.log_activity("Simulation reset")
                    # Add logic to reset the simulation
                elif 600 <= mouse_pos[0] <= 650 and 50 <= mouse_pos[1] <= 100:
                    selected_weight = 0.5
                elif 660 <= mouse_pos[0] <= 710 and 50 <= mouse_pos[1] <= 100:
                    selected_weight = 1
                elif 720 <= mouse_pos[0] <= 770 and 50 <= mouse_pos[1] <= 100:
                    selected_weight = 1.5
                elif 780 <= mouse_pos[0] <= 830 and 50 <= mouse_pos[1] <= 100:
                    selected_weight = 2
                elif 840 <= mouse_pos[0] <= 890 and 50 <= mouse_pos[1] <= 100:
                    selected_weight = 2.5
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_weight = 0.5
                elif event.key == pygame.K_2:
                    selected_weight = 1
                elif event.key == pygame.K_3:
                    selected_weight = 1.5
                elif event.key == pygame.K_4:
                    selected_weight = 2
                elif event.key == pygame.K_5:
                    selected_weight = 2.5

        screen.fill((255, 255, 255))  # Clear screen with white background
        scale.draw(screen)
        scale.draw_status(screen)
        for obj in objects:
            obj.draw(screen)

        draw_button(screen, "Start", button_x, button_y, button_width, button_height, button_color)
        draw_button(screen, "Stop", button_x, button_y + 60, button_width, button_height, button_color)
        draw_button(screen, "Undo", button_x, button_y + 120, button_width, button_height, button_color)
        draw_button(screen, "Reset", button_x, button_y + 180, button_width, button_height, button_color)

        # Draw weight selection buttons
        pygame.draw.circle(screen, (255, 0, 0), (625, 75), 25)
        pygame.draw.circle(screen, (255, 0, 0), (685, 75), 25)
        pygame.draw.circle(screen, (255, 0, 0), (745, 75), 25)
        pygame.draw.circle(screen, (255, 0, 0), (805, 75), 25)
        pygame.draw.circle(screen, (255, 0, 0), (865, 75), 25)

        # Draw indicator for selected weight
        if selected_weight == 0.5:
            pygame.draw.circle(screen, (0, 255, 0), (625, 75), 10)
        elif selected_weight == 1:
            pygame.draw.circle(screen, (0, 255, 0), (685, 75), 10)
        elif selected_weight == 1.5:
            pygame.draw.circle(screen, (0, 255, 0), (745, 75), 10)
        elif selected_weight == 2:
            pygame.draw.circle(screen, (0, 255, 0), (805, 75), 10)
        elif selected_weight == 2.5:
            pygame.draw.circle(screen, (0, 255, 0), (865, 75), 10)

        font = pygame.font.Font(None, 36)
        weight_text = font.render(f"Selected Size: {selected_weight} kg", True, (0, 0, 0))
        screen.blit(weight_text, (900, 50))

        pygame.display.update()

if __name__ == "__main__":
    main()