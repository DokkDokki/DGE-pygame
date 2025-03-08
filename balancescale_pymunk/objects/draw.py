import pygame
import pymunk
import pymunk.pygame_util

def setup(space, screen_width, screen_height):
    # Create the static base
    base_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    base_body.position = (screen_width // 2, screen_height // 3)
    base_shape = pymunk.Segment(base_body, (-50, 0), (50, 0), 5)
    base_shape.density = 1
    space.add(base_body, base_shape)

    # Create the pivot
    pivot_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    pivot_body.position = (screen_width // 2, screen_height // 3)
    pivot_shape = pymunk.Circle(pivot_body, 5)
    pivot_shape.density = 1
    space.add(pivot_body, pivot_shape)

    # Create the beam
    beam_body = pymunk.Body(1, 1000)  # Mass, Inertia
    beam_body.position = (screen_width // 2, screen_height // 3)
    beam_shape = pymunk.Segment(beam_body, (-100, 0), (100, 0), 5)
    beam_shape.density = 1
    space.add(beam_body, beam_shape)

    # Create the pivot joint
    pivot_joint = pymunk.PivotJoint(beam_body, pivot_body, (screen_width // 2, screen_height // 3))
    space.add(pivot_joint)

    # Create the rotational limit joint
    limit_joint = pymunk.RotaryLimitJoint(beam_body, pivot_body, -0.2, 0.2)
    space.add(limit_joint)

def draw(space, screen, draw_options):
    space.debug_draw(draw_options)
    space.step(1/60.0)