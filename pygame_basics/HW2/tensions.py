import sys, pygame
from HW2.vector import Vector
from random import *
from pygame.locals import *
import math
import numpy

background_color = (255, 255, 255)
(width, height) = (400, 400)

screen = pygame.display.set_mode((width ,height))
pygame.display.set_caption("Tensions Joseph Sklar")
pygame.font.init()
myfont = pygame.font.SysFont("monospace", 15)

class Board(object):
    def __init__(self):
        self.left_line = ((50,50),(50,350))
        self.top_line = ((50,50),(350,50))
        self.right_line = ((350, 50,), (350,350))

    def display(self):
        pygame.draw.line(screen, (0,0,0), self.left_line[0], self.left_line[1], 5)
        pygame.draw.line(screen, (0, 0, 0), self.top_line[0], self.top_line[1], 5)
        pygame.draw.line(screen, (0, 0, 0), self.right_line[0], self.right_line[1], 5)

class Rope(Vector):
    def __init__(self,length, angle, back_end_coordinates, color, tension = 0):
        Vector.__init__(self, length, angle, back_end_coordinates)
        self.tension = tension
        self.color = color
        self.break_point = 375
        self.broken = False
    def get_knot_coordinates(self):
        coordinates = (int((self.get_cartesian_coordinates()[0][0] + self.get_cartesian_coordinates()[1][0]) / 2),
                       int((self.get_cartesian_coordinates()[0][1] + self.get_cartesian_coordinates()[1][1])/2))
        return coordinates
    def displayRope(self, screen):
        self.display(screen)
        pygame.draw.circle(screen, (0,0,0), (self.get_knot_coordinates()[0], self.get_knot_coordinates()[1]), 5)
    def splitRope(self):
        upper_rope_vector = Rope.from_cartesian_coordinates(self.get_knot_coordinates(), self.get_cartesian_coordinates()[1])
        upper_rope = Rope(upper_rope_vector.length, upper_rope_vector.angle, upper_rope_vector.back_pos, (0,0,0))
        lower_rope_vector = Rope.from_cartesian_coordinates(self.get_cartesian_coordinates()[0], self.get_knot_coordinates())
        lower_rope = Rope(lower_rope_vector.length, lower_rope_vector.angle, lower_rope_vector.back_pos, (0,0,0))
        return (upper_rope, lower_rope)
class Block(Rect):
    def __init__(self, left, top, width, height):
        Rect.__init__(self,left, top, width, height)
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

    t2 = weight_of_block/(math.tan(angle1_adjusted) * math.cos(angle2_adjusted) + math.sin(angle2_adjusted))
    t1 = t2 * math.cos(angle2_adjusted)/math.cos(angle1_adjusted)
    return(t1,t2)






# render text


screen.fill(background_color)

board = Board()
board.display()
#if on top
option1 = (randint(50,200),50)
#if on side
option2 = (50, randint(50,150))
options = [option1 ,option2]
result = shuffle(options)
rope1_vector = Vector.from_cartesian_coordinates((200,150),options[1])
rope1 = Rope(rope1_vector.length, rope1_vector.angle, rope1_vector.back_pos, rope1_vector.get_cartesian_coordinates()[1])
rope1.displayRope(screen)

label = myfont.render("Angle of Rope 1: " + str(round(math.degrees(rope1_vector.angle - math.pi),4)), 1, (0,0,0) )
screen.blit(label, (100, 350))


#if on top
option1 = (randint(200,350),50)
#if on side
option2 = (350, randint(50,150))
options = [option1,option2]
shuffle(options)
rope2_vector = Vector.from_cartesian_coordinates((200,150), options[1],)
rope2 = Rope(rope2_vector.length, rope2_vector.angle, rope2_vector.back_pos, rope2_vector.get_cartesian_coordinates()[1])
rope2.displayRope(screen)

label = myfont.render("Angle of Rope 2: " + str(round(math.degrees(rope2_vector.angle * (-1)), 4)), 1, (0,0,0))
screen.blit(label, (100, 375))
print(get_tensions(rope1_vector.angle, rope2_vector.angle, randint(200,800)))



block = Block(175,150,50,50)
block.display()

pygame.display.flip()

weight = "";
weightInt = 0;

while 1:

    #if either is broken the printing will be different, we will add 200
    # in the y direction to both lower vectors as well as the box and the
    #number print
    if rope1.broken == True or rope2.broken == True :
        screen.fill(background_color)
        board.display()

    #split the left rope
        split_rope_1 = rope1.splitRope()
        upper_rope_1 = split_rope_1[0]
        lower_rope_1 = split_rope_1[1]

        upper_rope_1.display(screen)

        lower_rope_1_vector = Vector.from_cartesian_coordinates((lower_rope_1.get_cartesian_coordinates()[0][0],
                                                                 lower_rope_1.get_cartesian_coordinates()[0][1] + 100),
                                                                (lower_rope_1.get_cartesian_coordinates()[1][0],
                                                                 lower_rope_1.get_cartesian_coordinates()[1][1] + 100))
        lower_rope_1 = Rope(lower_rope_1_vector.length, lower_rope_1_vector.angle,
                            lower_rope_1_vector.back_pos, lower_rope_1_vector, (0, 0, 0))
        lower_rope_1.display(screen)

        split_rope_2 = rope2.splitRope()
        upper_rope_2 = split_rope_2[0]
        upper_rope_2.display(screen)
        lower_rope_2 = split_rope_2[1]

        lower_rope_2_vector = Vector.from_cartesian_coordinates((lower_rope_2.get_cartesian_coordinates()[0][0],
                                                                 lower_rope_2.get_cartesian_coordinates()[0][1] + 100),
                                                                (lower_rope_2.get_cartesian_coordinates()[1][0],
                                                                 lower_rope_2.get_cartesian_coordinates()[1][1] + 100))
        lower_rope_2 = Rope(lower_rope_2_vector.length, lower_rope_2_vector.angle,
                            lower_rope_2_vector.back_pos, lower_rope_2_vector, (0, 0, 0))
        lower_rope_2.display(screen)
    # Split right rope

        block.top = 250
        block.display()

        label = myfont.render(weight, 1, (0, 0, 0))
        screen.blit(label, (185, 275))

    else:
        screen.fill(background_color)
        board.display()
        rope1.displayRope(screen)
        label = myfont.render("Angle of Rope 1: " + str(round(math.degrees(rope1_vector.angle - math.pi), 4)), 1, (0, 0, 0))
        screen.blit(label, (100, 350))
        rope2.displayRope(screen)
        label = myfont.render("Angle of Rope 2: " + str(round(math.degrees(rope2_vector.angle * (-1)), 4)), 1, (0, 0, 0))
        screen.blit(label, (100, 375))
        block.display()

        label = myfont.render(weight, 1, (0, 0, 0))
        screen.blit(label, (185, 175))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


        elif event.type == KEYDOWN:
            if event.unicode.isdigit():
                weight += event.unicode
            elif event.key == K_BACKSPACE:
                weight = weight[:-1]
            elif event.key == K_RETURN:
                weightInt = int(weight);
                tensions_after_block = get_tensions(rope1.angle, rope2.angle, weightInt);
                if tensions_after_block[0] :
                    rope2.broken = True
                    print("we broke the first")
                if tensions_after_block[1] > 375:
                    rope2.broken = True
                    print("we broke the second")

    pygame.display.flip()