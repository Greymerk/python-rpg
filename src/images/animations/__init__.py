from random import Random
from random import randint

class Animation(object):

	def __init__(self):
		self.images = []
		
	def get(self, pos):
		if randint(0, 2) == 1:
			return self.images[0]
		
		return self.images[1]
		
	def add(self, images):
		for image in images:
			if image[-4:] == '.png':
				self.images.append(image)


class Variety(object):
	def __init__(self):
		self.images = []
		
	def get(self, pos):
		n = int(pos[0]) | int(pos[1])
		i = n % len(self.images) 
		return self.images[i]
		
	def add(self, images):
		for image in images:
			if image[-4:] == '.png':
				self.images.append(image)