import sys, pygame, pygame.mixer
from random import *
from pygame.locals import *
import math
import time
import numpy
from enum import Enum
from time import sleep

#WELCOME to "Balls of Wrath" Code is explained in the comments

#Basic setup
background_color = (255, 255, 255)
height = 600
width = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balls Of Wrath")

pygame.font.init()

#Setup for the Arrows that are being shot
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


#Setup for the three different typed of balls
class Type(Enum):
    Float_Collide = 2
    Bounce_No_Collide = 3
    Bounce_Collide = 4

#(a helper method)
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
    def __init__(self, color, x, y, vx, vy, radius, mass):
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
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
# TAKING GRAVITY INTO ACCOUNT for the 2 type of balls that do
    def calculate_velocity(self, t):
        velocity_y = self.vy + ((3.7 * t))
        self.vy = velocity_y


class Ball_Collide(Ball):
    def __init__(self, color, x, y, vx, vy, radius, mass):
        Ball.__init__(self, color, x, y, vx, vy, radius, mass)

    #Results of Collisions TAKING INTO ACCOUNT DIFFERENT MASSES
    def collide(self, ball_2):

        v2xi = ball_2.vx
        ball_2.vx = ((self.mass * self.vx + ball_2.mass * ball_2.vx) - ((ball_2.vx - self.vx) * self.mass))/(self.mass + ball_2.mass)
        self.vx = ball_2.vx + v2xi - self.vx

        v2yi = ball_2.vy
        ball_2.vy = ((self.mass * self.vy + ball_2.mass * ball_2.vy) - ((ball_2.vy - self.vy) * self.mass))/(self.mass + ball_2.mass)
        self.vy = ball_2.vy + v2yi - self.vy



class Ball_Float_Collide(Ball_Collide):
    def __init__(self, color, x, y, vx, vy, radius, mass):
        Ball_Collide.__init__(self, color, x, y, vx, vy, radius, mass)


class Ball_Bounce_Collide(Ball_Collide):
    def __init__(self, color, x, y, vx, vy, radius, mass):
        Ball_Collide.__init__(self, color, x, y, vx, vy, radius, mass)

    def move(self, board, t):
        self.calculate_velocity(t)
        self.x = self.x + (self.vx * t)
        self.y = self.y + (self.vy * t)
        self.field_collision(board)


class Ball_Bounce_No_Collide(Ball):
    def __init__(self, color, x, y, vx, vy, radius, mass):
        Ball.__init__(self, color, x, y, vx, vy, radius, mass)

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
            types = [Type.Float_Collide, Type.Bounce_Collide, Type.Bounce_No_Collide]
            type = choice(types)
            if type == Type.Float_Collide:
                angle = math.radians(randint(40, 50))
                velocity = 25
                vx = velocity * math.cos(angle)
                vy = velocity * math.sin(angle)
                radius = randint(15, 25)
                # ratio of volume to radius for a sphere
                mass = radius ** 3
                ball = Ball_Float_Collide((255, 0, 0), 50, randint(25, height / 2 - 100), vx, vy, radius, mass)
                self.list.append(ball)
            if type == Type.Bounce_No_Collide:
                angle = math.radians(randint(40, 50))
                velocity = 25
                vx = velocity * math.cos(angle)
                vy = velocity * math.sin(angle)
                radius = randint(15, 25)
                # ratio of volume to radius for a sphere
                mass = radius ** 3
                ball = Ball_Bounce_No_Collide((253,240,10), 50, randint(25, height / 2 - 100), vx, vy, radius, mass)
                self.list.append(ball)
            if type == Type.Bounce_Collide:
                angle = math.radians(randint(40, 50))
                velocity = 25
                vx = velocity * math.cos(angle)
                vy = velocity * math.sin(angle)
                # ratio of volume to radius for a sphere
                radius = randint(15, 25)
                mass = radius ** 3
                ball = Ball_Bounce_Collide((0, 0, 135), 50, randint(25, height / 2 - 100), vx, vy, radius, mass)
                self.list.append(ball)

#Setting up Sonic

class Sonic(object):
    def __init__(self, moving_left_image, moving_right_image, center_image, dead_image, sonic_height, sonic_width, board, lives):
        self.x = width / 2
        self.sonic_height = sonic_height
        self.sonic_width = sonic_width
        self.y = board.floor - self.sonic_height
        self.speed = 6
        self.arrow_capacity = 1
        self.arrows_used = 0
        self.moving_left_image = moving_left_image
        self.moving_right_image = moving_right_image
        self.center_image = center_image
        self.dead_image = dead_image
        self.direction = "NONE"
        self.arrow_shooting = False
        self.arrow = None
        self.arrow_speed = 6
        self.points = 0
        self.lives = lives
        self.in_loss_of_life = False
        self.score = 0

    def display_left(self):
        screen.blit(self.moving_left_image, (self.x, self.y))
    def display_right(self):
        screen.blit(self.moving_right_image, (self.x, self.y))
    def display_center(self):
        screen.blit(self.center_image, (self.x, self.y))
    def display_dead(self):
        screen.blit(self.dead_image, (self.x, self.y))

    def move_and_display(self, board):
        if self.in_loss_of_life:
            self.display_dead()
        elif self.direction == "NONE":
            self.display_center()
        elif self.direction == "RIGHT":
            self.x += self.speed
            self.display_right()
        elif self.direction == "LEFT":
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
#Implementing what happens when sonic comes into contact with either balls, coins, stars or bombs
    def field_collision_with_sonic(self, balls, items):
        for i in balls.list:
            if self.is_sonic_collide_with_ball(i):
                if not self.in_loss_of_life:
                    self.lives = self.lives - 1
                    pygame.time.set_timer(wait_for_loss_of_life, 500)
                    self.in_loss_of_life = True
            if self.arrow_shooting:
                arrow = self.arrow.display()
                if arrow.colliderect(i.display()):
                    balls.list.remove(i)
                    self.arrow_shooting = False
        for i in items.list:
            if self.is_sonic_collide_with_item(i):
                if isinstance(i, Star):
                    self.score = self.score + 300
                if isinstance(i, Coin):
                    self.score = self.score + 100
                if isinstance(i, Bomb):
                    balls.list.clear()
                items.list.remove(i)

        return True
    def is_sonic_collide_with_ball(self, ball):
        total_radius = self.sonic_width/4 + ball.radius
        total_distance = math.sqrt((((self.x + self.sonic_width/2)  - ball.x) ** 2) + (((self.y + self.sonic_height/2) - ball.y) ** 2))
        if (total_distance <= total_radius):
            return True
        else:
            return False
    def is_sonic_collide_with_item(self, item):
       if self.x < item.x + item.width - 10 and self.x > item.x + 10:
           return True
       elif self.x + self.sonic_width < item.x + item.width - 10 and self.x + self.sonic_width > item.x + 10:
            return True
       else:
           return False

#Setting up items
class Item(object):
    def __init__(self, board, x):
        self.image = None
        self.height = 45
        self.width = 45
        self.x = x
        self.y = board.floor - self.height
    def display(self):
        screen.blit(self.image, (self.x, self.y))

class Coin(Item):
    def __init__(self, board, x):
        Item.__init__(self, board, x)
        self.value = 100
        self.image = pygame.transform.scale(pygame.image.load("coin.png"), (self.width, self.height - 10))

class Star(Item):
    def __init__(self, board, x):
        Item.__init__(self, board, x)
        self.value = 300
        self.image = pygame.transform.scale(pygame.image.load("star.png"), (self.width, self.height - 10))
class Bomb(Item):
    def __init__(self, board, x):
        Item.__init__(self, board, x)
        self.image = pygame.transform.scale(pygame.image.load("bomb.png"), (self.width, self.height - 10))

class Items(object):
    def __init__(self, board):
        self.list = []


class Board(object):
    def __init__(self, image):
        self.left_wall = 0
        self.right_wall = width
        self.floor = height - 100
        self.roof = 0
        self.image = pygame.transform.scale(pygame.image.load(image), (self.right_wall - self.left_wall, self.floor - self.roof))
    def display(self, color, size):
        screen.blit(self.image, (self.left_wall, self.roof))
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
                sonic.arrow = VectorArrow((0, 0 ,0), (sonic.x + (sonic.sonic_width / 2), board.floor), (sonic.x + (sonic.sonic_width / 2), board.floor - 75))
    elif event.type == KEYUP:
        if event.key == K_RIGHT:
            if sonic.direction == "RIGHT":
                sonic.direction = "NONE"
        if event.key == K_LEFT:
            if sonic.direction == "LEFT":
                sonic.direction = "NONE"

def add_balls(event, board, balls, round_count):
    if event.type == ball_added:
        balls.add_balls_to_list(1)
        round_count = round_count + 1
    return round_count

def add_items(event, board, items, coin_count):
    if event.type == coin_added:
        if len(items.list) != 0:
            items.list.clear()
        if coin_count % 12 == 0:
            items.list.append(Bomb(board, randint(board.left_wall, board.right_wall - 50)))
            coin_count  = coin_count + 1
        elif coin_count % 5 == 0:
            items.list.append(Star(board, randint(board.left_wall, board.right_wall - 50)))
            coin_count = coin_count + 1
        else:
            items.list.append(Coin(board, randint(board.left_wall, board.right_wall - 50)))
            coin_count = coin_count + 1
    print(str(coin_count))
    return coin_count

#SETUP for the game
balls = Balls()
balls.add_balls_to_list(1)
board = Board("background.png")
items = Items(board)
sonic_left = pygame.image.load("sonic_left.png")
sonic_left = pygame.transform.scale(sonic_left, (75,75))
sonic_right = pygame.image.load("sonic_right.png")
sonic_right = pygame.transform.scale(sonic_right, (75,75))
sonic_center = pygame.image.load("sonic_center.png")
sonic_center = pygame.transform.scale(sonic_center, (75,75))
sonic_dead = pygame.image.load("sonic_hurt.png")
sonic_dead = pygame.transform.scale(sonic_dead, (75,75))
sonic = Sonic(sonic_left, sonic_right ,sonic_center, sonic_dead, 75, 75, board, 3)

#An array to make sure balls are considered as "colliding with each other" multiple times per collision
in_collision = [[False] * 100 for i in range(100)]


clock = pygame.time.Clock()
clock.tick()


#timed events
ball_added = USEREVENT + 1
coin_added = USEREVENT + 2
wait_for_loss_of_life= USEREVENT + 3
count = USEREVENT + 4
ball_added_timer = 4000
pygame.time.set_timer(count, 1000)
pygame.time.set_timer(ball_added, ball_added_timer)
pygame.time.set_timer(coin_added, 2500)
round_count = 0
coin_count = 1
#gameplay
time = 0
playing = False
welcome_message = "Play"
count_down = 3
counting_down = False
game_over = False
high_score = 0
while 1:
    #THIS CODE SETS UP THE HOME SCREEN
    screen.fill((0,0,0))
    sonic_home = pygame.image.load("sonic_home.png")
    sonic_home = pygame.transform.scale(sonic_home, (60,60))
    screen.blit(sonic_home, (width / 2 -30, 5))

    welcome_font = pygame.font.SysFont("ariel", 40)
    welcome_font.set_underline(True)
    welcome_font.set_bold(True)
    score = welcome_font.render("Balls of Wrath", 1, (0, 0, 255))
    screen.blit(score, (width/ 2 -110, 75))

    instructions_font = pygame.font.SysFont("ariel", 40)
    instructions_font = pygame.font.SysFont("monospace", 15)
    instructions_font.set_bold(True)
    instruction_1 = instructions_font.render("Collect as many points as you can while avoiding the bouncing balls", 1, (255, 255, 255))
    screen.blit(instruction_1, (width / 2 - 300, 130))

    instruction_2 = instructions_font.render("Destroy balls by shooting them with arrows", 1,(255, 255, 255))
    screen.blit(instruction_2, (width / 2 - 175, 150))

    instruction_3 = instructions_font.render("Collect Coin = 100 points", 1, (255, 255, 255))
    screen.blit(instruction_3, (width / 2 - 150, 190))

    instruction_4 = instructions_font.render("Clear Field of All Balls = 200", 1, (255, 255, 255))
    screen.blit(instruction_4, (width / 2 - 150, 210))

    instruction_5 = instructions_font.render("Collect Star = 300 points", 1, (255, 255, 255))
    screen.blit(instruction_5, (width / 2 - 150, 230))
    instruction_5 = instructions_font.render("Collect Bomb = 200 points, all balls are destroyed", 1, (255, 255, 255))
    screen.blit(instruction_5, (width / 2 - 150, 250))

    instruction_6 = instructions_font.render("MOVE LEFT using the Left Arrow Key", 1, (255, 255, 255))
    screen.blit(instruction_6, (width / 2 - 175, 270))

    instruction_7 = instructions_font.render("MOVE RIGHT using the Right Arrow Key", 1, (255, 255, 255))
    screen.blit(instruction_7, (width / 2 - 175, 290))

    instruction_8 = instructions_font.render("SHOOT AN ARROW using the UP Arrow Key", 1, (255, 255, 255))
    screen.blit(instruction_8, (width / 2 - 175, 310))

    play_button = pygame.draw.rect(screen, (0, 0, 255), (width / 2 - 75, height - 150, 150, 75))
    welcome_font = pygame.font.SysFont("ariel", 40)
    score = welcome_font.render(str(welcome_message), 1, (0, 0, 0))
    if welcome_message == "Play Again":
        screen.blit(score, (width / 2 - 75 , height - 150 + 25))
        instruction_9 = instructions_font.render("High Score: " + str(high_score), 1, (255, 255, 255))
        screen.blit(instruction_9, (width/2 - 75, height - 50))
    else:
        screen.blit(score, (width/2 - 75 + 45, height - 150 + 25))

    instruction_10 = instructions_font.render("Physics: There are three types of balls in the game. Blue balls", 1, (255, 255, 255))
    screen.blit(instruction_10, (width / 2 - 300, height - 250))

    instruction_11 = instructions_font.render("and Yellow balls are affected by gravity, Red balls are not.", 1, (255, 255, 255))
    screen.blit(instruction_11, (width / 2 - 300, height - 230))

    instruction_12 = instructions_font.render("Blue balls and Red balls collide with other balls, Yellow balls", 1, (255, 255, 255))
    screen.blit(instruction_12, (width / 2 - 300, height - 210))

    instruction_13 = instructions_font.render("do not. Each ball has a mass relative to thier volume and (by ", 1, (255, 255, 255))
    screen.blit(instruction_13, (width / 2 - 300, height - 190))

    instruction_14 = instructions_font.render("extension, thier radius). All collision are calculated accordingly.", 1, (255, 255, 255))
    screen.blit(instruction_14, (width / 2 - 300, height - 170))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if play_button.collidepoint(event.pos):
                counting_down = True
    clock.tick()

    while counting_down:
    #THIS CODE SETS UP THE COUNTDOWN
        screen.fill(background_color)
        board.display((0, 0, 0), 10)
        sonic.display_center()
        for ball in balls.list:
            ball.display()
            for item in items.list:
                item.display()
        countdown = welcome_font.render(str(count_down) + "!", 1, (0, 0, 0))
        screen.blit(countdown, (width / 2 - 20, height / 2))

        pygame.display.flip()
        if count_down == 0:
            pygame.time.set_timer(ball_added, ball_added_timer)
            pygame.time.set_timer(coin_added, 2500)
            count_down = count_down - 1
            pygame.time.set_timer(count, 0)
            counting_down = False
            playing = True
        if count_down > 0:

            for event in pygame.event.get():
                if event.type == count:
                    count_down = count_down - 1
        clock.tick()

    while playing:
    #THIS CODE SETS UP THE ACTUAL GAMEPLAY
        if game_over:
            screen.fill(background_color)
            board.display((0, 0, 0), 10)
            gameOver = welcome_font.render("Game Over", 1, (0, 0, 255))
            screen.blit(gameOver, (width / 2 - 75, height / 2 - 100))
            final_score = welcome_font.render("Score: " + str(sonic.score), 1, (0, 0, 255))
            screen.blit(final_score, (width / 2 - 65, height / 2))
            playing = False
            game_over = False
            count_down = 3
            ball_added_timer = 4000
            if sonic.score > high_score:
                high_score = sonic.score
            pygame.time.set_timer(count, 1000)
            pygame.display.flip()
            sonic = Sonic(sonic_left, sonic_right ,sonic_center, sonic_dead, 75, 75, board, 3)
            balls = Balls()
            balls.add_balls_to_list(1)
            items = Items(board)
            round_count = 0
            coin_count = 1
            welcome_message = "Play Again"
            pygame.time.delay(5000)


        else:
            screen.fill(background_color)
            board.display((0, 0, 0), 10)
            seconds = clock.tick(60) / 100
            time  = time + 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                round_count = add_balls(event, board, balls, round_count)
                coin_count = add_items(event, board, items, coin_count)
                if event.type == wait_for_loss_of_life:
                    sonic.in_loss_of_life = False
                if len(balls.list) == 0:
                    balls.add_balls_to_list(5)
                    sonic.score = sonic.score + 200
                if round_count % 10 == 0 and round_count > 0:
                    if ball_added_timer > 1000:
                        ball_added_timer = int(ball_added_timer - (ball_added_timer / 8))
                        pygame.time.set_timer(ball_added, ball_added_timer)
                implement_sonic_keys(event, sonic, board)

            sonic.move_and_display(board)
            sonic.field_collision_with_sonic(balls, items)

            board.detect_collisions(balls, in_collision)

            for ball in balls.list:
                ball.display()
                ball.move(board, seconds)
            for item in items.list:
                item.display()
            myfont = pygame.font.SysFont("monospace", 30)
            score = myfont.render("Lives: " + str(sonic.lives), 1, (0, 0, 0))
            screen.blit(score, (width - 300, height - 60))

            score = myfont.render("Score: " + str(sonic.score), 1, (0, 0, 0))
            screen.blit(score, (150 , height - 60))

            pygame.display.flip()

            if sonic.lives == 0:
                game_over = True
        #pygame.time.delay(10)
