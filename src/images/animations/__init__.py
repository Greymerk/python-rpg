from random import Random
from random import randint

class Animation(object):

	def __init__(self):
		self.images = []
		
	def get(self, (x, y)):
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
		
	def get(self, (x, y)):
		rand = Random()
		rand.seed(x | y)
		return rand.choice(self.images)
		
	def add(self, images):
		for image in images:
			if image[-4:] == '.png':
				self.images.append(image)