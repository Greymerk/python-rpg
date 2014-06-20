'''
Created on 2013-05-26

@author: brian
'''

from bard import Bard
from mage import Mage
from fighter import Fighter

class Party(object):
	
	def __init__(self, world):

		self.world = world
		self.members = []
		self.leader = 0   
		
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
		
	def load(self, data):
		
		if data is None:
			member = Bard(self.world)
			member.equip()
			member.name = "Jade"
			self.members.append(member)
			member.setGroup(self)
			
			member = Mage(self.world)
			member.equip()
			member.name = "Ice"
			self.members.append(member)
			member.setGroup(self)
			
			member = Mage(self.world)
			member.equip()
			member.name = "Fire"
			self.members.append(member)
			member.setGroup(self)
			
			member = Fighter(self.world)
			member.equip()
			member.name = "Gregg"
			self.members.append(member)
			member.setGroup(self)
			
			member = Fighter(self.world)
			member.equip()
			member.name = "Steve"
			self.members.append(member)
			member.setGroup(self)
			
			self.setLeader(0)
			return
		
		for e in data['members']:
			member = self.world.mobManager.loadEntity(e)
			self.members.append(member)
			member.setGroup(self)
			
		self.leader = data['leader']
			
	def getLeader(self):
		return self.members[self.leader]
	

	def canSee(self, position):
		for e in self.members:
				if e.canSee(position):
					return True

		return False
		
