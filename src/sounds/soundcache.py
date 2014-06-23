
import os
import pygame

class SoundCache(object):
	
	def __init__(self, soundDir="default"):
		
		self.basePath = os.path.dirname(__file__)
		self.soundDir = soundDir
		self.cache = {}
		
	def get(self, name):

		if name in self.cache:
			return self.cache[name]
		else:
			path = os.path.join(self.basePath, self.soundDir, name)
			self.cache[name] = pygame.mixer.Sound(path)
			self.cache[name].set_volume(0.5)
			return self.cache[name]
