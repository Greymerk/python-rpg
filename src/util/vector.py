import math


class Vector2(object):

        def __init__(self, x, y):
                self.x = x
		self.y = y

	def dist(self, other):
		relx = abs(self.x - other.x)
		rely = abs(self.y - other.y)
		return math.sqrt(relx**2 + rely**2)

        def __add__(self, other):
                self.x += other.x
                self.y += other.y

	def __eq__(self, other):
		if self.x != other.x:
			return False

		if self.y != other.y:
			return False

		return True

        def __str__(self):
                return str(self.x) + ' ' + str(self.y)

