'''
Created on 2013-05-28

@author: brian
'''

from pygame.draw import circle
from collections import deque

class Arrow:
	  
	def __init__(self, origin, targetLocation, color = (0xAA, 0x55, 0x00), targetEntity=None, fire=None, impact=None):
		self.particals = deque()
		self.maxParticals = 10
		self.targetEntity = targetEntity
		self.pos = self.origin = float(origin[0]) + 0.5, float(origin[1]) + 0.5
		self.granularity = 15
		self.fire = fire
		self.impact = impact
		
		if targetEntity is not None:
			self.target = float(targetEntity.position[0]) + 0.5, float(targetEntity.position[1]) + 0.5
		else:
			self.target = float(targetLocation[0]) + 0.5, float(targetLocation[1]) + 0.5
		
		self.vx = (float(self.target[0]) - self.origin[0]) / self.granularity
		self.vy = (float(self.target[1]) - self.origin[1]) / self.granularity

		for i in xrange(10):
			self.particals.append((self.vx * i * 2, self.vy * i * 2))

		if self.fire is not None:
			self.fire()
		self.color = color
		self.done = False

	def update(self):
		
		if self.targetEntity is not None:
			self.target = float(self.targetEntity.position[0]) + 0.5, float(self.targetEntity.position[1]) + 0.5
			self.vx = (float(self.target[0]) - self.origin[0]) / self.granularity
			self.vy = (float(self.target[1]) - self.origin[1]) / self.granularity
				
		if (int(self.pos[0]), int(self.pos[1])) == (int(self.target[0]), int(self.target[1])):
			self.done = True
			if self.impact is not None:
				self.impact()
			return

		self.pos = self.pos[0] + self.vx, self.pos[1] + self.vy
	
	def draw(self, surface, centerPos):

		if self.done:
			return

		offsetX = (self.pos[0] - self.origin[0]) * 32
		offsetY = (self.pos[1] - self.origin[1]) * 32
		x = int(16 + (centerPos[0] + offsetX))
		y = int(16 + (centerPos[1] + offsetY))
		
		for partical in self.particals:
			px = int(x + partical[0])
			py = int(y + partical[1])
			circle(surface, self.color, (px, py), 2)
			

