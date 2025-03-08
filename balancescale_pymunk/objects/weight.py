import pymunk
import pygame
import random
from utils import constants

class Weight:
    def __init__(self, space, position, mass):
        self.mass = mass
        self.body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, 10))
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.elasticity = 0.95
        space.add(self.body, self.shape)

    def draw(self, screen):
        x, y = self.body.position
        pygame.draw.circle(screen, (0, 0, 255), (int(x), int(y)), 10)

    def remove(self):
        self.space.remove(self.body, self.shape)

def create_initial_weights(space, pivot_x, pivot_y, scale_size, count):
    weights = []
    for _ in range(count):
        position = (pivot_x - scale_size // 2 + random.uniform(-20, 20), pivot_y - 20)
        weight = Weight(space, position, random.uniform(1, 3))
        weights.append(weight)
    return weights