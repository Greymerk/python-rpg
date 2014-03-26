'''
Created on 2013-06-04

@author: brian
'''

from pygame.color import THECOLORS

from items.projectiles import Star
from random import randint

class MagicMissile(object):
	
	color = THECOLORS['cyan']
	damage = 1, 5
	heal = False
	
	def __init__(self, caster, location, item):
		self.range = item.range
		self.caster = caster
		self.target = location
		casterName = self.caster.getName()
		self.entityHit = self.caster.world.getEntityFromLocation(self.target)
		if not self.entityHit is None:
			targetName = self.entityHit.getName()
			self.caster.world.log.append(casterName + ' cast ' + self.__class__.__name__ + ' at ' + targetName)
		else:
			self.caster.world.log.append(casterName + ' cast ' + self.__class__.__name__ + ' at nothing!')
		
		self.projectile = Star(caster.position, location, self.__class__.color, self.entityHit)
		self.done = False
	 
	def update(self):
		self.projectile.update()
		if self.projectile.done:
			if not self.entityHit is None:
				self.entityHit.inflict(self.caster, randint(self.__class__.damage[0], self.__class__.damage[1]))
			self.done = True
			return True
		
		return False
		
	def draw(self, surface, position):
		if not self.done:
			self.projectile.draw(surface, position)
	
	@classmethod
	def validTarget(cls, actor, target):

		if not target in actor.getEnemies():
			return False

		if not target.isAlive():
			return False

		if not actor.canSee(target.position):
			return False

		return True

class Fireball(MagicMissile):
    
    color = THECOLORS['orangered']
    damage = 3, 7
