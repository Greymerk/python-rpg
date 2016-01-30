from random import randint
from projectiles import Star
from math import sqrt
from pygame.color import THECOLORS

class Explosion(object):
	
	range = 6
	radius = 4
	damage = 2, 5
	heal = False
	name = "Explosion"
	icon = "firebolt"
	
	def __init__(self, caster, location, item):
		self.item = item
		self.range = MagicMissile.range
		self.caster = caster
		self.target = location
		self.range = self.__class__.range
		self.damage = self.__class__.damage
		self.color = THECOLORS['orange']
		casterName = self.caster.getName()
		self.entityHit = self.caster.world.getEntityFromLocation(self.target)
		if not self.entityHit is None:
			targetName = self.entityHit.getName()
			self.caster.world.log.append(casterName + ' cast ' + self.__class__.__name__ + ' at ' + targetName)
		else:
			self.caster.world.log.append(casterName + ' cast ' + self.__class__.__name__ + ' at nothing!')
		
		self.projectile = Star(caster.position, location, self.item.color, self.fire, self.impact)
		self.explosion = []
		self.done = False
	 
	def update(self):
	
		if not self.projectile.done:
			self.projectile.update()
			
			if self.projectile.done:
				#explosion start
				targets = Explosion.getNearbyTiles(self.target, Explosion.radius)
				if not targets:
					self.done = True
					return True
				for pos in targets:
					newStar = Star(self.target, pos, self.color, None, None)
					self.explosion.append(newStar)
			return False

		if not self.explosion:
			return True
		
		done = True
		for star in self.explosion:
			if star.done:
				continue
			star.update()
			if star.done:
				e = self.caster.world.getEntityFromLocation(star.end)
				if e is not None:
					e.inflict(self.caster, randint(self.damage[0], self.damage[1]))
			else:
				done = False
				
		if done:
			self.done = True
			
		return done
		
	def draw(self, surface, position, visible):
		if not self.done:
			if not self.projectile.done:
				self.projectile.draw(surface, position, visible)
			if self.explosion:
				for star in self.explosion:
					star.draw(surface, position, visible)
		
	@staticmethod
	def getNearbyTiles(pos, r):
		targets = []
		xP = pos[0] - (r - 1)
		yP = pos[1] - (r - 1)
		for x in xrange(r * 2 - 1):
			for y in xrange(r * 2 - 1):
				toHit = (xP + x, yP + y)
				if Explosion.canHit(pos, toHit, r):
					targets.append(toHit)
		return targets
	
	@staticmethod
	def canHit(origin, position, r):
		
		relx = abs(float(origin[0]) - float(position[0]))
		rely = abs(float(origin[1]) - float(position[1]))
		
		distance = sqrt(relx**2 + rely**2)
		
		if(distance <= r - 1):
			return True
			
		return False
		
	@classmethod
	def validTarget(cls, actor, target):

		if not target in actor.getEnemies():
			return False
	
		if not target.isAlive():
			return False
	
		if not actor.partyCanSee(target.position):
			return False
	
		nearbyTiles = cls.getNearbyTiles(target.position, Explosion.radius)
		for pos in nearbyTiles:
			e = actor.world.getEntityFromLocation(pos)
			if e is None:
				continue
			if not target.isAlive():
				continue
			if e is actor:
				return False
			if e in actor.getFriends():
				return False
	
		return True

	def fire(self):
		self.caster.world.sounds.get("fireball.wav").play()
	
	def impact(self):
		self.caster.world.sounds.get("explosion.wav").play()
		
	def getAllyInRange(self, entity, radius):
		
		for e in entity.getFriends():
			if e is entity:
				continue
			if not e.isAlive():
				continue
			if e.distance(entity.position) < radius:
				return e