import math


class Vector2(object):

	def __init__(self, x, y=None):
			if(y is None):
				self.x = float(x[0])
				self.y = float(x[1])
			else:
				self.x = float(x)
				self.y = float(y)

	def dist(self, other):
		relx = abs(self.x - other[0])
		rely = abs(self.y - other[1])
		return math.sqrt(relx**2 + rely**2)

	def inRange(self, range):
		return self.x * self.x + self.y * self.y <= range * range + 1
		
	def __add__(self, other):
		self.x += other[0]
		self.y += other[1]
		return self
		
	def __sub__(self, other):
		self.x -= other[0]
		self.y -= other[1]
		return self

	def __mul__(self, other):
		self.x *= other[0]
		self.y *= other[1]
		return self
		
	def __eq__(self, other):
		if self.x != other[0]:
			return False

		if self.y != other[1]:
			return False

		return True

	def center(self):
		self.x = math.floor(self.x) + 0.5
		self.y = math.floor(self.y) + 0.5
		
	def save(self):
		return Vector2.save(self)

	def __getitem__(self, key):
		return (self.x, self.y)[key]

	def __str__(self):
			return str(self.x) + ' ' + str(self.y)

	@staticmethod
	def save(vec):
		data = {}
		data["x"] = vec[0]
		data["y"] = vec[1]
		return data
			
	@staticmethod
	def load(data):
		return Vector2(data["x"], data["y"])
