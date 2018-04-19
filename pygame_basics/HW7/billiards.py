import sys, pygame
from random import *
from pygame.locals import *
import math
import time
import numpy as n

background_color = (80, 220, 100)
height = 400
width = 400


screen = pygame.display.set_mode((width ,height))
pygame.display.set_caption("Billiards Joseph Sklar")

pygame.font.init()
myfont = pygame.font.SysFont("monospace", 15)


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
            try: angle =  math.atan((front_end_coordinates[1] - back_end_coordinates[1])/(front_end_coordinates[0] - back_end_coordinates[0]))
            except ZeroDivisionError: angle = 0
        vector = Vector(length, angle, back_end_coordinates)
        return vector

    @classmethod
    def create_random_vector(cls):
        vector = Vector(randint(100,150), math.radians(randint(0,359)), (randint(100, 300), randint(100, 300)))
        return vector

    def display(self, screen):
        return pygame.draw.line(screen, (0,0,0), self.back_pos, self.get_cartesian_coordinates()[1], 5)



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


class Ball(object):
    def __init__(self, color, x, y):
        self.color = color
        self.radius = 15
        self.x = x
        self.y = y
        self.velocity = [0,0]
    def display(self):
        return pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self, velocity):
        self.x = self.x + velocity[0]
        self.y = self.y  - velocity[1]

    def is_balls_collide(self, ball_2):
        total_radius = self.radius + ball_2.radius
        total_distance = math.sqrt((self.x - ball_2.x) ** 2 + (self.y - ball_2.y) ** 2)
        if (total_distance <= total_radius):
            return True
        else:
            return False

    def collide(self, ball_2):
        angle = math.atan2(self.y - ball_2.y, self.x - ball_2.x)
        v1x = self.velocity[0]
        v2x = ball_2.velocity[0]

        v1y = self.velocity[1]
        v2y = ball_2.velocity[1]
#1 Normal vector






ball1 = Ball((255,255,255), 50, 350)
ball2 = Ball((255,0,0), 200, 100)
ball3 = Ball((0,0,255), 350, 200)
ball_count = 3
balls = [ball1, ball2, ball3]
ball1_arrow = None
ball1_vector = None


ball_pressed = False
ball_released = False
ball1_in_motion = False
ball2_in_motion = False
ball3_in_motion = False


while 1:
    screen.fill(background_color)
    ball1.display();
    ball2.display();
    ball3.display();

    if ball_pressed == True:
        ball1_arrow.display()
    if ball1_in_motion:
        ball1.move(ball1.velocity)
        if ball1.y >= 400 - ball1.radius:
            ball1.velocity[1] = -1 * (ball1.velocity[1])
        if ball1.y <= 0 + ball1.radius:
            ball1.velocity[1] = -1 * (ball1.velocity[1])
        if ball1.x <= 0 + ball1.radius:
            ball1.velocity[0] = -1 * (ball1.velocity[0])
        if ball1.x >= 400 - ball1.radius:
            ball1.velocity[0] = -1 * (ball1.velocity[0])

    for i in range(0, ball_count):
        for j in range(i + 1, ball_count):
            if balls[i].is_balls_collide(balls[j]):
                balls[i].collide(balls[j])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif (event.type == pygame.MOUSEBUTTONDOWN) and not ball_released:
            mouse_x, mouse_y = event.pos
            if ball1.display().collidepoint(event.pos):
                ball_pressed = True
                if ball1_arrow:
                    ball1_arrow.display()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                ball_pressed = False
                ball_released = True
                ball1_in_motion = True

        elif (event.type == pygame.MOUSEMOTION) and not ball_released:
            ball_pressed = True
            mouse_x, mouse_y = event.pos
            ball1_vector = Vector.from_cartesian_coordinates((ball1.x, ball1.y),event.pos)
            ball1_arrow = VectorArrow.from_vector((0,0,0), ball1_vector)
            ball1.velocity = [(mouse_x - ball1.x)/30, (ball1.y - mouse_y)/30]




    pygame.display.flip()
    pygame.time.delay(10)

#if(m.sqrt((mx-x)**2+(my-y)**2)<=radius+cursorRadius):
#Just check whether the distance between the two centers is less than the sum of the radiuses.
'''
     distance = math.sqrt((self.x - ball_2.x) ** 2 + (self.y - ball_2.y) ** 2)
        collision = n.array([self.x - ball_2.x,self.y - ball_2.y])
        collision = collision / distance
        aci = n.dot(self.velocity, collision)
        bci = n.dot(ball_2.velocity, collision)

        # Solve for the new velocities using the 1-dimensional elastic collision equations.
        #Turns out it's really simple when the masses are the same.
        acf = bci
        bcf = aci
        print(self.velocity)
        temp = n.add(self.velocity, (acf - aci) * collision, casting="unsafe")
        self.velocity[0] += temp [0]
        temp = n.add(ball_2.velocity, (bcf - bci) * collision, casting="unsafe")
        self.velocity[1] += temp[1]
        print("!!!!!")
'''