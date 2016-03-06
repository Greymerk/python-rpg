'''
Created on 2013-05-27

@author: brian
'''
from pygame.color import THECOLORS

from random import randint
from projectiles import Star

class HealBolt(object):
	
	range = 5
	damage = 2, 5
	heal = True
	name = "Heal Bolt"
	icon = "healbolt"
	cooldown = 0
	
	def __init__(self, caster, location, item):
		self.item = item
		self.caster = caster
		self.target = location
		self.done = False
		self.color = THECOLORS['yellow']
		self.entityHit = self.caster.world.getEntityFromLocation(self.target)
		self.projectile = Star(caster.position, self.target, self.color, self.fire)
		casterName = self.caster.getName()
		if not self.entityHit is None:
			targetName = self.entityHit.getName()
			self.caster.world.log.append(casterName + ' cast Heal at ' + targetName)
		else:
			self.caster.world.log.append(casterName + ' cast Heal at nothing!')
	 
	def update(self):
		pos = None
		if self.entityHit is not None:
			pos = self.entityHit.position
		self.projectile.update(pos)
		if self.projectile.done:
			if not self.entityHit is None:
				self.entityHit.heal(self.caster, randint(self.damage[0], self.damage[1]))
			self.done = True
			return True
		return False
		
	def draw(self, surface, position, visible):
		if not self.done:
			self.projectile.draw(surface, position, visible)
	
	@classmethod
	def validTarget(cls, actor, target):

		if not target in actor.getFriends():
			return False

		if not target.isAlive():
			return False

		if target.health / target.maxHealth > 0.8:
			return False

		if not actor.partyCanSee(target.position):
			return False

		return True
		
	
	def fire(self):
		self.caster.world.sounds.get("spell-healing.wav").play()

   
