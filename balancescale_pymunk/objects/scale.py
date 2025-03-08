import pymunk
import pygame

class BalanceScale:
    def __init__(self, space, position, size):
        self.space = space
        self.position = position
        self.size = size

        # Create the static body for the pivot point
        self.pivot_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.pivot_body.position = position

        # Create the dynamic body for the beam
        self.beam_body = pymunk.Body()
        self.beam_body.position = position

        # Create the beam shape with the specified size
        self.beam_shape = pymunk.Segment(self.beam_body, (-size, 0), (size, 0), 5)
        self.beam_shape.density = 1
        self.space.add(self.beam_body, self.beam_shape)

        # Create the pivot joint
        self.pivot_joint = pymunk.PivotJoint(self.beam_body, self.pivot_body, position)
        self.space.add(self.pivot_joint)

        # Optionally, you can add a damping factor to the beam body to slow down its rotation
        self.beam_body.angular_damping = 1.0

    def draw(self, screen, draw_options):
        # Draw the beam
        pygame.draw.line(screen, (0, 0, 0), (self.position[0] - self.size, self.position[1]), (self.position[0] + self.size, self.position[1]), 5)

    def get_arm_position(self, side):
        if side == "left":
            return self.beam_body.position + pymunk.Vec2d(-self.size, 0).rotated(self.beam_body.angle)
        elif side == "right":
            return self.beam_body.position + pymunk.Vec2d(self.size, 0).rotated(self.beam_body.angle)