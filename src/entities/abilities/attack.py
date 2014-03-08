'''
Created on 2013-06-01

@author: brian
'''

from random import randint

class Attack(object):
	
	heal = False  
	
	def __init__(self, caster, location):
		
		weapon = caster.inventory.getWeapon()
		self.range = weapon.range
		self.damage = weapon.damage
		
		self.caster = caster
		self.target = location
		casterName = self.caster.getName()
		self.entityHit = self.caster.world.getEntityFromLocation(self.target)
		if not self.entityHit is None:
			self.entityHit.inflict(self.caster, randint(self.damage[0], self.damage[1]))
		else:
			self.caster.world.log.append(casterName + ' attacked nothing!')
		
		self.done = False
	 
	def update(self):
		return True
		
	def draw(self, surface, position):
		pass
	

	def validTarget(self, actor, target):

		if not target.isAlive():
			return False

		if target in self.actor.getFriends():
			return False

		return True
