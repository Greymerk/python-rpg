'''
Created on 2013-05-25

@author: brian
'''

from src.util import Vector2

class Pursue(object):

	def __init__(self, actor):
		self.actor = actor
		self.target = None
		
	def condition(self):
		
		if not self.actor.hostile:
			return False
		
		self.target = None
		
		for entity in self.actor.getEnemies():
			if self.actor.group is None:
				canSee = self.actor.canSee
			else:
				canSee = self.actor.group.canSee
		
			if canSee(entity.position) and entity.isAlive():
				
				for ability in self.actor.abilities:
					if ability.inRange(entity.position):
						if not ability.valid(entity):
						   continue
				
				if self.target is None:
					self.target = entity
					continue
				
				if self.actor.distance(entity.position) < self.actor.distance(self.target.position):
					self.target = entity
					
		
		return self.target is not None
	
	def do(self):
		
		x = self.target.position[0] - self.actor.position[0]
		y = self.target.position[1] - self.actor.position[1]
		
		direction = (self.sign(x), 0) if abs(x) > abs(y) else (0, self.sign(y))
		alternative = (self.sign(x), 0) if abs(x) <= abs(y) else (0, self.sign(y))
		
		pos = Vector2(self.actor.position)
		pos += Vector2(direction)
		
		
		if self.actor.world.isLocationPassable(pos):
			self.actor.move(Vector2(direction))
		else:
			self.actor.move(Vector2(alternative))
		
		
	@staticmethod
	def sign(n):
		return -1 if n < 0 else 1 
	
