import pygame
import math

def draw_base(screen: pygame.Surface, center_x: int, center_y: int) -> None:
    """Draw the base stand of the balance scale"""
    DARK_GRAY = (64, 64, 64)
    base_width = 60
    base_height = 100
    base_x = center_x - base_width // 2
    base_y = center_y - base_height // 2
    pygame.draw.rect(screen, DARK_GRAY, (base_x, base_y, base_width, base_height))

def draw_pivot(screen: pygame.Surface, center_x: int, center_y: int) -> None:
    """Draw the pivot point of the balance scale"""
    DARK_GRAY = (64, 64, 64)
    pivot_radius = 10
    pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y - 40), pivot_radius)

def draw_beam(screen: pygame.Surface, center_x: int, center_y: int, beam_length: int) -> tuple:
    """Draw the horizontal beam and return the end points"""
    DARK_GRAY = (64, 64, 64)
    beam_thickness = 10
    left_end = (center_x - beam_length // 2, center_y - 40)
    right_end = (center_x + beam_length // 2, center_y - 40)
    pygame.draw.line(screen, DARK_GRAY, left_end, right_end, beam_thickness)
    return left_end, right_end

def draw_plates(screen: pygame.Surface, left_end: tuple, right_end: tuple) -> tuple:
    """Draw the plates and their strings, return plate centers"""
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)
    plate_radius = 30
    
    left_plate_center = (left_end[0], left_end[1] + 40)
    right_plate_center = (right_end[0], right_end[1] + 40)
    
    # Draw strings
    pygame.draw.line(screen, DARK_GRAY, left_end, left_plate_center, 2)
    pygame.draw.line(screen, DARK_GRAY, right_end, right_plate_center, 2)
    
    # Draw plates
    pygame.draw.circle(screen, LIGHT_GRAY, left_plate_center, plate_radius)
    pygame.draw.circle(screen, LIGHT_GRAY, right_plate_center, plate_radius)
    
    return left_plate_center, right_plate_center

def draw_balance_scale(screen: pygame.Surface, center_x: int, center_y: int, beam_length: int = 200) -> None:
    """Draw the complete balance scale"""
    draw_base(screen, center_x, center_y)
    draw_pivot(screen, center_x, center_y)
    left_end, right_end = draw_beam(screen, center_x, center_y, beam_length)
    draw_plates(screen, left_end, right_end)

def draw_weight(screen: pygame.Surface, position: tuple, weight: int) -> None:
    """Draw a weight on the scale plate"""
    WEIGHT_COLOR = (128, 0, 0)  # Dark red
    weight_size = 20 + weight * 5  # Size increases with weight
    pygame.draw.circle(screen, WEIGHT_COLOR, position, weight_size)
    
    # Draw weight number
    font = pygame.font.Font(None, 36)
    text = font.render(str(weight), True, (255, 255, 255))
    text_rect = text.get_rect(center=position)
    screen.blit(text, text_rect)

# Create a surface for the scale image
scale_x = 400  # Default x position
scale_y = 300  # Default y position
scale_image = pygame.Surface((400, 300), pygame.SRCALPHA)  # Create transparent surface

def draw_scale_on_surface():
    """Draw the scale on the scale_image surface"""
    global scale_image
    draw_balance_scale(scale_image, 200, 150)  # Draw in center of surface

# Initialize the scale image
draw_scale_on_surface()