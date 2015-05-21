
from weapon import Weapon
from tilestack import TileStack

class ItemFactory(object):
	
	itemList = {}
	itemList["Weapon"] = Weapon
	itemList["TileStack"] = TileStack
	
	def __init__(self, terrain):
		self.weapons = Weapon
		self.terrain = terrain
	
	def load(self, data):
		itemType = data['type']
		
		o = self.itemList[itemType]()
		o.load(data)
		return o

	def getStack(self, material, size=1):
		return TileStack(material, size)