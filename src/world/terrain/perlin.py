import random

class Perlin:

	def __init__(self, nSeed):
		
		self.mask = 0xFF
		self.size = 256
	
		random.seed(nSeed)

		self.p = range(self.size)
		random.shuffle(self.p)
		self.gradientX = self.gradientY = [0]*self.size

		for i in range(self.size):
			self.gradientX[i] = float(random.randint(0,32767))/(32768/2)-1
			self.gradientY[i] = float(random.randint(0,32767))/(32768/2)-1
				

	def noise(self, point):

		# find neighbouring grid points
		surroundingPoints = self.getSurroundingGridPoints(point)
		
		# find offsets between point and neighbouring grid-points
		offsets = self.getGridOffsets(point)

		# permute values to get pseudo randomly chosen gradients
		gradients = self.selectGradients(surroundingPoints)

		# computer the dot product between the vectors and the gradients
		dotProducts = self.computeDotProduct(gradients, offsets)

		#modulate with the weight function
		weightX = self.weight(offsets[0])
		weightY = self.weight(offsets[2])
		
		v0 = dotProducts[0] - weightX * (dotProducts[0] - dotProducts[1])
		v1 = dotProducts[2] - weightX * (dotProducts[2] - dotProducts[3])

		v = v0 - weightY * (v0 - v1)

		return v

	def getSurroundingGridPoints(self, (x, y)):
		i0 = int(x)
		i1 = i0 + 1

		j0 = int(y)
		j1 = j0 + 1

		gpx0 = i0 & self.mask
		gpx1 = i1 & self.mask

		gpy0 = j0 & self.mask
		gpy1 = j1 & self.mask

		return gpx0, gpx1, gpy0, gpy1
		
	def getGridOffsets(self, (x, y)):
		
		i = int(x)
		j = int(y)
		
		tx0 = x - float(i)
		tx1 = tx0 - 1
		
		ty0 = y - float(j)
		ty1 = ty0 - 1
		
		return tx0, tx1, ty0, ty1
		

	def selectGradients(self, (qx0, qx1, qy0, qy1)):
		q00 = self.p[(qy0 + self.p[qx0]) & self.mask]
		q01 = self.p[(qy0 + self.p[qx1]) & self.mask]

		q10 = self.p[(qy1 + self.p[qx0]) & self.mask]
		q11 = self.p[(qy1 + self.p[qx1]) & self.mask]
		
		return q00, q01, q10, q11
	
	def computeDotProduct(self, (q00, q01, q10, q11), (tx0, tx1, ty0, ty1)):
		vec00 = self.gradientX[q00]*tx0 + self.gradientY[q00]*ty0
		vec01 = self.gradientX[q01]*tx1 + self.gradientY[q01]*ty0

		vec10 = self.gradientX[q10]*tx0 + self.gradientY[q10]*ty1
		vec11 = self.gradientX[q11]*tx1 + self.gradientY[q11]*ty1
		
		return vec00, vec01, vec10, vec11
	
	def weight(self, value):
		return (3 - (2 * value)) * value * value
		
		
		




		


