import numpy as np

class Branch(object):

    def __init__(self, x, y, direction, rotation, speed):
        self.x = float(x)
        self.y = float(y)
        self.direction = direction
        self.rotation = rotation
        self.speed = speed
        self.color = (255,255,255)
        self.distance_travelled = 0
        self.dead = False

    def step(self):
        self.direction += self.rotation
        if self.direction > (np.pi * 2):
            self.direction -= (np.pi * 2)
        elif self.direction < 0:
            self.direction += (np.pi * 2)
        self.x += np.sin(self.direction) * self.speed
        self.y += np.cos(self.direction) * self.speed
        self.distance_travelled += self.speed