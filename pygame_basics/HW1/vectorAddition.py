
# it will be easier to get it by cartesion than polar
'''
Have them pop up, use your mouse to move them,
then have the third be created
Use python random class to generate random
use the polygon functions
pygame.draw.polygon

steps:
1) figure out how to draw and arrow or a functioning line
2) figure out which elements on the pointlist go to which
3) the nose and the middle of the tail should be the "coordinates"
of the vector class
4) get one to appear
	-- calculating all second

-- in place of first 4, figure out ho to draw a line
-- figure out how to move it.
5) implement the random to make an arrow
6) get two on the screen
7) define an add method that takes two vectors as paramters 
and returns a 3rd new one. 
8) draw that new one and get ri of the old two. 

class Vector(object):
	def __init__(self, start_pos, end_pos):
		self.


	def display(self):
		pygame.draw.line(screen, self.color, start_pos, end_pos, width=1)

# arrow pygame.draw.polygon(window, (0, 0, 0), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))
# polygon(                  Surface,    color,    pointlist,      width=0) -> Rect                                       
'''

import sys, pygame
import math
import numpy

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

#takes coordinates, finds angle between
    def angle_between(self):
        x = numpy.array([self.front_point[0] - self.back_point[0], self.front_point[1] -self.back_point[1]])
        y = numpy.array([self.front_point[0] - self.back_point[0], self.back_point[1]])
        return math.degrees(math.acos(numpy.dot(self.back_point,self.front_point)/(numpy.dot((numpy.linalg.norm(x)),(numpy.linalg.norm(y))))))
    def right_adjust_x(self):
        return 5 * math.cos(self.angle_between())
    def right_adjust_y(self):
        return 5 * math.sin(self.angle_between())
    def left_adjust_x(self):
        return -5 * math.cos(self.angle_between())
    def left_adjust_y(self):
        return -5 * math.sin(self.angle_between())
    def display(self):
        pygame.draw.polygon(screen, (0, 0, 0), ((self.point_1), (self.point_2), (self.point_3), (self.point_4), (self.front_point), (self.point_6), (self.point_7)))




screen = pygame.display.set_mode((width ,height))
pygame.display.set_caption("Vector Addition Joseph Sklar")

vector = Vector((0,150),(300,150))
print(vector.angle_between())
print(vector.right_adjust_y())
print(vector.right_adjust_x())
print(vector.point_1)
print(vector.back_point)
print(vector.point_2)
print(vector.point_3)
print(vector.point_4)
print(vector.point_6)
print(vector.front_point)
print(vector.point_7)

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(background_color)
    vector.display()

    pygame.display.flip()

