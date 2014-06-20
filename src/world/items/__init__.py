
from weapon import Weapon

class ItemFactory(object):
	
	itemList = {}
	itemList["Weapon"] = Weapon
	
	def __init__(self):
		self.weapons = Weapon
	
	def load(self, data):
		itemType = data['type']

		o = self.itemList[itemType]()
		o.load(data)
		return o