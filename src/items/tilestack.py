
from item import Item

class TileStack(Item):

	def __init__(self, id=0, size=1):
		self.id = id
		self.size = size

	def add(self, amount=1):
		self.size += amount

	def getmaterial(self):
		return self.id
		
	def save(self):
		data = {}
		data['type'] = self.__class__.__name__
		data['material'] = self.id
		data['size'] = self.size
		return data

	def load(self, data):
		if 'material' in data:
			self.id = data['material']
		if 'size' in data:
			self.size = data['size']
