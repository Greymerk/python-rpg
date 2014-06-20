'''
Created on 2013-05-27

@author: brian
'''
from pygame.color import THECOLORS

from random import randint
from projectiles import Star

class HealBolt(object):
	
	color = THECOLORS['gold']
	heal = True
	
	def __init__(self, caster, location, item):
		self.range = 6
		self.damage = 2, 6
		self.caster = caster
		self.target = location
		self.done = False
		self.entityHit = self.caster.world.getEntityFromLocation(self.target)
		self.projectile = Star(caster.position, location, item.color, self.entityHit)
		casterName = self.caster.getName()
		if not self.entityHit is None:
			targetName = self.entityHit.getName()
			self.caster.world.log.append(casterName + ' cast Heal at ' + targetName)
		else:
			self.caster.world.log.append(casterName + ' cast Heal at nothing!')
	 
	def update(self):
		self.projectile.update()
		if self.projectile.done:
			if not self.entityHit is None:
				self.entityHit.heal(self.caster, randint(self.damage[0], self.damage[1]))
			self.done = True
			return True
		return False
		
	def draw(self, surface, position):
		if not self.done:
			self.projectile.draw(surface, position)
	
	@classmethod
	def validTarget(cls, actor, target):

		if not target in actor.getFriends():
			return False

		if not target.isAlive():
			return False

		if target.health / target.maxHealth > 0.8:
			return False

		if not actor.canSee(target.position):
			return False

		return True
   
