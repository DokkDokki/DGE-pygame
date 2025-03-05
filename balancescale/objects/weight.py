import pymunk
import pygame
import random
from utils import constants

class Weight:
    def __init__(self, space, position, mass):
        self.space = space
        self.position = position
        self.mass = mass
        self.radius = constants.WEIGHT_SIZES.get(mass, 10)  # Default radius if mass not found

        self.body = pymunk.Body(mass, 100)  # Mass, Inertia
        self.body.position = position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = 1
        self.space.add(self.body, self.shape)

    def draw(self, screen, draw_options):
        # Pymunk's debug draw handles most of the drawing
        pass

    def remove(self):
        self.space.remove(self.body, self.shape)

def create_initial_weights(space, scale, num_weights):
    """Creates a list of initial weights on one side of the scale."""
    weights = []
    for _ in range(num_weights):
        mass = random.choice(constants.BIG_WEIGHTS)
        position = scale.get_arm_position("left") + (random.uniform(-20, 20), -50)  # Slightly random position above the arm
        weight = Weight(space, position, mass)
        weights.append(weight)
    return weights