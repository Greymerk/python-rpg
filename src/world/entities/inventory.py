'''
Created on 2013-06-01

@author: brian
'''

class Inventory(object):
	
	def __init__(self, owner, itemFactory):
		self.bag = [None] * 8
		self.bar = [None] * 8
		self.owner = owner
		self.itemFactory = itemFactory
		
		
	def getAction(self):

		if len(self.bar) == 0:
			return None
		
		for item in self.bar:
			
			if item is None:
				continue
			
			for e in self.owner.world.getAllEntities():
				
				if not item.ability.validTarget(self.owner, e):
					continue
				
				if not self.owner.canHit(e.position, item.range):
					continue

				return item.ability(self.owner, e.position, item) #ability instance
	
	def load(self, data):
	
		if 'bag' in data.keys():
			bag = data['bag']
			for i in range(len(bag)):
				if bag[i] is None:
					self.bag[i] = None
				else:
					self.bag[i] = self.itemFactory.load(bag[i])
	
		if 'bar' in data.keys():
			bar = data['bar']
			for i in range(len(bar)):
				if bar[i] is None:
					self.bar[i] = None
				else:
					self.bar[i] = self.itemFactory.load(bar[i])
		
		
	def pocket(self, id):
	
		for i in range(len(self.bag)):
			if self.bag[i] is None:
				self.bag[i] = self.itemFactory.getStack(id)
				return
			if self.bag[i].id is id:
				self.bag[i].size += 1
				return

		
	def save(self):
		data = {}
		
		bag = []
		for i in self.bag:
			if i is None:
				bag.append(None)
			else:
				bag.append(i.save())
		data['bag'] = bag
		
		bar = []
		for i in self.bar:
			if i is None:
				bar.append(None)
			else:
				bar.append(i.save())
		data['bar'] = bar
		
		return data
