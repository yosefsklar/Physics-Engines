import sys, pygame
from random import *
from pygame.locals import *
import math
import numpy



background_color = (255, 255, 255)
(width, height) = (400, 400)

screen = pygame.display.set_mode((width ,height))
pygame.display.set_caption("Vector Addition Joseph Sklar")

class Line(object):
    def __init__(self, color):
        self.color = color
        self.length = randint(100,150)
        self.angle = math.radians(randint(0,359))
        self.back_pos = (randint(100, 300), randint(100, 300))
        self.front_pos =(self.back_pos[0] + self.length * math.cos(self.angle), self.back_pos[1] + self.length * math.sin(self.angle))
        self.x_component = self.front_pos[0] - self.back_pos[0]
        self.y_component = self.front_pos[1] - self.back_pos[1]
        self.dragging = False
        self.triangle_point_center = (self.back_pos[0] + (self.length - 10) * math.cos(self.angle), self.back_pos[1] + (self.length - 10) * math.sin(self.angle))
        self.triangle_point_1 = (self.triangle_point_center[0] + (5 * math.sin(self.angle)), self.triangle_point_center[1] - (5 * math.cos(self.angle)))
        self.triangle_point_2 = self.front_pos
        self.triangle_point_3 = (self.triangle_point_center[0] - (5 * math.sin(self.angle)), self.triangle_point_center[1] + (5 * math.cos(self.angle)))
    def displayTri(self):
        return pygame.draw.polygon(screen, self.color, (self.triangle_point_1, self.triangle_point_2, self.triangle_point_3), 0)
    def displayLine(self):
        self.displayTri()
        return pygame.draw.line(screen, self.color, self.back_pos, self.front_pos, 5)



line1 = Line((0, 0, 0))
line1Rect = line1.displayLine()

line2 = Line((0, 255, 0))
line2Rect = line2.displayLine()

line3 = None
print(line1.front_pos)
print(line1.triangle_point_center)
while line3 == None:
    line1Rect = line1.displayLine()
    line2Rect = line2.displayLine()
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
            if abs(line1.back_pos[0] - line2.front_pos[0]) < 7 and abs(line1.back_pos[1] - line2.front_pos[1]) < 7:

                line3 = Line((255, 0, 0))
                line3.back_pos = line2.back_pos
                line3.front_pos = line1.front_pos

                #find the angle and the length
                line3.length = math.sqrt((line3.front_pos[0] - line3.back_pos[0])**2 + (line3.front_pos[1] - line3.back_pos[1])**2)
                line3.angle =  math.atan((line3.front_pos[0] - line3.back_pos[0]) / (line3.front_pos[1] - line3.back_pos[1]))

                if (line3.front_pos[1] - line3.back_pos[1]) < 0:
                    line3.triangle_point_center = (line3.back_pos[0] + ((line3.length - 10) * math.sin(line3.angle) * (-1)), (line3.back_pos[1] + (line3.length - 10) * math.cos(line3.angle) * (-1)))
                else:
                    line3.triangle_point_center = (line3.back_pos[0] + ((line3.length - 10) * math.sin(line3.angle)), (line3.back_pos[1] + (line3.length - 10) * math.cos(line3.angle)))
                line3.triangle_point_1 = (line3.triangle_point_center[0] + (5 * math.cos(line3.angle)), line3.triangle_point_center[1] - (5 * math.sin(line3.angle)))
                line3.triangle_point_2 = line3.front_pos
                line3.triangle_point_3 = (line3.triangle_point_center[0] - (5 * math.cos(line3.angle)), line3.triangle_point_center[1] + (5 * math.sin(line3.angle)))


            elif abs(line1.front_pos[0] - line2.back_pos[0]) < 7 and abs(line1.front_pos[1] - line2.back_pos[1]) < 7:
                line3 = Line((255, 0, 0))
                line3.back_pos = line1.back_pos
                line3.front_pos = line2.front_pos

                # find the angle and the length
                line3.length = math.sqrt(
                    (line3.front_pos[0] - line3.back_pos[0]) ** 2 + (line3.front_pos[1] - line3.back_pos[1]) ** 2)
                line3.angle = math.atan(
                    (line3.front_pos[0] - line3.back_pos[0]) / (line3.front_pos[1] - line3.back_pos[1]))

                if (line3.front_pos[1] - line3.back_pos[1]) < 0:
                    line3.triangle_point_center = (
                    line3.back_pos[0] + ((line3.length - 10) * math.sin(line3.angle) * (-1)),
                    (line3.back_pos[1] + (line3.length - 10) * math.cos(line3.angle) * (-1)))
                else:
                    line3.triangle_point_center = (line3.back_pos[0] + ((line3.length - 10) * math.sin(line3.angle)),
                                                   (line3.back_pos[1] + (line3.length - 10) * math.cos(line3.angle)))
                line3.triangle_point_1 = (line3.triangle_point_center[0] + (5 * math.cos(line3.angle)),
                                          line3.triangle_point_center[1] - (5 * math.sin(line3.angle)))
                line3.triangle_point_2 = line3.front_pos
                line3.triangle_point_3 = (line3.triangle_point_center[0] - (5 * math.cos(line3.angle)),
                                          line3.triangle_point_center[1] + (5 * math.sin(line3.angle)))

        elif event.type == pygame.MOUSEMOTION:
            if line1.dragging:
                mouse_x, mouse_y = event.pos
                line1.back_pos = (mouse_x, mouse_y)
                line1.front_pos = (mouse_x + line1.x_component, mouse_y + line1.y_component)
                line1.triangle_point_center = (line1.back_pos[0] + (line1.length - 10) * math.cos(line1.angle),
                                               line1.back_pos[1] + (line1.length - 10) * math.sin(line1.angle))
                line1.triangle_point_1 = (line1.triangle_point_center[0] + (5 * math.sin(line1.angle)),
                                          line1.triangle_point_center[1] - (5 * math.cos(line1.angle)))
                line1.triangle_point_2 = line1.front_pos
                line1.triangle_point_3 = (line1.triangle_point_center[0] - (5 * math.sin(line1.angle)),
                                          line1.triangle_point_center[1] + (5 * math.cos(line1.angle)))
            elif line2.dragging:
                mouse_x, mouse_y = event.pos
                line2.back_pos = (mouse_x, mouse_y)
                line2.front_pos = (mouse_x + line2.x_component, mouse_y + line2.y_component)
                line2.triangle_point_center = (line2.back_pos[0] + (line2.length - 10) * math.cos(line2.angle),
                                              line2.back_pos[1] + (line2.length - 10) * math.sin(line2.angle))
                line2.triangle_point_1 = (line2.triangle_point_center[0] + (5 * math.sin(line2.angle)),
                                          line2.triangle_point_center[1] - (5 * math.cos(line2.angle)))
                line2.triangle_point_2 = line2.front_pos
                line2.triangle_point_3 = (line2.triangle_point_center[0] - (5 * math.sin(line2.angle)),
                                          line2.triangle_point_center[1] + (5 * math.cos(line2.angle)))


#line.front_pos = (mx, my)
#line.back_pos = (mx + 100, my +100)

    screen.fill(background_color)
    line1.displayLine()
    line2.displayLine()
    if line3 != None:
        line3.displayLine()

    pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()