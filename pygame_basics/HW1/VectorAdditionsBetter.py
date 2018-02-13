import sys, pygame
from random import *
from pygame.locals import *
import math
import numpy


background_color = (255, 255, 255)
(width, height) = (400, 400)

screen = pygame.display.set_mode((width ,height))
pygame.display.set_caption("Vector Addition Joseph Sklar")



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

    def display(self):
        pygame.draw.line(screen, (0,0,0), self.back_pos, self.get_cartesian_coordinates()[1], 5)



class VectorArrow(Vector):
    def __init__(self, color, length, angle, back_end_coordinates):
        Vector.__init__(self, length, angle, back_end_coordinates)
        self.color = color
        self.dragging = False


    @classmethod
    def from_vector(cls, color, vector):
        vector_arrow = VectorArrow(color, vector.length, vector.angle, vector.back_pos)
        return vector_arrow

    @classmethod
    def create_random_vector_arrow(cls, color):
        vector_arrow = VectorArrow.from_vector(color, Vector.create_random_vector())
        return vector_arrow

    def displayTri(self):

        triangle_point_center = (self.back_pos[0] + (self.length - 10) * math.cos(self.angle),
                                     self.back_pos[1] + (self.length - 10) * math.sin(self.angle))
        triangle_point_1 = (triangle_point_center[0] + (5 * math.sin(self.angle)),
                            triangle_point_center[1] - (5 * math.cos(self.angle)))
        triangle_point_2 = self.get_cartesian_coordinates()[1]
        triangle_point_3 = (triangle_point_center[0] - (5 * math.sin(self.angle)),
                            triangle_point_center[1] + (5 * math.cos(self.angle)))
        return pygame.draw.polygon(screen, self.color,
                                   (triangle_point_1, triangle_point_2, triangle_point_3), 0)
    def display(self):
        self.displayTri()
        return pygame.draw.line(screen, self.color, self.back_pos, self.get_cartesian_coordinates()[1], 5)





vectorArrow_1 = VectorArrow.create_random_vector_arrow((0,0,0))
vectorArrow_2 = VectorArrow.create_random_vector_arrow((0,255,0))

vectorArrow_1.display()
vectorArrow_2.display()

vectorArrow_3 = None



while vectorArrow_3 == None:
    vectorArrow_1_rect = vectorArrow_1.display()
    vectorArrow_2_rect = vectorArrow_2.display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if vectorArrow_1_rect.collidepoint(event.pos):
                vectorArrow_1.dragging = True
                mouse_x, mouse_y = event.pos
                print(vectorArrow_1.dragging)
            elif vectorArrow_2_rect.collidepoint(event.pos):
                vectorArrow_2.dragging = True
                mouse_x, mouse_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                vectorArrow_1.dragging = False
                vectorArrow_2.dragging = False
            if abs(vectorArrow_1.back_pos[0] - vectorArrow_2.get_cartesian_coordinates()[1][0]) < 7 and abs(vectorArrow_1.back_pos[1] - vectorArrow_2.get_cartesian_coordinates()[1][1]) < 7:
                #we will enter cartesian coordinates
                back_pos = vectorArrow_2.back_pos
                front_pos = vectorArrow_1.get_cartesian_coordinates()[1]
                print(front_pos)
                vector_3 = Vector.from_cartesian_coordinates(back_pos,front_pos)
                vectorArrow_3 = VectorArrow.from_vector((255,0,0), vector_3)
            elif abs(vectorArrow_1.get_cartesian_coordinates()[1][0] - vectorArrow_2.back_pos[0]) < 7 and abs(vectorArrow_1.get_cartesian_coordinates()[1][1] - vectorArrow_2.back_pos[1]) < 7:
                back_pos = vectorArrow_1.back_pos
                front_pos = vectorArrow_2.get_cartesian_coordinates()[1]
                print(front_pos)
                vector_3 = Vector.from_cartesian_coordinates(back_pos, front_pos)
                vectorArrow_3 = VectorArrow.from_vector((255, 0, 0), vector_3)
        elif event.type == pygame.MOUSEMOTION:
            if vectorArrow_1.dragging:
                mouse_x, mouse_y = event.pos
                vectorArrow_1.back_pos = (mouse_x, mouse_y)
            if vectorArrow_2.dragging:
                mouse_x, mouse_y = event.pos
                vectorArrow_2.back_pos = (mouse_x, mouse_y)
    screen.fill(background_color)
    vectorArrow_1.display()
    vectorArrow_2.display()
    if vectorArrow_3 != None:
        vectorArrow_3.display()

    pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()