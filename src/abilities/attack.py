'''
Created on 2013-06-01

@author: brian
'''

from random import randint

class Attack(object):
	
	range = 1
	damage = 2, 5
	heal = False 
	name = "Attack"
	icon = "sword.png"
	
	def __init__(self, caster, location, item):
		
		self.caster = caster
		self.target = location
		self.item = item
		self.range = self.__class__.range
		self.damage = self.__class__.damage
		
		casterName = self.caster.getName()
		self.entityHit = self.caster.world.getEntityFromLocation(self.target)
		if not self.entityHit is None:
			self.entityHit.inflict(self.caster, randint(self.damage[0], self.damage[1]))
		else:
			self.caster.world.log.append(casterName + ' attacked nothing!')
		
		self.done = False
	 
	def update(self):
		return True
		
	def draw(self, surface, position, visible):
		pass
	
	@classmethod
	def validTarget(cls, actor, target):

		if not target.isAlive():
			return False

		if target in actor.getFriends():
			return False

		return True
