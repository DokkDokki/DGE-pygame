import pygame
import sys
import numpy as np
import pymunk
import time
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
SCALE_HEIGHT = 150  # Height of the scale bar remains the same
SCALE_POS = (WIDTH // 2, HEIGHT // 2)  # Center position of the scale
SCALE_LEFT = SCALE_POS[0] - SCALE_WIDTH // 2
SCALE_RIGHT = SCALE_POS[0] + SCALE_WIDTH // 2
MAX_ANGLE = 45  # Maximum tilt angle in degrees

# Add this after the space initialization
def create_scale(space):
    # Create the static body for the scale
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = SCALE_POS
    
    # Create the segment shape for the scale
    shape = pymunk.Segment(body, (-SCALE_WIDTH//2, 0), (SCALE_WIDTH//2, 0), THICKNESS)
    shape.friction = 0.5
    shape.elasticity = ELASTICITY
    shape.collision_type = 2  # Different collision type for the scale
    
    # Add the body and shape to the space
    space.add(body, shape)
    return body, shape

def create_middle_wall(space):
    # Create the vertical wall in the middle
    middle_wall = pymunk.Poly.create_box(space.static_body, (100, HEIGHT))
    middle_wall.body.position = (WIDTH // 2, HEIGHT // 2)
    middle_wall.collision_type = 3
    space.add(middle_wall)
    return middle_wall

class Scale:
    def __init__(self):
        self.image = pygame.image.load("balancescale/assets/images/scalebase.png")  # Load your bar image
        self.image = pygame.transform.scale(self.image, (SCALE_WIDTH, SCALE_HEIGHT))  # Scale the image to the new dimensions
        self.rect = self.image.get_rect(center=SCALE_POS)
        self.angle = 0  # Initial angle of the scale
        
    def draw(self, screen):
        # Rotate the image based on the current angle
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)
        
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
        
        # Calculate the angle based on the weight difference
        weight_diff = left_weight - right_weight
        self.angle = np.clip(weight_diff * 2, -MAX_ANGLE, MAX_ANGLE)
        
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
    scale = Scale()

    # Create middle wall
    middle_wall = create_middle_wall(space)
    
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
                    selected_size = (selected_size + 1) % len(RADII)
                    current_particle = PreParticle(mouse_pos[0], selected_size)
                elif event.key == pygame.K_DOWN:
                    selected_size = (selected_size - 1) % len(RADII)
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
        size_text = font.render(f"Size: {selected_size + 1}", True, (0, 0, 0))
        screen.blit(size_text, (10, 10))
        
        # Single display update
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()