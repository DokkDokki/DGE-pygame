import pygame
import sys
import numpy as np
import pymunk
import time
import math
from constants import *
from initialize.display import screen, background

# Initialize Pygame
pygame.init()
rng = np.random.default_rng()

# Get screen dimensions from the imported screen
WIDTH = screen.get_width()
HEIGHT = screen.get_height()

# Constants
PAD = (24, 160)
A = (PAD[0], PAD[1])
B = (PAD[0], HEIGHT - PAD[0])
C = (WIDTH - PAD[0], HEIGHT - PAD[0])
D = (WIDTH - PAD[0], PAD[1])
BG_COLOR = (255, 240, 148)
W_COLOR = (255, 190, 58)
COLORS = [
    (245, 0, 0),
    (250, 100, 100),
    (150, 20, 250),
    (250, 210, 10),
    (250, 150, 0),
    (245, 0, 0),
    (250, 250, 100),
    (255, 180, 180),
    (255, 255, 0),
    (100, 235, 10),
]

FPS = 240
RADII = [17, 25, 32, 38, 45, 55, 64, 75, 87, 100]  # Particle sizes
THICKNESS = 15     # Wall thickness
DENSITY = 0.001    # Particle density
ELASTICITY = 0.1   # Bounce factor
IMPULSE = 10000    # Force applied
GRAVITY = 2000     # Gravity strength
DAMPING = 0.8      # Energy loss factor
NEXT_DELAY = FPS
NEXT_STEPS = 20
BIAS = 0.00001
POINTS = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
WEIGHT_MULTIPLIER = 0.1  # Conversion factor for KG

shape_to_particle = dict()

# Define the specific size values
SIZE_VALUES = [0.5, 1, 1.5, 2, 2.5, 3, 5, 7, 11, 16]

class Particle:
    def __init__(self, pos, n, space, mapper):
        self.n = n % 11
        self.radius = RADII[self.n]
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = tuple(pos)
        self.shape = pymunk.Circle(body=self.body, radius=self.radius)
        self.shape.density = DENSITY
        self.shape.elasticity = ELASTICITY
        self.shape.collision_type = 1
        self.shape.friction = 0.2
        self.has_collided = False
        mapper[self.shape] = self
        space.add(self.body, self.shape)
        self.alive = True

    def draw(self, screen):
        if self.alive:
            c1 = np.array(COLORS[self.n])
            c2 = (c1 * 0.8).astype(int)
            pygame.draw.circle(screen, tuple(c2), self.body.position, self.radius)
            pygame.draw.circle(screen, tuple(c1), self.body.position, self.radius * 0.9)

    def kill(self, space):
        space.remove(self.body, self.shape)
        self.alive = False

    @property
    def pos(self):
        return np.array(self.body.position)

class PreParticle:
    def __init__(self, x, n):
        self.n = n % 11
        self.radius = RADII[self.n]
        self.x = x

    def draw(self, screen):
        c1 = np.array(COLORS[self.n])
        c2 = (c1 * 0.8).astype(int)
        pygame.draw.circle(screen, tuple(c2), (self.x, PAD[1] // 2), self.radius)
        pygame.draw.circle(screen, tuple(c1), (self.x, PAD[1] // 2), self.radius * 0.9)

    def set_x(self, x):
        lim = PAD[0] + self.radius + THICKNESS // 2
        self.x = np.clip(x, lim, WIDTH - lim)

    def release(self, space, mapper):
        return Particle((self.x, PAD[1] // 2), self.n, space, mapper)

# Update these constants to make the scale bar larger
SCALE_WIDTH = 900  # New width of the scale bar (700 + 40)
SCALE_HEIGHT = 300 # Height of the scale bar remains the same
SCALE_POS = (WIDTH // 2, HEIGHT // 2 + 50)  # Adjusted center position of the scale
SCALE_LEFT = SCALE_POS[0] - SCALE_WIDTH // 2
SCALE_RIGHT = SCALE_POS[0] + SCALE_WIDTH // 2
MAX_ANGLE = 12  # Maximum tilt angle in degrees

# Add this after the space initialization
def create_scale(space):
    # Create dynamic body for the scale
    body = pymunk.Body(mass=1000, moment=pymunk.moment_for_segment(1000, (-SCALE_WIDTH//2, 0), (SCALE_WIDTH//2, 0), THICKNESS))
    body.position = SCALE_POS
    
    # Pin joint to fix the center in place while allowing rotation
    joint = pymunk.PinJoint(space.static_body, body, (SCALE_POS[0], SCALE_POS[1]), (0, 0))
    
    # Create the segment shape for the scale bar
    shape = pymunk.Segment(body, (-SCALE_WIDTH//2, 0), (SCALE_WIDTH//2, 0), THICKNESS)
    shape.friction = 0.5
    shape.elasticity = ELASTICITY
    shape.collision_type = 2
    
    # Create the rectangular shape for the scale bar
    scale_bar_shape = pymunk.Poly.create_box(body, (SCALE_WIDTH, THICKNESS))
    scale_bar_shape.friction = 0.5
    scale_bar_shape.elasticity = ELASTICITY
    scale_bar_shape.collision_type = 2
    
    # NEW: Add invisible walls on the left plate to catch balls
    left_plate_width = 120
    left_plate_height = 40
    left_wall_height = 80  # Higher walls to prevent balls from escaping
    
    # Left plate floor (horizontal barrier)
    left_plate_floor = pymunk.Segment(
        body, 
        (-SCALE_WIDTH//2 - left_plate_width//2, -THICKNESS), 
        (-SCALE_WIDTH//2 + left_plate_width//2, -THICKNESS), 
        5
    )
    left_plate_floor.friction = 0.9  # High friction to prevent sliding
    
    # Left plate left wall (vertical barrier)
    left_plate_left_wall = pymunk.Segment(
        body, 
        (-SCALE_WIDTH//2 - left_plate_width//2, -THICKNESS), 
        (-SCALE_WIDTH//2 - left_plate_width//2, -THICKNESS - left_wall_height), 
        5
    )
    left_plate_left_wall.friction = 0.9
    
    # Left plate right wall (vertical barrier)
    left_plate_right_wall = pymunk.Segment(
        body, 
        (-SCALE_WIDTH//2 + left_plate_width//2, -THICKNESS), 
        (-SCALE_WIDTH//2 + left_plate_width//2, -THICKNESS - left_wall_height), 
        5
    )
    left_plate_right_wall.friction = 0.9
    
    # NEW: Add invisible walls on the right plate to catch balls
    right_plate_width = 120
    
    # Right plate floor (horizontal barrier)
    right_plate_floor = pymunk.Segment(
        body, 
        (SCALE_WIDTH//2 - right_plate_width//2, -THICKNESS), 
        (SCALE_WIDTH//2 + right_plate_width//2, -THICKNESS), 
        5
    )
    right_plate_floor.friction = 0.9
    
    # Right plate left wall (vertical barrier)
    right_plate_left_wall = pymunk.Segment(
        body, 
        (SCALE_WIDTH//2 - right_plate_width//2, -THICKNESS), 
        (SCALE_WIDTH//2 - right_plate_width//2, -THICKNESS - left_wall_height), 
        5
    )
    right_plate_left_wall.friction = 0.9
    
    # Right plate right wall (vertical barrier)
    right_plate_right_wall = pymunk.Segment(
        body, 
        (SCALE_WIDTH//2 + right_plate_width//2, -THICKNESS), 
        (SCALE_WIDTH//2 + right_plate_width//2, -THICKNESS - left_wall_height), 
        5
    )
    right_plate_right_wall.friction = 0.9
    
    # Add all shapes to the space
    space.add(body, shape, scale_bar_shape, joint,
              left_plate_floor, left_plate_left_wall, left_plate_right_wall,
              right_plate_floor, right_plate_left_wall, right_plate_right_wall)
    
    return body, shape

class Scale:
    def __init__(self, body):
        # Load the scale platform image
        self.image = pygame.image.load("balancescale/assets/images/scalebase.png")
        self.image = pygame.transform.scale(self.image, (SCALE_WIDTH, SCALE_HEIGHT))
        self.rect = self.image.get_rect(center=SCALE_POS)
        
        # Load the base image
        try:
            self.base_image = pygame.image.load("balancescale/assets/images/Base.png")
            base_width = 150
            base_height = 180
            self.base_image = pygame.transform.scale(self.base_image, (base_width, base_height))
            self.base_rect = self.base_image.get_rect(center=SCALE_POS)
        except Exception as e:
            print(f"Error loading base image: {e}")
            self.base_image = pygame.Surface((150, 180))
            self.base_image.fill((150, 100, 50))
            self.base_rect = self.base_image.get_rect(center=SCALE_POS)
        
        # Add left and right plates
        try:
            # Create smaller plates that will fit at the edges
            self.plate_image = pygame.image.load("balancescale/assets/images/plate_left.png")
            plate_width = 500  
            plate_height = 250  
            self.plate_image = pygame.transform.scale(self.plate_image, (plate_width, plate_height))
            
            # Position them EXACTLY at the left and right edges
            self.left_plate_pos = (SCALE_POS[0] - SCALE_WIDTH//2, SCALE_POS[1] - THICKNESS)
            self.right_plate_pos = (SCALE_POS[0] + SCALE_WIDTH//2, SCALE_POS[1] - THICKNESS)
        except Exception as e:
            print(f"Error loading plate image: {e}")
            plate_width = 120
            plate_height = 40
            self.plate_image = pygame.Surface((plate_width, plate_height))
            self.plate_image.fill((200, 170, 100))  # Tan color for plates
            self.left_plate_pos = (SCALE_POS[0] - SCALE_WIDTH//2, SCALE_POS[1] - THICKNESS)
            self.right_plate_pos = (SCALE_POS[0] + SCALE_WIDTH//2, SCALE_POS[1] - THICKNESS)
        
        self.body = body
        
    def draw(self, screen):
        # Get the angle from the physics body in degrees
        angle_degrees = math.degrees(self.body.angle)
        angle_rad = self.body.angle
        
        # Rotate the scale platform image
        rotated_image = pygame.transform.rotate(self.image, -angle_degrees)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        
        # Draw the scale platform first
        screen.blit(rotated_image, new_rect.topleft)
        
        # Calculate rotated positions for the plates
        # Left plate
        left_offset_x = self.left_plate_pos[0] - SCALE_POS[0]
        left_offset_y = self.left_plate_pos[1] - SCALE_POS[1]
        rotated_left_x = SCALE_POS[0] + left_offset_x * math.cos(angle_rad) - left_offset_y * math.sin(angle_rad)
        rotated_left_y = SCALE_POS[1] + left_offset_x * math.sin(angle_rad) + left_offset_y * math.cos(angle_rad)
        
        # Right plate
        right_offset_x = self.right_plate_pos[0] - SCALE_POS[0]
        right_offset_y = self.right_plate_pos[1] - SCALE_POS[1]
        rotated_right_x = SCALE_POS[0] + right_offset_x * math.cos(angle_rad) - right_offset_y * math.sin(angle_rad)
        rotated_right_y = SCALE_POS[1] + right_offset_x * math.sin(angle_rad) + right_offset_y * math.cos(angle_rad)
        
        # Rotate the plate images
        rotated_plate = pygame.transform.rotate(self.plate_image, -angle_degrees)
        
        # Draw the plates
        left_plate_rect = rotated_plate.get_rect(center=(rotated_left_x, rotated_left_y))
        right_plate_rect = rotated_plate.get_rect(center=(rotated_right_x, rotated_right_y))
        screen.blit(rotated_plate, left_plate_rect.topleft)
        screen.blit(rotated_plate, right_plate_rect.topleft)
        
        # Draw the base last (on top)
        screen.blit(self.base_image, self.base_rect.topleft)
        
    def calculate_weight_distribution(self, particles):
        left_weight = 0
        right_weight = 0
        total_weight = 0
        center_x = SCALE_POS[0]
        
        # First calculate total weight
        for particle in particles:
            if particle.alive:
                weight = particle.radius * WEIGHT_MULTIPLIER
                total_weight += weight
                if particle.body.position.x < center_x:
                    # Calculate weight based on distance from center
                    distance = (center_x - particle.body.position.x) / (SCALE_WIDTH/2)
                    left_weight += weight * distance
                else:
                    # Calculate weight based on distance from center
                    distance = (particle.body.position.x - center_x) / (SCALE_WIDTH/2)
                    right_weight += weight * distance
        
        # Reduce sensitivity for more realistic rotation
        weight_diff = left_weight - right_weight
        
        # Reduce angle multiplier from 0.05 to 0.03 for less extreme rotation
        target_angle = np.clip(weight_diff * 0.03, -math.radians(MAX_ANGLE), math.radians(MAX_ANGLE))
        
        # Add damping to the angle calculation to prevent oscillation
        current_angle = self.body.angle
        damped_target = target_angle * 0.7 + current_angle * 0.3  # Add damping
        
        # Reduce torque multiplier from 5000 to 3000 for smoother movement
        torque_value = (damped_target - current_angle) * 3000
        
        # Set the torque directly on the body
        self.body.torque = torque_value
        
        return left_weight, right_weight

# Create Pygame window
pygame.display.set_caption("Balance Scale")
clock = pygame.time.Clock()
pygame.font.init()

space = pymunk.Space()
space.gravity = (0, GRAVITY)
space.damping = DAMPING
space.collision_bias = BIAS

def main():
    # Initialize game state
    game_over = False
    current_particle = PreParticle(WIDTH // 2, 0)
    particles = []
    dragging = False
    selected_size = 0  # Initial size index

    # Create scale
    scale_body, scale_shape = create_scale(space)
    scale = Scale(scale_body)  # Pass the body to the Scale
    
    # Rest of the function remains unchanged

    # Main Game Loop
    while not game_over:
        # Get current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    new_particle = current_particle.release(space, shape_to_particle)
                    particles.append(new_particle)
                    current_particle = PreParticle(mouse_pos[0], selected_size)
                elif event.button == 3:  # Right click
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:  # Right click release
                    dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                current_particle.set_x(mouse_pos[0])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_size = (selected_size + 1) % len(SIZE_VALUES)
                    current_particle = PreParticle(mouse_pos[0], selected_size)
                elif event.key == pygame.K_DOWN:
                    selected_size = (selected_size - 1) % len(SIZE_VALUES)
                    current_particle = PreParticle(mouse_pos[0], selected_size)

        # Update preview particle position even when not dragging
        if not dragging:
            current_particle.set_x(mouse_pos[0])

        # Update physics
        space.step(1/FPS)

        # Calculate weight distribution
        left_weight, right_weight = scale.calculate_weight_distribution(particles)
        
        # Single draw section
        screen.fill(BG_COLOR)
        scale.draw(screen)
        
        # Draw all particles
        for particle in particles:
            particle.draw(screen)
        
        # Draw current particle preview
        current_particle.draw(screen)
        
        # Draw weight indicators
        font = pygame.font.Font(None, 36)
        left_text = font.render(f"Left: {left_weight:.1f} KG", True, (0, 0, 0))
        right_text = font.render(f"Right: {right_weight:.1f} KG", True, (0, 0, 0))
        screen.blit(left_text, (10, 50))
        screen.blit(right_text, (WIDTH - 200, 50))
        
        # Draw size indicator
        size_text = font.render(f"Weight: {SIZE_VALUES[selected_size]}", True, (0, 0, 0))
        screen.blit(size_text, (10, 10))
        
        # Single display update
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()