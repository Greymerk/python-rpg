'''
Created on 2013-05-28

@author: brian
'''

from math import hypot

from pygame.draw import circle
from collections import deque

class Arrow:
	
	def __init__(self, origin, endLocation, color = (0xAA, 0x55, 0x00), fire=None, impact=None):
		
		self.particals = deque()
		self.maxParticals = 10
		
		self.start = self.pos = float(origin[0]) + 0.5, float(origin[1]) + 0.5
		self.end = float(endLocation[0]) + 0.5, float(endLocation[1]) + 0.5
		
		self.color = color
		self.fire = fire
		self.impact = impact
		
		dx = abs(float(origin[0]) - endLocation[0])
		dy = abs(float(origin[1]) - endLocation[1])
		dist = int(hypot(dx, dy))
		if dist is 0:
			dist = 1
		
		self.vx = (float(self.end[0]) - self.start[0]) / (2 * dist)
		self.vy = (float(self.end[1]) - self.start[1]) / (2 * dist)
		
		self.trail = deque()
		
		for i in xrange(10):
			self.particals.append((self.vx * i * 2, self.vy * i * 2))

		if self.fire is not None:
			self.fire()

		self.done = False

	def update(self):
		
		tx = abs(float(self.pos[0]) - float(self.start[0]))
		ty = abs(float(self.pos[1]) - float(self.start[1]))
		distTravel = int(hypot(tx, ty))
		
		dx = abs(float(self.start[0]) - float(self.end[0]))
		dy = abs(float(self.start[1]) - float(self.end[1]))
		distTotal = int(hypot(dx, dy))
			
		if (distTravel >= distTotal):
			self.done = True
			if self.impact is not None:
				self.impact()
			return

		self.pos = self.pos[0] + self.vx, self.pos[1] + self.vy
	
	def draw(self, surface, camPos, visible):

	
		tileSize = 32
		relx = self.start[0] - camPos[0]
		rely = self.start[1] - camPos[1]
		center = (((relx + 8) * tileSize), ((rely + 8) * tileSize))
	
		offsetX = (self.pos[0] - self.start[0]) * tileSize
		offsetY = (self.pos[1] - self.start[1]) * tileSize
		x = int((center[0] + offsetX))
		y = int((center[1] + offsetY))
		
		pos = (int(self.pos[0]), int(self.pos[1]))
		
		if not visible(pos):
			return

		for partical in self.particals:
			px = int(x + partical[0])
			py = int(y + partical[1])
			circle(surface, self.color, (px, py), 2)
			

