import sys, pygame, pygame.mixer
from random import *
from pygame.locals import *
import math
import time
import numpy
from enum import Enum




background_color = (255, 255, 255)
height = 600
width = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balls Of Wrath")

pygame.font.init()
myfont = pygame.font.SysFont("monospace", 15)

class Vector(object):
    def __init__(self, back_end_coordinates, front_end_coordinates):
        self.front_pos = front_end_coordinates
        self.back_pos = back_end_coordinates

    def display(self):
        pygame.draw.line(screen, (0,0,0), self.back_pos, self.front_pos, 5)

class VectorArrow(Vector):
    def __init__(self, color, back_pos, front_end_coordinates):
        Vector.__init__(self, back_pos, front_end_coordinates)
        self.color = color
        self.dragging = False
    def get_length(self):
        return math.sqrt((self.front_pos[0] - self.back_pos[0]) ** 2 + (self.front_pos[1] - self.back_pos[1]) ** 2)
    def get_angle(self):
        # if (self.front_pos[0] - self.back_pos[0]) < 0:
        #     angle = (math.atan((self.front_pos[1] - self.back_pos[1]) / (
        #                 self.front_pos[0] - self.back_pos[0]))) + math.pi
        # else:
        #     angle =  math.atan((self.front_pos[1] - self.back_pos[1])/(self.front_pos[0] - self.back_pos[0]))
        angle = math.radians(270)
        return angle
    def displayTri(self):

        triangle_point_center = (self.back_pos[0] + (self.get_length() - 10) * math.cos(self.get_angle()),
                                     self.back_pos[1] + (self.get_length() - 10) * math.sin(self.get_angle()))
        triangle_point_1 = (triangle_point_center[0] + (5 * math.sin(self.get_angle())),
                            triangle_point_center[1] - (5 * math.cos(self.get_angle())))
        triangle_point_2 = self.front_pos
        triangle_point_3 = (triangle_point_center[0] - (5 * math.sin(self.get_angle())),
                            triangle_point_center[1] + (5 * math.cos(self.get_angle())))
        return pygame.draw.polygon(screen, self.color,
                                   (triangle_point_1, triangle_point_2, triangle_point_3), 0)
    def display(self):
        self.displayTri()
        return pygame.draw.line(screen, self.color, self.back_pos, self.front_pos, 5)

class Type(Enum):
    Float_No_Collide = 1
    Float_Collide = 2
    Bounce_No_Collide = 3
    Bounce_Collide = 4


def get_angle(x, y):
    if x < 0:
        angle = (math.atan(y / x)) + math.pi
    else:
        try:
            angle = math.atan(y / x)
        except ZeroDivisionError:
            angle = 0
    return angle

class Ball(object):
    def __init__(self, color, x, y, vx, vy, radius):
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self._in_collision = False
        self.type = type
        self.time = 0
    def display(self):
        return pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    def field_collision(self, board):
        if self.y >= board.floor - ball.radius:
            ball.vy = -1 * (ball.vy)
            ball.y = board.floor - ball.radius
            self.time = 0
        if ball.y <= board.roof + ball.radius:
            ball.vy = -1 * (ball.vy)
            ball.y = board.roof + ball.radius
        if ball.x <= board.left_wall + ball.radius:
            ball.vx = -1 * (ball.vx)
            ball.x = board.left_wall + ball.radius
        if ball.x >= board.right_wall - ball.radius:
            ball.vx = -1 * (ball.vx)
            ball.x = board.right_wall - ball.radius
    def is_balls_collide(self, ball_2):
        total_radius = self.radius + ball_2.radius
        total_distance = math.sqrt(((self.x - ball_2.x) ** 2) + ((self.y - ball_2.y) ** 2))
        if (total_distance <= total_radius):
            return True
        else:
            return False

    def move(self, board, t):
        self.x = self.x + (self.vx * t)
        self.y = self.y + (self.vy * t)
        self.field_collision(board)

    def calculate_velocity(self, t):
        velocity_y = self.vy + ((3.7 * t))
        self.vy = velocity_y


class Ball_Collide(Ball):
    def __init__(self, color, x, y, vx, vy, radius):
        Ball.__init__(self, color, x, y, vx, vy, radius)

    def collide(self, ball_2):
        ball1_vx_initial = self.vx
        ball1_vy_initial = self.vy
        self.vx = ball_2.vx
        self.vy = ball_2.vy
        ball_2.vx = ball1_vx_initial
        ball_2.vy = ball1_vy_initial


class Ball_Float_No_Collide(Ball):
    def __init__(self, color, x, y, vx, vy, radius):
        Ball.__init__(self, color, x, y, vx, vy, radius)



class Ball_Float_Collide(Ball_Collide):
    def __init__(self, color, x, y, vx, vy, radius):
        Ball_Collide.__init__(self, color, x, y, vx, vy, radius)



class Ball_Bounce_Collide(Ball_Collide):
    def __init__(self, color, x, y, vx, vy, radius):
        Ball_Collide.__init__(self, color, x, y, vx, vy, radius)

    def move(self, board, t):
        self.calculate_velocity(t)
        self.x = self.x + (self.vx * t)
        self.y = self.y + (self.vy * t)
        self.field_collision(board)



class Ball_Bounce_No_Collide(Ball):
    def __init__(self, color, x, y, vx, vy, radius):
        Ball.__init__(self, color, x, y, vx, vy, radius)

    def move(self, board, t):
        self.calculate_velocity(t)
        self.x = self.x + (self.vx * t)
        self.y = self.y + (self.vy * t)
        self.field_collision(board)


class Balls(object):
    def __init__(self):
        self.list = []
    def add_balls_to_list(self, number):
        for x in range(number):
            # types = [Type.Float_No_Collide, Type.Float_Collide, Type.Bounce_No_Collide, Type.Bounce_Collide]
            types = [Type.Float_Collide, Type.Bounce_Collide, Type.Bounce_No_Collide]
            type = choice(types)
            if type == Type.Float_No_Collide:
                angle = math.radians(randint(45, 135))
                velocity = 40
                vx = velocity * math.cos(angle)
                vy = velocity * math.sin(angle)
                ball = Ball_Float_No_Collide((0,255,0), 50, randint(25, height / 2 - 100), vx, vy, randint(15,25))
                self.list.append(ball)
            if type == Type.Float_Collide:
                angle = math.radians(randint(45, 135))
                velocity = 40
                vx = velocity * math.cos(angle)
                vy = velocity * math.sin(angle)
                ball = Ball_Float_Collide((255, 0, 0), 50, randint(25, height / 2 - 100), vx, vy, randint(15,25))
                self.list.append(ball)
            if type == Type.Bounce_No_Collide:
                vx = 40
                vy = 0
                ball = Ball_Bounce_No_Collide((253,240,10), 50, randint(25, height / 2 - 100), vx, vy, randint(15,25))
                self.list.append(ball)
            if type == Type.Bounce_Collide:
                vx = 40
                vy = 0
                ball = Ball_Bounce_Collide((0, 0, 255), 50, randint(25, height / 2 - 100), vx, vy, randint(15,25))
                self.list.append(ball)

class Sonic(object):
    def __init__(self, moving_left_image, moving_right_image, center_image, sonic_height, sonic_width, board):
        self.x = width / 2
        self.sonic_height = sonic_height
        self.sonic_width = sonic_width
        self.y = board.floor - self.sonic_height
        self.speed = 5
        self.arrow_capacity = 1
        self.arrows_used = 0
        self.moving_left_image = moving_left_image
        self.moving_right_image = moving_right_image
        self.center_image = center_image
        self.direction = "NONE"
        self.arrow_shooting = False
        self.arrow = None
        self.arrow_speed = 5

    def display_left(self):
        screen.blit(self.moving_left_image, (self.x, self.y))
    def display_right(self):
        screen.blit(self.moving_right_image, (self.x, self.y))
    def display_center(self):
        screen.blit(self.center_image, (self.x, self.y))

    def move_and_display(self, board):
        if self.direction == "NONE":
            self.display_center()
        if self.direction == "RIGHT":
            self.x += self.speed
            self.display_right()
        if self.direction == "LEFT":
            self.x -= self.speed
            self.display_left()
        if sonic.x < board.left_wall:
            sonic.x = board.left_wall
        if sonic.x > board.right_wall - sonic.sonic_width:
            sonic.x = board.right_wall - sonic.sonic_width
        if self.arrow_shooting:
            if self.arrow.front_pos[1] <= board.roof:
                self.arrow_shooting = False
            else:
                self.arrow.front_pos = (self.arrow.front_pos[0] , self.arrow.front_pos[1] - self.arrow_speed)
                self.arrow.display()

    def field_collision_with_sonic(self, balls):
        for i in range(0, len(balls.list)):
            if self.is_sonic_collide_with_ball(balls.list[i]):
                    print("Sonic is Killed!")
    def is_sonic_collide_with_ball(self, ball):
        total_radius = self.sonic_width/2 + ball.radius
        total_distance = math.sqrt((((self.x + self.sonic_width/2)  - ball.x) ** 2) + (((self.y + self.sonic_height/2) - ball.y) ** 2))
        if (total_distance <= total_radius):
            return True
        else:
            return False

class Board(object):
    def __init__(self):
        self.left_wall = 0
        self.right_wall = width
        self.floor = height - 100
        self.roof = 0
    def display(self, color, size):
        pygame.draw.line(screen, color, (self.left_wall, self.roof), (self.left_wall, self.floor), size)
        pygame.draw.line(screen, color, (self.left_wall, self.roof), (self.right_wall, self.roof), size)
        pygame.draw.line(screen, color, (self.right_wall, self.roof), (self.right_wall, self.floor), size)
        pygame.draw.line(screen, color, (self.left_wall, self.floor), (self.right_wall, self.floor), size)
    def detect_collisions(self, balls, in_collision):
        for i in range(0, len(balls.list)):
            for j in range(i + 1, len(balls.list)):
                if balls.list[i].is_balls_collide(balls.list[j]):
                    if not in_collision[i][j]:
                        if isinstance(balls.list[i], Ball_Collide) and isinstance(balls.list[j], Ball_Collide):
                            balls.list[i].collide(balls.list[j])
                            in_collision[i][j] = True

                else:
                    in_collision[i][j] = False

def implement_sonic_keys(event, sonic, board):
    if event.type == KEYDOWN:
        if event.key == K_RIGHT:
            sonic.direction = "RIGHT"
        if event.key == K_LEFT:
            sonic.direction = "LEFT"
        if event.key == K_UP:
            if sonic.arrow_shooting == False:
                sonic.arrow_shooting = True
                sonic.arrow = VectorArrow((0, 0, 0), (sonic.x + (sonic.sonic_width / 2), board.floor), (sonic.x + (sonic.sonic_width / 2), board.floor - 75))
    elif event.type == KEYUP:
        if event.key == K_RIGHT:
            if sonic.direction == "RIGHT":
                sonic.direction = "NONE"
        if event.key == K_LEFT:
            if sonic.direction == "LEFT":
                sonic.direction = "NONE"



#SETUP
#physical
balls = Balls()
balls.add_balls_to_list(3)

board = Board()
sonic_left = pygame.image.load("sonic_left.png")
sonic_left = pygame.transform.scale(sonic_left, (75,75))
sonic_right = pygame.image.load("sonic_right.png")
sonic_right = pygame.transform.scale(sonic_right, (75,75))
sonic_center = pygame.image.load("sonic_center.png")
sonic_center = pygame.transform.scale(sonic_center, (75,75))
sonic = Sonic(sonic_left, sonic_right ,sonic_center, 75, 75, board)

#action
in_collision = [[False] * 10 for i in range(10)]


clock = pygame.time.Clock()
clock.tick()

#gameplay
while 1:
    screen.fill(background_color)
    board.display((0, 0, 0), 10)
    seconds = clock.tick() / 100
    #calculate_velocity(seconds, velocity)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        implement_sonic_keys(event, sonic, board)

    sonic.move_and_display(board)
    sonic.field_collision_with_sonic(balls)

    board.detect_collisions(balls, in_collision)

    for ball in balls.list:
        ball.display()
        ball.move(board, seconds)

    pygame.display.flip()
    pygame.time.delay(10)

'''
pygame.image.load("tux.png")
screen.blit(tux,(200,200))
resize--> tux = pygame.transform.scale(tux, (100,100))
look out sound bible, get a wav file, in working folder
sound = pygame.mixer.Sound('start.wave')
sound.play()

elif event.type == KEYDOWN:
    if event.key == K_ESCAPE:
    
elif event.type == MOUSEBUTTONDOWN:

speed--> 
clock = pygame.time.Clock()
Clock.tick(60)

mx,my = pygame.mouse.get_pos()

bg Image -->
bg = pygame.image.load()

screen.blit(bg,(0,0))

'''
