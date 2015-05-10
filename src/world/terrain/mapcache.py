import os
import pygame

from simplex import Simplex

class MapCache(object):
	
	def __init__(self, chunkManager, seed):
		
		self.chunkManager = chunkManager
		self.mapDir = 'save/map/'
		self.noise = Simplex(seed)
		
		if not os.path.isdir(self.mapDir):
			os.mkdir(self.mapDir)
		
		self.basePath = os.path.dirname(__file__)
		self.cache = {}
		
	def load(self, name):
		path = self.mapDir + name + '.png'
		
		if not os.path.isfile(path):
			return
			
		f = open(path, 'r')
		self.cache[name] = pygame.image.load(path).convert_alpha()
		return self.cache[name]
		
	def get(self, x, y):
		name = str(x) + '_' + str(y)
		
		if(name in self.cache):
			return self.cache[name]
		
		if(self.chunkManager.isLoaded(x, y)):
			chunk = chunkManager.getChunk(x << 4, y << 4)
			self.genMap(chunk)
		
		return self.load(name)
		
	def genMap(self, chunk):
		img = pygame.Surface((16, 16))
		
		for y in range(16):
			for x in range(16):
				t = chunk.getTile(x, y)
				groundColor = t.getGround().color()
				shadow = self.getShadow(chunk.pos[0] * 16 + x, chunk.pos[1] * 16 + y)
				color = self.blend(shadow, groundColor)
				
				img.set_at((x, y), color)
				
				
		img = pygame.transform.scale2x(img)
		x, y = chunk.pos
		name = str(x) + '_' + str(y)
		path = self.mapDir + name + '.png'
		pygame.image.save(img, path)
		self.cache[name] = img
		
	def getShadow(self, x, y):
		octaves = 6
		persistence = 0.75
		scale = 0.004
		c1 = self.noise.octave_noise_2d(octaves, persistence, scale, x, y)
		if c1 < 0.05:
			return 0.5
		c1 += 0.4
		c2 = self.noise.octave_noise_2d(octaves, persistence, scale, x - 2, y - 2)
		c1 = (c1 - c2)
		c1 *= 1.2
		
		if c1 > 1:
			c1 = 1
		if c1 < 0:
			c1 = 0
		
		return c1
		
	def blend(self, percent, map):
		
		r = int(map[0] * percent)
		g = int(map[1] * percent)
		b = int(map[2] * percent)

		return r, g, b
