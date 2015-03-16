import terrain

class Tile:

	def __init__(self):
		self.layers = []

	def getGround(self):
		tileId = self.layers[-1:][0]
		return terrain.lookup[tileId]
		
	def setGround(self, id):
		if(len(self.layers) > 0):
			self.layers = []
		
		self.layers.append(id)
		
	def isPassable(self):
		return self.getGround().passable

	def isTransparent(self):
		return self.getGround().transparent

	def isBreakable(self):
		return self.getGround().breakable

	def getName(self):
		return self.getGround().singular
		
	def canBuild(self):
		top = self.layers[-1:][0]
		return terrain.lookup[top].passable
	
	def build(self, id):
		self.layers.append(id)
	
	def destroy(self):
		if(self.isBreakable()):
			id = self.layers.pop()
			if(len(self.layers) == 0):
				self.layers.append(terrain.Grass.id)
			return terrain.lookup[id].drop()
		
	def save(self):
		data = {}
		data['layers'] = self.layers
		return data

	def load(self, data):
		if 'layers' in data.keys():
			self.layers = data['layers']

