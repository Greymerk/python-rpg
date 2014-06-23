import pygame
from ai import AIController
from math import sqrt
from random import randint

from inventory import Inventory



class Entity:

	living = "player.png"
	dead = "body.png"
	step = "step.wav"
	ouch = "ouch.wav"
	
	def __init__(self, world):
		self.image = None
		self.gore = None
		self.position = (0,0)
		self.world = world
		self.group = None
		self.ai = AIController()
		self.singular = 'unknown'
		self.sight = 5
		self.health = self.maxHealth = 30
		self.inventory = Inventory(self, world.items)
		self.deathTimer = 50
		self.hostile = False
		self.lastAttacker = None
		self.name = None
		self.action = None

	def move(self, direction):

		x, y = direction
		oldx, oldy = self.position

		newx = oldx + x
		newy = oldy + y

		if not self.world.isLocationPassable((newx, newy)):
			return False

		self.position = (newx, newy)
		
		return True

	def update(self):
		
		done = True
		
		if self.action is not None:
			done = self.action.update()
			if done:
				self.action = None
				
		return done
			

			
	def draw(self, screen, posx, posy, images):
		tileSize = 32
		position = (((posx + 8)*tileSize), ((posy + 8) * tileSize))
		if self.health == 0:
			screen.blit(images.get(self.__class__.dead), position)
			return
		screen.blit(images.get(self.__class__.living), position)
		if self.action is not None:
			self.action.draw(screen, position)
		

	def save(self):
		data = {}
		data['type'] = self.__class__.__name__
		data['position'] = self.position
		data['health'] = self.health
		data['deathTimer'] = self.deathTimer
		data['hostile'] = self.hostile
		if self.lastAttacker is not None:
			data['lastAttacker'] = self.lastAttacker.position
		data['name'] = self.name
		data['inventory'] = self.inventory.save()
		data['ai'] = self.ai.save()
			
		return data

	def load(self, data):
		if 'position' in data.keys():
			self.position = data['position']
		if 'health' in data.keys():
			self.health = data['health']
		if 'deathTimer' in data.keys():
			self.deathTimer = data['deathTimer']
		if 'hostile' in data.keys():
			self.hostile = data['hostile']
		if 'lastAttacker' in data.keys():
			self.lastAttacker = self.world.getEntityFromLocation(data['lastAttacker'])
		if 'name' in data.keys():
			self.name = data['name']
		if 'inventory' in data.keys():
			self.inventory.load(data['inventory'])
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
	
	def canSee(self, position):
		
		relx = abs(self.position[0] - position[0])
		rely = abs(self.position[1] - position[1])
		
		distance = sqrt(relx**2 + rely**2)
		
		if(distance > self.sight):
			return False

		if self.world.obscured(self.position, position):
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
		
		distance = sqrt(float(((location[0] - self.position[0])**2 + (location[1] - self.position[1])**2)))
		return distance <= sqrt(2*((attackRange)**2)) 
			
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
			
		self.position = (x, y)


	def getName(self):
		if self.name is None:
			return self.__class__.__name__
		else:
			return self.name

	def getSpellList(self):
				
		if not self.inventory.offhand.__class__ is Spellbook:
		    return []
		
		return self.inventory.offhand.spellList
	
	def pocket(self, item):
		self.inventory.pocket(item)
	
	def equip(self):
		pass

