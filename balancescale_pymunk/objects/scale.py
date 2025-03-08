import pymunk
import pygame

class BalanceScale:
    def __init__(self, space, position, scale_size):
        self.space = space
        self.position = position
        self.scale_size = scale_size
        self.beam_length = scale_size * 4  # Adjust as needed
        self.beam_height = 10
        self.pivot_radius = 5
        self.stand_height = scale_size * 2  # Height of the stand

        self.create_scale()

    def create_scale(self):
        # Static base
        self.base_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.base_body.position = self.position
        self.base_shape = pymunk.Segment(self.base_body, (-self.scale_size, 0), (self.scale_size, 0), 5)
        self.base_shape.density = 1
        self.space.add(self.base_body, self.base_shape)

        # Pivot
        self.pivot_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.pivot_body.position = self.position
        self.pivot_shape = pymunk.Circle(self.pivot_body, self.pivot_radius)
        self.pivot_shape.density = 1
        self.space.add(self.pivot_body, self.pivot_shape)

        # Beam
        self.beam_body = pymunk.Body(1, 1000)  # Mass, Inertia
        self.beam_body.position = self.position
        self.beam_shape = pymunk.Segment(self.beam_body, (-self.beam_length / 2, 0), (self.beam_length / 2, 0), self.beam_height)
        self.beam_shape.density = 1
        self.space.add(self.beam_body, self.beam_shape)

        # Barriers at the ends of the beam
        self.left_barrier = pymunk.Segment(self.beam_body, (-self.beam_length / 2, -self.beam_height), (-self.beam_length / 2, self.beam_height), 5)
        self.left_barrier.density = 1
        self.space.add(self.left_barrier)

        self.right_barrier = pymunk.Segment(self.beam_body, (self.beam_length / 2, -self.beam_height), (self.beam_length / 2, self.beam_height), 5)
        self.right_barrier.density = 1
        self.space.add(self.right_barrier)

        # Pivot Joint
        self.pivot_joint = pymunk.PivotJoint(self.beam_body, self.pivot_body, self.position)
        self.space.add(self.pivot_joint)

        # Rotary Limit Joint
        self.limit_joint = pymunk.RotaryLimitJoint(self.beam_body, self.pivot_body, -0.2, 0.2)  # Limits in radians
        self.space.add(self.limit_joint)

    def draw(self, screen, draw_options):
        # Draw the stand
        stand_start = (self.position[0], self.position[1])
        stand_end = (self.position[0], self.position[1] + self.stand_height)
        pygame.draw.line(screen, (0, 0, 0), stand_start, stand_end, 5)  # Black color, 5 width
        
        # Pymunk's debug draw handles the rest of the drawing
        pass # Nothing to do here, Pymunk draws directly

    def get_arm_position(self, side):
        """Returns the position of the left or right arm of the scale."""
        if side == "left":
            return self.beam_body.position + pymunk.Vec2d(-self.beam_length / 2, 0).rotated(self.beam_body.angle)
        elif side == "right":
            return self.beam_body.position + pymunk.Vec2d(self.beam_length / 2, 0).rotated(self.beam_body.angle)
        else:
            raise ValueError("Side must be 'left' or 'right'")