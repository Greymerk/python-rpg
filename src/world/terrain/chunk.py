import string
import os
import chunkgen
from tile import Tile
import json
import terrain
import math


class Chunk:

	size = 16
	
	def __init__(self, pos, seed, mobManager, mapCache):
		self.seed = seed
		self.pos = pos
		self.mobs = mobManager
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
		with open(fileName, 'w') as f:
			json.dump(chunkData, f, sort_keys=True, indent=4)
		

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
		
		with open(fileName, 'r') as f:
			chunkData = json.load(f)
		
		tileList = chunkData['tiles']
		for data in tileList:
			tileToLoad = Tile()
			tileToLoad.load(data)
			self.tiles.append(tileToLoad)
			
		self.mobs.load(chunkData['mobs'])

	def generate(self):
		self.tiles = chunkgen.ChunkGen(self.seed, self.pos).generate()
		
	def getTile(self, x, y):
		return self.tiles[y * Chunk.size + x]
		
	def setTile(self, (x, y), id):
		tile = self.tiles[y % 16 * Chunk.size + x % 16]
		tile.build(id)
		self.mapCache.genMap(self)
		self.save()

	def getDistToChunk(self, pos):
		x, y = pos
		return math.sqrt((self.pos[0] - x)**2 + (self.pos[1] - y)**2)	
