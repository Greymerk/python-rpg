from simplex import Simplex
import terrain
import random
import tile

# This class generates new chunks on request
class ChunkGen:
	
	def __init__(self, seed, inChunkPos):
		self.chunkPos = inChunkPos
		random.seed(seed)
		self.noiseGen = Simplex(seed)
		self.chunkSize = 16

		self.mats = {}
		self.mats[-10]  = terrain.Water.id
		self.mats[-9]  = terrain.Water.id
		self.mats[-8]  = terrain.Water.id
		self.mats[-7]  = terrain.Water.id
		self.mats[-6]  = terrain.Water.id
		self.mats[-5]  = terrain.Water.id
		self.mats[-4]  = terrain.Water.id
		self.mats[-3]  = terrain.Water.id
		self.mats[-2]  = terrain.Water.id
		self.mats[-1]  = terrain.Water.id
		self.mats[0]  = terrain.Water.id
		self.mats[1]  = terrain.Sand.id
		self.mats[2]  = terrain.Grass.id
		self.mats[3]  = terrain.Grass.id
		self.mats[4]  = terrain.Brush.id
		self.mats[5]  = terrain.Foothills.id
		self.mats[6]  = terrain.Mountain.id
		self.mats[7]  = terrain.Mountain.id
		self.mats[8]  = terrain.Peak.id
		self.mats[9]  = terrain.Peak.id
		self.mats[10]  = terrain.Peak.id

	# Call this when you want a new chunk
	def generate(self):

		# create blank chunk
		newChunk = [tile.Tile() for i in range(self.chunkSize ** 2)]

		# fill in the basic terrain
		newChunk = self.genTerrain(newChunk)

		# add decorations, like trees
		newChunk = self.decorate(newChunk)

		return newChunk

	def genTerrain(self, newChunk):

		octaves = 6
		persistence = 0.75
		scale = 0.004
		
		for row in range(self.chunkSize):
			for col in range(self.chunkSize):

				xPos = (self.chunkPos[0]*self.chunkSize + col)
				yPos = (self.chunkPos[1]*self.chunkSize + row)

				elevation = self.noiseGen.octave_noise_2d(octaves, persistence, scale, xPos, yPos)

				elevation *= 15

				elevation = int(elevation)

				ground = self.getGroundMat(elevation)

				newChunk[row*self.chunkSize + col].setGround(ground)

		return newChunk

		

	# takes an integer argument (0-9)
	# returns a tile
	def getGroundMat(self, elevation):

		if (elevation < -10):
			elevation = -10

		if (elevation > 9):
			elevation = 9

		newMat = self.mats[elevation]

		return newMat

	def decorate(self, newChunk):

		# add some features
		for i in range(self.chunkSize ** 2):

			if(newChunk[i].getGround() in [terrain.Grass, terrain.Brush]):
	
				# add trees and stuff
				if(random.randint(0,10) == 0):
					
					if random.randint(0, 4) == 0:
						newChunk[i].build(terrain.DeadTree.id)
					else:
						newChunk[i].build(terrain.Tree.id)
					
			if(newChunk[i].getGround() == terrain.Foothills):
				
				if(random.randint(0,10) == 0):
					newChunk[i].build(terrain.Rock.id)

		return newChunk