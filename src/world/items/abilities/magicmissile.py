'''
Created on 2013-06-04

@author: brian
'''

from random import randint
from projectiles import Star

class MagicMissile(object):
	
	range = 5
	damage = 2, 5
	heal = False
	
	def __init__(self, caster, location, item):
		self.item = item
		self.range = item.range
		self.caster = caster
		self.target = location
		self.range = self.__class__.range
		self.damage = self.__class__.damage
		casterName = self.caster.getName()
		self.entityHit = self.caster.world.getEntityFromLocation(self.target)
		if not self.entityHit is None:
			targetName = self.entityHit.getName()
			self.caster.world.log.append(casterName + ' cast ' + self.__class__.__name__ + ' at ' + targetName)
		else:
			self.caster.world.log.append(casterName + ' cast ' + self.__class__.__name__ + ' at nothing!')
		
		self.projectile = Star(caster.position, location, item.color, self.fire, self.impact)
		self.done = False
	 
	def update(self):
		self.projectile.update()
		if self.projectile.done:
			if not self.entityHit is None:
				self.entityHit.inflict(self.caster, randint(self.item.damage[0], self.item.damage[1]))
			self.done = True
			return True
		
		return False
		
	def draw(self, surface, position, visible):
		if not self.done:
			self.projectile.draw(surface, position, visible)
	
	@classmethod
	def validTarget(cls, actor, target):

		if not target in actor.getEnemies():
			return False

		if not target.isAlive():
			return False

		if not actor.partyCanSee(target.position):
			return False

		return True

	def fire(self):
		self.caster.world.sounds.get("magic-missile.wav").play()
	
	def impact(self):
		self.caster.world.sounds.get("fireball-impact.wav").play()
	
class FireBall(MagicMissile):
	
	def fire(self):
		self.caster.world.sounds.get("fireball.wav").play()
	
	def impact(self):
		self.caster.world.sounds.get("fireball-impact.wav").play()