
from pygame.locals import *
from vector import Vector2
from enum import enum
from random import choice

class Cardinal(object):

	directions = enum('NORTH', 'EAST', 'WEST', 'SOUTH')
	
	key_map = {}
	key_map[K_UP] =	directions.NORTH
	key_map[K_DOWN] = directions.SOUTH
	key_map[K_LEFT] = directions.WEST
	key_map[K_RIGHT] = directions.EAST

	names = {}
	names[directions.NORTH] = "North"
	names[directions.SOUTH] = "South"
	names[directions.WEST] = "West"
	names[directions.EAST] = "East"
	
	values = {}
	values[directions.NORTH] = Vector2(0, -1)
	values[directions.SOUTH] = Vector2(0, 1)
	values[directions.WEST] = Vector2(-1, 0)
	values[directions.EAST] = Vector2(1, 0)

	@staticmethod
	def choice():
		return choice(Cardinal.values.values())


if __name__ == '__main__' :
	print K_UP in Cardinal.key_map.keys()
