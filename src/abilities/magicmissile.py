'''
Created on 2013-06-04

@author: brian
'''

from random import randint
from projectiles import Star
from pygame.color import THECOLORS
from src.util import Vector2

class MagicMissile(object):
	
	range = 5
	damage = 2, 5
	heal = False
	name = "Magic Missile"
	color = THECOLORS['lightcyan']
	icon = "magicbolt"
	cooldown = 0
	
	def __init__(self, caster, location, item):
		self.item = item
		self.caster = caster
		self.target = location
		self.range = self.__class__.range
		self.damage = self.__class__.damage
		self.color = self.__class__.color
		casterName = self.caster.getName()
		self.entityHit = self.caster.world.getEntityFromLocation(self.target)
		if not self.entityHit is None:
			targetName = self.entityHit.getName()
			self.caster.world.log.append(casterName + ' cast ' + self.__class__.__name__ + ' at ' + targetName)
		else:
			self.caster.world.log.append(casterName + ' cast ' + self.__class__.__name__ + ' at nothing!')
		
		self.projectile = Star(caster.position, location, self.color, self.fire, self.impact)
		self.done = False
	 
	def update(self):
		pos = None
		if self.entityHit is not None:
			pos = Vector2(self.entityHit.position)
		self.projectile.update(pos)
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
	
	range = 6
	damage = 3, 8
	heal = False
	color = THECOLORS['orange']
	name = "Fireball"
	icon = "firebolt"
	
	def fire(self):
		self.caster.world.sounds.get("fireball.wav").play()
	
	def impact(self):
		self.caster.world.sounds.get("fireball-impact.wav").play()
		
