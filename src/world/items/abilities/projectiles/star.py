import pygame, random
from collections import deque

class Star:
	
	tileSize = 32
	ballSize = 3
	scatter = 5
	maxParticals = 10
	granularity = 15
	
	def __init__(self, origin, targetLocation, color, targetEntity = None, fire=None, impact=None):
		self.particals = deque()
		self.targetEntity = targetEntity
		self.pos = self.origin = float(origin[0]) + 0.5, float(origin[1]) + 0.5
		self.fire = fire
		self.impact = impact
		if targetEntity is not None:
			self.target = float(targetEntity.position[0]) + 0.5, float(targetEntity.position[1]) + 0.5
		else:
			self.target = float(targetLocation[0]) + 0.5, float(targetLocation[1]) + 0.5
		
		self.vx = (float(self.target[0]) - self.origin[0]) / Star.granularity
		self.vy = (float(self.target[1]) - self.origin[1]) / Star.granularity

		if self.fire is not None:
			self.fire()
		self.color = color
		self.done = False

	def update(self):
		
		if self.targetEntity is not None:
			self.target = float(self.targetEntity.position[0]) + 0.5, float(self.targetEntity.position[1]) + 0.5
			self.vx = (float(self.target[0]) - self.origin[0]) / Star.granularity
			self.vy = (float(self.target[1]) - self.origin[1]) / Star.granularity
				
		if (int(self.pos[0]), int(self.pos[1])) == (int(self.target[0]), int(self.target[1])):
			self.done = True
			if self.impact is not None:
				self.impact()
			return

		self.updateStar()
		self.updateParticles()
		
	
	def updateStar(self):

		self.pos = self.pos[0] + self.vx, self.pos[1] + self.vy
	
	def updateParticles(self):

		x, y = self.pos
		
		while len(self.particals) > Star.maxParticals:
			self.particals.popleft()

		for i in xrange(3):
			s = Star.scatter
			newPartical = (x + float(random.randint(-s,s))/32, y + float(random.randint(-s,s))/32)
			self.particals.append(newPartical)

	def draw(self, surface, centerPos, visible):

		if self.done:
			return

		offsetX = (self.pos[0] - self.origin[0]) * Star.tileSize
		offsetY = (self.pos[1] - self.origin[1]) * Star.tileSize
		x = int(16 + (centerPos[0] + offsetX))
		y = int(16 + (centerPos[1] + offsetY))
		
		if not visible(self.pos):
			return
		
		pygame.draw.circle(surface, self.color, (x, y), Star.ballSize)
		
		for partical in self.particals:
			offsetX = (partical[0] - self.origin[0]) * Star.tileSize
			offsetY = (partical[1] - self.origin[1]) * Star.tileSize
			x = int(16 + (centerPos[0] + offsetX))
			y = int(16 + (centerPos[1] + offsetY))
			surface.set_at((x, y), self.color)
			surface.set_at((x, y + 1), self.color)
			surface.set_at((x + 1, y), self.color)
			surface.set_at((x + 1, y + 1), self.color)
			

