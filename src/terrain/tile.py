import terrain


class Tile:

	def __init__(self):
		self.layers = []

	def isPassable(self):
		tileId = self.layers[-1:][0]
		return terrain.lookup[tileId].passable

	def isTransparent(self):
		tileId = self.layers[-1:][0]
		return terrain.lookup[tileId].transparent

	def isBreakable(self):
		tileId = self.layers[-1:][0]
		return terrain.lookup[tileId].breakable

	def build(self, id):
		top = self.layers[-1:][0]
		if(terrain.lookup[top].passable):
			self.layers.append(id)
					
	def destroy(self):
		top = self.layers[-1:][0]
		if(terrain.lookup[top].breakable):
			self.layers.pop()
			if(len(self.layers) == 0):
				self.layers.append(terrain.Grass.id)
		
	def setGround(self, id):
		if(len(self.layers) > 0):
			self.layers = []
		
		self.layers.append(id)
		
	def getGround(self):
		tileId = self.layers[-1:][0]
		
		return terrain.lookup[tileId]
	
	def getName(self):
		tileId = self.layers[-1:][0]
		
		return terrain.lookup[tileId].singular
	

	def save(self):
		data = {}
		data['layers'] = self.layers
		return data


	def load(self, data):
		if 'layers' in data.keys():
			self.layers = data['layers']

