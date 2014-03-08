import string
import os
import chunkgen
import pickle
from tile import Tile
import json

class Chunk:
	
	def __init__(self, pos, seed, mobManager):
		self.seed = seed
		self.pos = pos
		self.mobs = mobManager
		self.chunkSize = 16
		self.tiles = []
		
		self.saveDir = 'save/world/'
		if not os.path.isdir(self.saveDir):
			os.mkdir(self.saveDir)
			
		self.mapDir = 'save/map/'
		if not os.path.isdir(self.mapDir):
			os.mkdir(self.mapDir)

		self.load()

	def getPos(self):
		return self.pos


	def save(self):

		self.saveMap()

		chunkData = {}
		tileList = []
		for tile in self.tiles:
			tileList.append(tile.save())
		chunkData['tiles'] = tileList
		chunkData['mobs'] = self.mobs.save(self.pos)

		x, y = self.pos
		fileName = self.saveDir + str(x) + '_' + str(y)
		f = open(fileName, 'w')
		p = pickle.Pickler(f)
		p.dump(chunkData)
		f.close()
		
	def getMap(self):
		intMap = [0]*256
		
		for i in range(256):
			intMap[i] = self.tiles[i].getGround().id
	
		return intMap
		
	def saveMap(self):
		intMap = self.getMap()
		jsonMap = json.dumps(intMap)
		x, y = self.pos
		fileName = self.mapDir + str(x) + '_' + str(y)
		f = open(fileName, 'w')
		f.write(jsonMap)
		f.close()
		
	def unload(self):
		self.save()
		self.mobs.unload(self.pos)
			

	def load(self):
		x, y = self.pos
		fileName = self.saveDir + str(x) + '_' + str(y)
		if not os.path.isfile(fileName):
			self.generate()
			self.save()
			return
		
		f = open(fileName, 'r')
		p = pickle.Unpickler(f)
		chunkData = p.load()
		f.close()
		
		tileList = chunkData['tiles']
		for data in tileList:
			tileToLoad = Tile()
			tileToLoad.load(data)
			self.tiles.append(tileToLoad)
			
		self.mobs.load(chunkData['mobs'])


	def generate(self):
		self.tiles = chunkgen.ChunkGen(self.seed, self.pos).generate()

		
	def getTile(self, x, y):
		return self.tiles[y * self.chunkSize + x]
	
	@classmethod
	def loadMap(cls, x, y):
	
		fileName = 'save/map/' + str(x) + '_' + str(y)
		
		if not os.path.exists(fileName):
			return
		
		f = open(fileName, 'r')
		jsonMap = f.read()
		f.close()
		
		intMap = json.loads(jsonMap)
		
		return intMap

