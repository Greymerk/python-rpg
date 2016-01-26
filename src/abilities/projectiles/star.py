import pygame
import random

from src.util import Vector2
from math import hypot
from collections import deque

class Star:

	ballSize = 3
	scatter = 8
	maxParticals = 20
	granularity = 15
	
	def __init__(self, start, end, color, fire=None, impact=None):
		self.start = start
		self.end = end

		self.fire = fire
		self.impact = impact

		self.particals = deque()

		self.pos = self.origin = Vector2(float(start[0]), float(start[1]))
		self.pos.center()
		self.target = Vector2(float(end[0]), float(end[1]))
		self.target.center()
		
		dist = self.pos.dist(self.target)
		if int(dist) == 0:
			dist = 1 

		vx = (float(self.target.x) - self.origin.x) / (3 * dist)
		vy = (float(self.target.y) - self.origin.y) / (3 * dist)
		self.velocity = Vector2(vx, vy)

		if self.fire is not None:
			self.fire()

		self.color = color
		self.done = False

	def update(self):
		
		if (int(self.pos.x), int(self.pos.y)) == (int(self.target.x), int(self.target.y)):
			self.done = True
			if self.impact is not None:
				self.impact()
			return

		self.pos + self.velocity
		
		x, y = (self.pos.x, self.pos.y)
		
		while len(self.particals) > Star.maxParticals:
			self.particals.popleft()

		for i in xrange(3):
			s = Star.scatter
			newPartical = (x + float(random.randint(-s,s))/32, y + float(random.randint(-s,s))/32)
			self.particals.append(newPartical)

	def draw(self, surface, camPos, visible):

		if self.done:
			return

		tileSize = 32
		relx = self.origin.x - camPos[0]
		rely = self.origin.y - camPos[1]
		center = (((relx + 8) * tileSize), ((rely + 8) * tileSize))
			
		offsetX = (self.pos.x - self.origin.x) * tileSize
		offsetY = (self.pos.y - self.origin.y) * tileSize
		x = int((center[0] + offsetX))
		y = int((center[1] + offsetY))
		
		if not visible(self.pos):
			return
		
		pygame.draw.circle(surface, self.color, (x, y), Star.ballSize)
		
		for partical in self.particals:
			offsetX = (partical[0] - self.origin[0]) * tileSize
			offsetY = (partical[1] - self.origin[1]) * tileSize
			x = int((center[0] + offsetX))
			y = int((center[1] + offsetY))
			surface.set_at((x, y), self.color)
			surface.set_at((x, y + 1), self.color)
			surface.set_at((x + 1, y), self.color)
			surface.set_at((x + 1, y + 1), self.color)
			

