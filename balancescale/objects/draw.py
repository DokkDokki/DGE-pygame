import pygame

#Draw the balance scale
def draw_scale(screen, scale_size, scale_color, scale_position):
    pygame.draw.rect(screen, scale_color, (scale_position[0], scale_position[1], scale_size[0], scale_size[1]))