'''
Created on 2013-05-26

@author: brian
'''

from mobs import Bard
from mobs import Fighter
from mobs import Mage
from mobs import Priest


class Party(object):
	
	def __init__(self, world):

		self.world = world
		self.members = []
		self.leader = 0   
		self.visibilityCache = {}
		self.visibilityTurn = world.time
		
	def add(self, entity):
		self.members.append(entity)
		entity.setGroup(self)
		
	def save(self):
		
		data = {}
		
		members = []
		
		for e in self.members:
			members.append(e.save())
			
		data['members'] = members
		data['leader'] = self.leader
		
		return data
		
	def setLeader(self, index):
			   
		if not index in range(len(self.members)):
			return
		
		self.members[self.leader].ai.active = True	
		self.leader = index
		self.members[self.leader].ai.active = False
		
		return self.getLeader()
		
	def load(self, data):
		
		if data is None:
			
			member = Fighter(self.world)
			member.equip()
			member.name = "Steve"
			self.members.append(member)
			member.setGroup(self)
			
			member = Fighter(self.world)
			member.equip()
			member.name = "Gregg"
			self.members.append(member)
			member.setGroup(self)
			
			member = Mage(self.world)
			member.equip()
			member.name = "Johne"
			self.members.append(member)
			member.setGroup(self)
			
			member = Priest(self.world)
			member.equip()
			member.name = "Maya"
			self.members.append(member)
			member.setGroup(self)
			
			member = Priest(self.world)
			member.equip()
			member.name = "Alice"
			self.members.append(member)
			member.setGroup(self)

			member = Bard(self.world)
			member.equip()
			member.name = "Kat"
			self.members.append(member)
			member.setGroup(self)
			member.position = self.world.getSpawnLocation()
			
			self.setLeader(0)
			
			for e in self.members:
				e.teleportToLeader()
			
			return
		
		for e in data['members']:
			member = self.world.mobManager.loadEntity(e)
			self.members.append(member)
			member.setGroup(self)
			
		self.leader = data['leader']
			
	def getLeader(self):
		return self.members[self.leader]
	

	def canSee(self, position):

		pos = (position[0], position[1])

		if self.visibilityTurn is not self.world.time:
			self.visibilityTurn = self.world.time
			self.visibilityCache = {}

		if pos in self.visibilityCache:
			return self.visibilityCache[pos]

		for e in self.members:
			if e.canSee(position):
				self.visibilityCache[pos] = True
				return True

		self.visibilityCache[pos] = False
		return False
		
	def resetLeader(self):
		for i in range(len(self.members)):
			if self.members[i].isAlive():
				return self.setLeader(i)

	def __iter__(self):
		return iter(self.members)
