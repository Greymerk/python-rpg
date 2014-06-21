#!/usr/bin/python

import time
import pygame

from world import World
from gui import Gameview
from player import Player
from images import ImageCache

seed = 26281376

pygame.init()
screenSize = (1024, 600)
surface = pygame.display.set_mode(screenSize)
pygame.display.set_caption("RPG Game")

world = World(seed)
user = Player(world)
view = Gameview(world, user, surface, ImageCache())

clock = pygame.time.Clock()

while(True):
	
	clock.tick(20)
	view.draw()

	if not world.update():
		continue
	
	if(user.turn()):
		continue

	world.turn()
	user.save()
	
	
