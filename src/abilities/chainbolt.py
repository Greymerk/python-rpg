from random import randint
from projectiles import Star

class ChainBolt(object):
	
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
		self.bolts = 3
		if not self.entityHit is None:
			targetName = self.entityHit.getName()
			self.caster.world.log.append(casterName + ' cast ' + self.__class__.__name__ + ' at ' + targetName)
		else:
			self.caster.world.log.append(casterName + ' cast ' + self.__class__.__name__ + ' at nothing!')
		
		self.projectile = Star(caster.position, location, self.item.color, self.fire, self.impact)
		self.done = False
	 
	def update(self):
	
		self.projectile.update()
		if self.projectile.done:
			if self.entityHit is not None:
				self.entityHit.inflict(self.caster, randint(self.item.damage[0], self.item.damage[1]))
			if self.bolts <= 0 or self.entityHit is None:
				self.done = True
				return True
			else:
				self.bolts -= 1
				nextTarget = self.getAllyInRange(self.entityHit, self.range)
				if nextTarget is None:
					self.done = True
					return True
				self.projectile = Star(self.entityHit.position, nextTarget.position, self.item.color, self.fire, self.impact)
				self.entityHit = nextTarget
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
		
	def getAllyInRange(self, entity, radius):
		
		for e in entity.getFriends():
			if e is entity:
				continue
			if not e.isAlive():
				continue
			if e.distance(entity.position) < radius:
				return e