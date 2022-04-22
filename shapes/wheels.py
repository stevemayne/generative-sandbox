import numpy as np
import pygame

class GeoObject(object):

    def position(self):
        return (0,0)

class Wheel(GeoObject):
    def __init__(self, x: int, y: int, rotation_speed: float, arm_length: float, initial_rotation_angle: float = 0,
        attach_to: "GeoObject" = None, color = (0, 0, 255), oval_factor = 0.0):
        self.x = x
        self.y = y
        self.rotation_speed = rotation_speed
        self.arm_length = arm_length
        self.angle = initial_rotation_angle
        self.attach_to = attach_to
        self.color = color
        self.oval_factor = oval_factor
    
    def step(self) -> None:
        self.angle = self.angle + self.rotation_speed
        if (self.angle > 2 * np.pi):
            self.angle = self.angle - 2 * np.pi
        elif (self.angle < 0):
            self.angle = self.angle + 2 * np.pi

    def position(self):
        if self.attach_to:
            self.x, self.y = self.attach_to.position()
        x = np.sin(self.angle) * self.arm_length
        y = np.cos(self.angle) * self.arm_length
        return (self.x + x, self.y + y)
    
    def draw(self, screen):
        x, y = self.position()
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.arm_length, width=1)
        pygame.draw.circle(screen, self.color, (x, y), 2)