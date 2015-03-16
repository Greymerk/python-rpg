
import os
import pygame
import imp

from animations import Animation
from animations import Variety

class ImageCache(object):
	
	def __init__(self, textureDir="u5"):
		
		self.basePath = os.path.dirname(__file__)
		self.textureDir = textureDir
		self.cache = {}
		self.animations = {}
		
	def get(self, name, pos = None):
		anim = self.getAnimation(name)
		
		if anim is None:
			return self.getImage(name + '.png')
		
		return self.getImage(name + '/' + anim.get(pos))
		
	def getAnimation(self, name):
		if not name in self.animations:
			path = os.path.join(self.basePath, self.textureDir, name)
			if os.path.isdir(path):
				anim = Variety()
				anim.add(os.listdir(path))
				self.animations[name] = anim
			else:
				self.animations[name] = None
		return self.animations[name]
		
	def getImage(self, name):
			if name in self.cache:
				return self.cache[name]
			else:
				return self.addImage(name)
		
	def addImage(self, name):
		path = os.path.join(self.basePath, self.textureDir, name)
		self.cache[name] = pygame.image.load(path).convert_alpha()
		return self.cache[name]