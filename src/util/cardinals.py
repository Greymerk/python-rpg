
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

	@staticmethod
	def toward(pos, tar):
		diff = Vector2(tar)
		diff -= pos
		if pos == tar: 
			return None

		if abs(diff[0]) > abs(diff[1]):
			if diff[0] < 0:
				return Cardinal.directions.WEST
			else:
				return Cardinal.directions.EAST
		else:
			if diff[1] < 0:
				return Cardinal.directions.NORTH
			else:
				return Cardinal.directions.SOUTH 

if __name__ == '__main__' :
	print K_UP in Cardinal.key_map.keys()
