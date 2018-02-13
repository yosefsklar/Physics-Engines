#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creating a Pygame window
"""

import sys, pygame
pygame.init()

background_color = (0,255,255) #seems like we can call fields
(width, height) = (320, 240)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Exercise 1')

screen.fill(background_color)
pygame.display.flip()

#logic to end the program
while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()


