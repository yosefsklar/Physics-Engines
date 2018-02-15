import sys, pygame
from random import *
from pygame.locals import *
import math
import numpy

class Vector(object):
    def __init__(self, length, angle, back_end_coordinates):
        self.length = length
        self.angle = angle
        self.back_pos = back_end_coordinates

    def get_cartesian_coordinates(self):
        return ((self.back_pos),(self.back_pos[0] + self.length * math.cos(self.angle), self.back_pos[1] + self.length * math.sin(self.angle)))

    @classmethod
    def from_cartesian_coordinates(cls, back_end_coordinates, front_end_coordinates):
        length = math.sqrt((front_end_coordinates[0] - back_end_coordinates[0]) ** 2 + (front_end_coordinates[1] - back_end_coordinates[1]) ** 2)
        if (front_end_coordinates[0] - back_end_coordinates[0]) < 0:
            angle = (math.atan((front_end_coordinates[1] - back_end_coordinates[1]) / (
                        front_end_coordinates[0] - back_end_coordinates[0]))) + math.pi
        else:
            angle =  math.atan((front_end_coordinates[1] - back_end_coordinates[1])/(front_end_coordinates[0] - back_end_coordinates[0]))
        vector = Vector(length, angle, back_end_coordinates)
        return vector

    @classmethod
    def create_random_vector(cls):
        vector = Vector(randint(100,150), math.radians(randint(0,359)), (randint(100, 300), randint(100, 300)))
        return vector

    def display(self, screen):
        return pygame.draw.line(screen, (0,0,0), self.back_pos, self.get_cartesian_coordinates()[1], 5)

