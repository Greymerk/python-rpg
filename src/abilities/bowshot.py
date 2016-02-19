'''
Created on 2013-05-28

@author: brian
'''

from pygame.color import THECOLORS
from projectiles import Arrow
from random import randint

class BowShot(object):
	
	range = 7
	damage = 2, 5
	heal = False
	name = "Shoot"
	icon = "arrow"
	cooldown = 0
		
	def __init__(self, caster, location, item):
		self.caster = caster
		self.target = location
		self.item = item
		self.color = THECOLORS['chocolate']
		self.range = self.__class__.range
		self.damage = self.__class__.damage
		
		casterName = self.caster.getName()
		
		self.entityHit = self.caster.world.getEntityFromLocation(self.target)
		if not self.entityHit is None:
			targetName = self.entityHit.getName()
			self.caster.world.log.append(casterName + ' shot ' + targetName + ' with a ' + self.__class__.__name__)
		else:
			self.caster.world.log.append(casterName + ' shot nothing!')

		self.projectile = Arrow(caster.position, location, self.color, self.fire, self.impact)
		self.done = False
		
	def update(self):
		self.projectile.update()
		if self.projectile.done:
			if not self.entityHit is None:
				self.entityHit.inflict(self.caster, randint(self.damage[0], self.damage[1]))
			self.done = True
			return True
		
		return False
		
	def draw(self, surface, position, visible):
		if not self.done:
			self.projectile.draw(surface, position, visible)
			
	@classmethod
	def validTarget(cls, actor, target):
	
		if not target.isAlive():
			return False
		
		if target in actor.getFriends():
			return False
		
		return actor.partyCanSee(target.position)
		
	
	def fire(self):
		self.caster.world.sounds.get("pew.wav").play()
	
	def impact(self):
		self.caster.world.sounds.get("hit.wav").play()