import string
import os
import chunkgen
import pickle
from tile import Tile
import json
import terrain

class Chunk:
	
	def __init__(self, pos, seed, mobManager, mapCache):
		self.seed = seed
		self.pos = pos
		self.mobs = mobManager
		self.chunkSize = 16
		self.tiles = []
		
		self.saveDir = 'save/world/'
		if not os.path.isdir(self.saveDir):
			os.mkdir(self.saveDir)
		
		self.load()
		self.mapCache = mapCache
		self.mapCache.genMap(self)
		
		
	def getPos(self):
		return self.pos


	def save(self):

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

	def unload(self):
		self.save()
		self.mapCache.genMap(self)
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
		
	def setTile(self, (x, y), id):
		tile = self.tiles[y % 16 * self.chunkSize + x % 16]
		tile.build(id)
		self.mapCache.genMap(self)
		self.save()

