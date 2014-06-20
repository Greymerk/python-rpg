
import os
import pygame



class ImageCache(object):
	
	def __init__(self, textureDir="u5"):
		
		self.basePath = os.path.dirname(__file__)
		self.textureDir = textureDir
		self.cache = {}
		
	def get(self, name):

		if name in self.cache:
			return self.cache[name]
		else:
			path = os.path.join(self.basePath, self.textureDir, name)
			self.cache[name] = pygame.image.load(path).convert_alpha()
			return self.cache[name]
