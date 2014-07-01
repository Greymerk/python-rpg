import pygame
import random

from math import hypot
from collections import deque

class Star:

	ballSize = 3
	scatter = 5
	maxParticals = 10
	granularity = 15
	
	def __init__(self, origin, targetLocation, color, fire=None, impact=None):
		self.particals = deque()
		self.pos = self.origin = float(origin[0]) + 0.5, float(origin[1]) + 0.5
		self.fire = fire
		self.impact = impact
		self.target = float(targetLocation[0]) + 0.5, float(targetLocation[1]) + 0.5
		
		dx = abs(float(origin[0]) - targetLocation[0])
		dy = abs(float(origin[1]) - targetLocation[1])
		dist = int(hypot(dx, dy))
		if dist is 0:
			dist = 1
		
		self.vx = (float(self.target[0]) - self.origin[0]) / (2 * dist)
		self.vy = (float(self.target[1]) - self.origin[1]) / (2 * dist)

		if self.fire is not None:
			self.fire()
		self.color = color
		self.done = False

	def update(self):
		
		if (int(self.pos[0]), int(self.pos[1])) == (int(self.target[0]), int(self.target[1])):
			self.done = True
			if self.impact is not None:
				self.impact()
			return

		self.pos = self.pos[0] + self.vx, self.pos[1] + self.vy
		
		x, y = self.pos
		
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
		relx = self.origin[0] - camPos[0]
		rely = self.origin[1] - camPos[1]
		center = (((relx + 8) * tileSize), ((rely + 8) * tileSize))
			
		offsetX = (self.pos[0] - self.origin[0]) * tileSize
		offsetY = (self.pos[1] - self.origin[1]) * tileSize
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
			

