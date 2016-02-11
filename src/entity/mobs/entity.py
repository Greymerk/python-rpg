import pygame
from math import sqrt
from random import randint

from src.ai import AIController
from src.inventory import Inventory
from src.util import Vector2

from time import time
from src.abilities import *

class Entity:

	living = "player"
	dead = "body"
	damage = "damage"
	step = "step.wav"
	ouch = "ouch.wav"
	
	def __init__(self, world):
		self.image = None
		self.gore = None
		self.position = Vector2(0,0)
		self.world = world
		self.group = None
		self.ai = AIController()
		self.abilities = [Attack]
		self.singular = 'unknown'
		self.sight = 5
		self.health = self.maxHealth = 30
		self.inventory = Inventory(self, world.items)
		self.deathTimer = 50
		self.lastDamage = 0
		self.hostile = False
		self.lastAttacker = None
		self.name = None
		self.action = None
		self.observers = []

	def move(self, direction):

		x, y = direction
		oldx, oldy = self.position

		newx = oldx + x
		newy = oldy + y

		if not self.world.isLocationPassable(Vector2(newx, newy)):
			return False

		self.position = Vector2(newx, newy)
		
		return True

	def update(self):
		
		done = True
		
		if self.action is not None:
			done = self.action.update()
			if done:
				self.action = None
				
		return done
			

			
	def draw(self, screen, camPos, images, visible):

		tileSize = 32
		relx = self.position[0] - camPos[0]  
		rely = self.position[1] - camPos[1] 
		position = (((relx + 8)*tileSize), ((rely + 8) * tileSize))

		if visible(self.position):
			screen.blit(self.getImage(images), position)
	
		if self.action is not None:
			self.action.draw(screen, camPos, visible)
	
	def getImage(self, images):
			if self.health == 0:
				return images.get(self.__class__.dead, self.position)
			elif time() - self.lastDamage < 0.2:
				return images.get(self.__class__.damage, self.position)
			else:
				return images.get(self.__class__.living, self.position)

	def save(self):
		data = {}
		data['type'] = self.__class__.__name__
		data['position'] = Vector2.save(self.position)
		data['health'] = self.health
		data['deathTimer'] = self.deathTimer
		data['hostile'] = self.hostile
		data['name'] = self.name
		data['inventory'] = self.inventory.save()
		abi = []
		for ability in self.abilities:
			abi.append(ability.__name__)
		data['abilities'] = abi
		data['ai'] = self.ai.save()
			
		return data

	def load(self, data):
		if 'position' in data.keys():
			self.position = Vector2.load(data['position'])
		if 'health' in data.keys():
			self.health = data['health']
		if 'deathTimer' in data.keys():
			self.deathTimer = data['deathTimer']
		if 'hostile' in data.keys():
			self.hostile = data['hostile']
		if 'name' in data.keys():
			self.name = data['name']
		if 'inventory' in data.keys():
			self.inventory.load(data['inventory'])
		if 'abilities' in data.keys():
			self.abilities = []
			for ability in data['abilities']:
				self.abilities.append(lookup[ability])
		if 'ai' in data.keys():
			self.ai.load(data['ai'])
			
	def turn(self):

		if self.health > 0:
			if self.group is not None:
				if self.distance(self.getLeader().position) > 20:
					self.teleportToLeader()
			self.regen()
			self.ai.act()
		else:			
			self.deathTimer -= 1
		
	def inChunk(self, position):
		
		
		posX = position[0] << 4
		posY = position[1] << 4
		
		mobX = self.position[0]
		mobY = self.position[1]
		
		if mobX < posX:
			return False
		
		if mobX > posX + 16:
			return False
		
		if mobY < posY:
			return False
		
		if mobY > posY + 16:
			return False
		
		return True
		
		
	def canSpawn(self, position):
		
		tile = self.world.getTile(position)
		ground = tile.getGround()
		if not ground.passable:
			return False
		
		if not ground.spawnable:
			return False
		
		return True
	
	def partyCanSee(self, position):
		if self.group is None:
			return self.canSee(position)
			
		return self.group.canSee(position)
	
	def canSee(self, target):
		
		relx = abs(self.position[0] - target[0])
		rely = abs(self.position[1] - target[1])

		if relx > self.sight or rely > self.sight:
			return False
		
		if(relx * relx + rely * rely > self.sight * self.sight):
			return False

		if self.world.obscured(self.position, target):
			return False
		
		return True
		
	def attack(self, location):

		weapon = self.inventory.getWeapon()
		spell = weapon.getAbility()
		self.cast(spell, location)
		
	def inflict(self, attacker, damage):
		
		startHealth = self.health
		
		self.hostile = True
		self.lastAttacker = attacker
		self.health -= damage
		
		if self.health <= 0:
			self.kill()
			
		endHealth = self.health
		
		damageDealt = startHealth - endHealth
		self.world.log.append(attacker.getName() + " hit " + self.getName() + " for " + str(damage) + " damage!")
		
		self.lastDamage = time()
		self.__class__.onDamage(self.world.sounds)
		return damageDealt
	
	def heal(self, healer, amount):
		if not self.isAlive():
			return 0
		
		startHealth = self.health
		self.health += amount
		
		if self.health > self.maxHealth:
			self.health = self.maxHealth
		
		healingDone = self.health - startHealth
		self.world.log.append(healer.getName() + " healed " + self.getName() + " for " + str(healingDone) + "!")
		return healingDone
		
	def kill(self):
		self.world.log.append(self.getName() + ' Died!')
		self.health = 0
		
	def revive(self, reviver):
		
		if self.health != 0:
			return
		
		self.health = 1
		self.world.log.append(self.getName() + ' resurrected by ' + reviver.getName())
		
		
	def distance(self, location):
		relx = abs(self.position[0] - location[0])
		rely = abs(self.position[1] - location[1])
		
		return int(sqrt(relx**2 + rely**2))
	
	def acquireTarget(self):
		
		for e in self.getEnemies():
			if self.canSee(e.position):
				return e
			
	def getAttackable(self):
		
		for e in self.getEnemies():
			if e.isAlive() and self.canSee(e.position) and self.canHit(e.position) :
				return e
			
	def getEnemies(self):
		if self in self.world.friendly:
			return self.world.mobManager.mobs
		else:
			return self.world.friendly
	
	def getFriends(self):
		if self in self.world.friendly:
			return self.world.friendly
		else:
			return self.world.mobManager.mobs
		
	def canHit(self, location, attackRange):
		pos = Vector2(self.position[0], self.position[1])
		pos.center()
		target = Vector2(location)
		target.center()
		pos -= target
		return pos.inRange(attackRange)
			
	def isAlive(self):
		return self.health > 0
	
	def regen(self):
		if self.health >= self.maxHealth:
			return
		
		if randint(0,5) is not 0:
			return
		
		self.health += 1
		
	def setGroup(self, group):
		self.group = group
		
		
	def getLeader(self):
		return self.group.getLeader() if self.group is not None else None
		
	def teleportToLeader(self):
		
		leader = self.getLeader()
		x, y = leader.position
		r = 1
		while(not self.world.isLocationPassable((x, y))):
			x = randint(-r,r) + leader.position[0]
			y = randint(-r,r) + leader.position[1]
			if r is 10:
				print "Failed to find a place to teleport to"
				return
			r += 1
			
		self.position = Vector2(x, y)


	def getName(self):
		if self.name is None:
			return self.__class__.__name__
		else:
			return self.name

	
	def getAction(self):

		if len(self.abilities) == 0:
			return None
		
		for ability in self.abilities:
			
			for e in self.world.getAllEntities():
				
				if not self.canHit(e.position, ability.range):
					continue
				
				if not ability.validTarget(self, e):
					continue
				
				return ability(self, e.position, None) #ability instance
	
	
	def pocket(self, item):
		self.inventory.pocket(item)
	
	def equip(self):
		pass
		
	def notify(self, event):
		for obs in self.observers:
			obs.notify(self, event)
		
	@classmethod
	def onDamage(cls, sounds):
		sounds.get("damage.wav").play()

