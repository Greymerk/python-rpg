from vector import Vector2

class Line(object):

	def __init__(self, start, end):
		self.start = start
		self.end = end
 

	def __iter__(self):
		error = 0
		deltax = self.end.x - self.start.x
		deltay = self.end.y - self.start.y
		if deltax == 0:
			for y in xrange(int(self.start.y), int(self.end.y), Line.sign(self.end.y - self.start.y)):
				yield Vector2(self.start.x, y)
			
		else:
			deltaerr = abs(deltay / deltax)
			y = self.start.y
			for x in xrange(int(self.start.x), int(self.end.x), Line.sign(self.end.x - self.start.x)):
				yield Vector2(x, y)
				error += deltaerr
				while error >= 0.5:
					yield Vector2(x, y)
					y += Line.sign(self.end.y - self.start.y)
					error -= 1.0

	@staticmethod
	def sign(n):
		return 1 if n >= 0 else -1

