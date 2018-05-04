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
    def add_balls_to_list(self):
        for x in range(10):
            types = [Type.Float_No_Collide, Type.Float_Collide, Type.Bounce_No_Collide, Type.Bounce_Collide]
            type = choice(types)
            if type == Type.Float_No_Collide:
                angle = math.radians(randint(45, 135))
                velocity = 40
                vx = velocity * math.cos(angle)
                vy = velocity * math.sin(angle)
                ball = Ball_Float_No_Collide((255, 0, 0), 50, randint(25, height / 2 - 100), vx, vy, randint(15,25))
                self.list.append(ball)
            elif type == Type.Float_Collide:
                angle = math.radians(randint(45, 135))
                velocity = 40
                vx = velocity * math.cos(angle)
                vy = velocity * math.sin(angle)
                ball = Ball_Float_Collide((253,240,10), 50, randint(25, height / 2 - 100), vx, vy, randint(15,25))
                self.list.append(ball)
            elif type == Type.Bounce_No_Collide:
                vx = 40
                vy = 0
                ball = Ball_Bounce_No_Collide((0, 255, 0), 50, randint(25, height / 2 - 100), vx, vy, randint(15,25))
                self.list.append(ball)
            elif type == Type.Bounce_Collide:
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

    def display_left(self):
        screen.blit(self.moving_left_image, (self.x, self.y))
    def display_right(self):
        screen.blit(self.moving_right_image, (self.x, self.y))
    def display_center(self):
        screen.blit(self.center_image, (self.x, self.y))

    def move_and_display(self):
        if self.direction == "NONE":
            self.display_center()
        if self.direction == "RIGHT":
            self.x += self.speed
            self.display_right()
        if self.direction == "LEFT":
            self.x -= self.speed
            self.display_left()

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

def implement_sonic_keys(event, sonic):
    if event.type == KEYDOWN:
        if event.key == K_RIGHT:
            sonic.direction = "RIGHT"
        if event.key == K_LEFT:
            sonic.direction = "LEFT"
    elif event.type == KEYUP:
        if event.key == K_RIGHT:
            if sonic.direction == "RIGHT":
                sonic.direction = "NONE"
        if event.key == K_LEFT:
            if sonic.direction == "LEFT":
                sonic.direction = "NONE"
        #if event.key == K_UP:
            #sonic.shoot()

#SETUP
#physical
balls = Balls()
balls.add_balls_to_list()

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
        implement_sonic_keys(event, sonic)

    sonic.move_and_display()

    #
    # board.detect_collisions(balls, in_collision)
    #
    # for ball in balls.list:
    #     ball.display()
    #     ball.move(board, seconds)

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
