
import sys, pygame
from random import *
import math
import numpy
'''
background_color = (255, 255, 255)
(width, height) = (500, 500)


class Vector(object):
    def __init__(self, back_point, front_point):


        self.back_point = back_point
        #start point is equivelent to the non-existent point_5
        self.front_point = front_point
        self.point_1 = (back_point[0] + self.right_adjust_x(), back_point[1] + self.right_adjust_y())
        self.point_2 = (back_point[0] + self.left_adjust_x(), back_point[1] + self.left_adjust_y())
        self.point_3 = (self.point_2[0]+ (280 * math.cos(self.angle_between())), self.point_2[1] + (280 * math.cos(self.angle_between())))
        self.point_4 = ((self.point_3[0] + self.left_adjust_x(), self.point_3[1] + self.left_adjust_y()))
        self.point_7 = (self.point_1[0]+ (280 * math.cos(self.angle_between())), self.point_1[1] + (280 * math.cos(self.angle_between())))
        self.point_6 = (self.point_7[0] + self.right_adjust_x(), self.point_7[1] + self.right_adjust_y())

    def angle_between(self):
        x = numpy.array([self.front_point[0] - self.back_point[0], self.front_point[1] -self.back_point[1]])
        y = numpy.array([self.front_point[0] - self.back_point[0], self.back_point[1]])
        return math.acos(numpy.dot(self.back_point,self.front_point)/(numpy.dot((numpy.linalg.norm(x)),(numpy.linalg.norm(y)))))
    def right_adjust_x(self):
        return 5 * math.cos(self.angle_between() + (3 * math.pi / 4))
    def right_adjust_y(self):
        return 5 * math.sin(self.angle_between() + (3 * math.pi / 4))
    def left_adjust_x(self):
        return 5 * math.cos(self.angle_between() + (math.pi / 4))
    def left_adjust_y(self):
        return 5 * math.sin(self.angle_between() + (math.pi / 4))

    def display(self):
        pygame.draw.polygon(screen, (0, 0, 0), ((self.point_1), (self.point_2), (self.point_3), (self.point_4), (self.front_point), (self.point_6), (self.point_7)))




vector = Vector((0,150),(300,150))
print(math.degrees(vector.angle_between()))
print(vector.back_point)
print(vector.front_point)
print(vector.point_1)
print(vector.point_2)
print(vector.point_3)
print(vector.point_4)
'''

# the goal here is to take the cordinates of a vector and give its angle.
'''
a = [0, 150]
b = [300, 150]
x = numpy.array(a)
y = numpy.array(b)
print(int(math.degrees(math.acos( numpy.dot(a, b) / (numpy.dot((numpy.linalg.norm(x)), (numpy.linalg.norm(y))))))))
'''

'''
import sys, pygame
from random import *
from pygame.locals import *
import math
import numpy



background_color = (255, 255, 255)
(width, height) = (400, 400)

class Line(object):
    def __init__(self, color):
        self.color = color
        self.length = randint(100,200)
        self.angle = math.radians(randint(0,359))
        self.front_pos =(self.length * math.cos(self.angle), self.length * math.sin(self.angle))
        self.back_pos  = (randint(100,300), randint(100,300))
        self.x_component = self.front_pos[0] - self.back_pos[0]
        self.y_component = self.front_pos[1] - self.back_pos[1]
        self.dragging = False
    def display(self):
        return pygame.draw.line(screen, self.color, self.back_pos, self.front_pos, 5)


screen = pygame.display.set_mode((width ,height))
pygame.display.set_caption("Vector Addition Joseph Sklar")

line1 = Line((0, 0, 0))
line1Rect = line1.display()

line2 = Line((0, 0, 0))
line2Rect = line2.display()

line3 = None
while 1:
    line1Rect = line1.display()
    line2Rect = line2.display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if line1Rect.collidepoint(event.pos):
                line1.dragging = True
                mouse_x, mouse_y = event.pos
                print(line1.dragging)
            elif line2Rect.collidepoint(event.pos):
                line2.dragging = True
                mouse_x, mouse_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                line1.dragging = False
                line2.dragging = False
                print(line1.dragging)
            if abs(line1.back_pos[0] - line2.front_pos[0]) < 5 and abs(line1.back_pos[1] - line2.front_pos[1]) < 5:
                line3 = Line((255,0,0))
                line3.back_pos = line2.back_pos
                line3.front_pos = line1.front_pos
            elif abs(line1.front_pos[0] - line2.back_pos[0]) < 5 and abs(line1.front_pos[1] - line2.back_pos[1]) < 5:
                line3 = Line((255, 0, 0))
                line3.back_pos = line1.back_pos
                line3.front_pos = line2.front_pos
        elif event.type == pygame.MOUSEMOTION:
            if line1.dragging:
                mouse_x, mouse_y = event.pos
                line1.back_pos = (mouse_x, mouse_y)
                line1.front_pos = (mouse_x + line1.x_component, mouse_y + line1.y_component)
            elif line2.dragging:
                mouse_x, mouse_y = event.pos
                line2.back_pos = (mouse_x, mouse_y)
                line2.front_pos = (mouse_x + line2.x_component, mouse_y + line2.y_component)


#line.front_pos = (mx, my)
#line.back_pos = (mx + 100, my +100)

    screen.fill(background_color)
    line1.display()
    line2.display()
    if line3 != None:
        line3.display()
    pygame.display.flip()
'''
'''
line3.triangle_point_center = (line3.back_pos[0] + (line3.length - 10) * math.cos(line3.angle),
                               line3.back_pos[1] + (line3.length - 10) * math.sin(line3.angle))
line3.triangle_point_1 = (line3.triangle_point_center[0] + (5 * math.sin(line3.angle)),
                          line3.triangle_point_center[1] - (5 * math.cos(line3.angle)))
line3.triangle_point_2 = line3.front_pos
line3.triangle_point_3 = (line3.triangle_point_center[0] - (5 * math.sin(line3.angle)),
                          line3.triangle_point_center[1] + (5 * math.cos(line3.angle)))

line3.triangle_point_center = (line3.back_pos[0] + (line3.length - 10) * math.cos(line3.angle),
                               line3.back_pos[1] + (line3.length - 10) * math.sin(line3.angle))
line3.triangle_point_1 = (line3.triangle_point_center[0] + (5 * math.sin(line3.angle)),
                          line3.triangle_point_center[1] - (5 * math.cos(line3.angle)))
line3.triangle_point_2 = line3.front_pos
line3.triangle_point_3 = (line3.triangle_point_center[0] - (5 * math.sin(line3.angle)),
                          line3.triangle_point_center[1] + (5 * math.cos(line3.angle)))
print(line3.back_pos)
print(line3.front_pos)
print(math.degrees(line3.angle))
print(line3.length)
print("point center")
print(line3.triangle_point_center)
print(line3.triangle_point_1)
print(line3.triangle_point_2)
print(line3.triangle_point_3)
'''
'''
line3.triangle_point_center = (line3.back_pos[0] + ((line3.length - 10) * math.sin(line3.angle)),
                               (line3.back_pos[1] + (line3.length - 10) * math.cos(line3.angle)))
'''
'''
math.sin(print((math.radians(44))))
print("original vectors:")
print(str(line2.back_pos) + "," + str(line2.front_pos))
print(str(line1.back_pos) + "," + str(line1.front_pos))
print("back position:" + str(line2.back_pos))
print("back position:" + str(line1.front_pos))
print(line3.back_pos)
print(line3.front_pos)
print("angle:")
print(math.degrees(line3.angle))
print(line3.length)
print("point center")
print(line3.triangle_point_center)
print(line3.triangle_point_1)
print(line3.triangle_point_2)
print(line3.triangle_point_3)

print("should be same back" + str(line3.back_pos[0]))
print("Heres the length" + str(line3.length))

'''
'''
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

    @classmethod
    def from_cartesian_coordinates(cls,back_end_coordinates, front_end_coordinates):
        length = math.sqrt((front_end_coordinates[0] - back_end_coordinates[0]) ** 2 + (front_end_coordinates[1] - back_end_coordinates[1]) ** 2)
        angle =  math.atan((front_end_coordinates[1] - back_end_coordinates[1])/(front_end_coordinates[0] - back_end_coordinates[0]))
        vector = Vector(length, angle, back_end_coordinates)
        return vector

    @classmethod
    def create_random_vector(cls):
        vector = Vector(randint(100,150), math.radians(randint(0,359)), (randint(100, 300), randint(100, 300)))
        return vector
    def get_cartesian_coordinates(self):
        return((self.back_pos),((self.back_pos[0] + self.length * math.cos(self.angle), self.back_pos[1] + self.length * math.sin(self.angle))))
    def display(self):
        pygame.draw.line(screen, (0,0,0), self.back_pos, self.get_cartesian_coordinates()[1], 5)

class VectorArrow(Vector):
    def __init__(self, color, length, angle, back_end_coordinates):
        Vector.__init__(self, length, angle, back_end_coordinates)
        self.color = color
        self.dragging = False
        self.triangle_point_center = (self.back_pos[0] + (self.length - 10) * math.cos(self.angle), self.back_pos[1] + (self.length - 10) * math.sin(self.angle))
        self.triangle_point_1 = (self.triangle_point_center[0] + (5 * math.sin(self.angle)), self.triangle_point_center[1] - (5 * math.cos(self.angle)))
        self.triangle_point_2 = self.get_cartesian_coordinates()[1]
        self.triangle_point_3 = (self.triangle_point_center[0] - (5 * math.sin(self.angle)), self.triangle_point_center[1] + (5 * math.cos(self.angle)))

    @classmethod
    def from_vector(cls, color, vector):
        vector_arrow = VectorArrow(color, vector.length, vector.angle, vector.back_pos)
        return vector_arrow

    @classmethod
    def create_random_vector_arrow(cls, color):
        vector_arrow = VectorArrow.from_vector(color, Vector.create_random_vector())
        return vector_arrow

    def displayTri(self):
        return pygame.draw.polygon(screen, self.color,
                                   (self.triangle_point_1, self.triangle_point_2, self.triangle_point_3), 0)
    def display(self):
        self.displayTri()
        return pygame.draw.line(screen, self.color, self.back_pos, self.get_cartesian_coordinates()[1], 5)


vector = Vector(100, 45, (50, 50))
vector.display()

vectorArrow = VectorArrow((0,0,0), 100, 50, (50,50))
vectorArrow.display()


vectorArrow_1 = VectorArrow.create_random_vector_arrow((0,0,0))
vectorArrow_2 = VectorArrow.create_random_vector_arrow((0,255,0))

vectorArrow_1.display()
vectorArrow_2.display()



while 1:
    screen.fill(background_color)
    pygame.display.flip()

    vectorArrow_1.display()
    vectorArrow_2.display()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
'''
'''
if math.degrees(self.angle) > 90 and math.degrees(self.angle) < 270:
    front_pos = (self.back_pos[0] + self.length * math.cos(self.angle) * (-1),
                 self.back_pos[1] + self.length * math.sin(self.angle) * (-1))
else:
    front_pos =

if (self.get_cartesian_coordinates()[1][0] - self.back_pos[0]) < 0:
    triangle_point_center = (self.back_pos[0] + ((self.length - 10) * math.cos(self.angle)),
                             self.back_pos[1] + ((self.length - 10) * math.sin(self.angle)))
else:
'''
import sys, pygame
from HW2.vector import Vector
from random import *
from pygame.locals import *
import math
import numpy

background_color = (255, 255, 255)
(width, height) = (400, 400)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tensions Joseph Sklar")
pygame.font.init()
myfont = pygame.font.SysFont("monospace", 15)


class Board(object):
    def __init__(self):
        self.left_line = ((50, 50), (50, 350))
        self.top_line = ((50, 50), (350, 50))
        self.right_line = ((350, 50,), (350, 350))

    def display(self):
        pygame.draw.line(screen, (0, 0, 0), self.left_line[0], self.left_line[1], 5)
        pygame.draw.line(screen, (0, 0, 0), self.top_line[0], self.top_line[1], 5)
        pygame.draw.line(screen, (0, 0, 0), self.right_line[0], self.right_line[1], 5)


class Rope(Vector):
    def __init__(self, length, angle, back_end_coordinates, color, tension=0):
        Vector.__init__(self, length, angle, back_end_coordinates)
        self.tension = tension
        self.color = color
        self.break_point = 375
        self.broken = False

    def get_knot_coordinates(self):
        coordinates = (int((self.get_cartesian_coordinates()[0][0] + self.get_cartesian_coordinates()[1][0]) / 2),
                       int((self.get_cartesian_coordinates()[0][1] + self.get_cartesian_coordinates()[1][1]) / 2))
        return coordinates

    def displayRope(self, screen):
        self.display(screen)
        pygame.draw.circle(screen, (0, 0, 0), (self.get_knot_coordinates()[0], self.get_knot_coordinates()[1]), 5)


class Block(Rect):
    def __init__(self, left, top, width, height):
        Rect.__init__(self, left, top, width, height)
        self.weight = 0;
        self.color = (150, 150, 255)
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def set_weight(self, weight):
        self.weight = weight

    def display(self):
        pygame.draw.rect(screen, self.color, (self.left, self.top, self.width, self.height))


def get_tensions(angle1, angle2, weight_of_block):
    angle1_adjusted = angle1 - math.pi
    angle2_adjusted = angle2 * (-1)

    t2 = weight_of_block / (math.tan(angle1_adjusted) * math.cos(angle2_adjusted) + math.sin(angle2_adjusted))
    t1 = t2 * math.cos(angle2_adjusted) / math.cos(angle1_adjusted)
    return (t1, t2)
screen.fill(background_color)
rope = Rope(100, math.radians(45), (200,200), (0,0,0))
rope.displayRope(screen)
print(rope.get_knot_coordinates())
pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()



lower_rope_1_vector = Vector.from_cartesian_coordinates((lower_rope_1.get_cartesian_coordinates()[0][0],
                                                                 lower_rope_1.get_cartesian_coordinates()[0][1] + 200),
                                                                (lower_rope_1.get_cartesian_coordinates()[1][0],
                                                                 lower_rope_1.get_cartesian_coordinates()[1][1] + 200))
        lower_rope_1 = Rope(lower_rope_1_vector.length, lower_rope_1_vector.angle,
                            lower_rope_1_vector.back_pos, lower_rope_1_vector, (0,0,0))
        lower_rope_1.display(screen)


lower_rope_2_vector = Vector.from_cartesian_coordinates((lower_rope_2.get_cartesian_coordinates()[0][0],
                                                                 lower_rope_2.get_cartesian_coordinates()[0][1] + 200),
                                                                (lower_rope_2.get_cartesian_coordinates()[1][0],
                                                                 lower_rope_2.get_cartesian_coordinates()[1][1] + 200))
lower_rope_2 = Rope(lower_rope_2_vector.length, lower_rope_2_vector.angle,
                    lower_rope_2_vector.back_pos, lower_rope_2_vector, (0, 0, 0))
lower_rope_2.display(screen)