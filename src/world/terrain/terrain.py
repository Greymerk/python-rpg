
from random import randint
from random import Random

# Base material class
class Material:

	id = 0
	singular = 'nothing'
	passable = True
	transparent = True
	breakable = False
	image = "tile.png"
	rgb = (20, 20, 20)
	jitter = 10
	spawnable = False
	
	@classmethod
	def color(cls):
		return gritify(cls.rgb, cls.jitter)
		
	@classmethod
	def getImage(cls, x=0, y=0):
		return cls.image
		
	@classmethod
	def drop(cls):
		return cls.id

### Terrain materials below ###

class Void(Material):
	
	singular = 'the void'
	symbol = '#'	
	passable = False
	image = "tile.png"

class Grass(Material):

	id = 1
	singular = 'grass'
	symbol = '-'
	image = "grass.png"
	rgb = (0, 150, 0)
	spawnable = True
	
	@classmethod
	def getImage(cls, x=0, y=0):
		rand = Random()
		rand.seed(x | y)
		if rand.randint(0, 3) == 0:
			return "grass2.png"
		return cls.image

class Brush(Material):

	id = 2
	singular = 'brush'
	symbol = 's'
	image = "brush.png"
	rgb = (50, 100, 20)
	spawnable = True
	
	@classmethod
	def getImage(cls, x=0, y=0):
		rand = Random()
		rand.seed(x | y)
		if rand.randint(0, 30) == 0:
			return "jungle.png"
		if rand.randint(0, 10) == 0:
			return "forest.png"
		return cls.image

class FloorBrick(Material):

	id = 3
	singular = 'floor'
	symbol = 'x'
	image = "floor-brick.png"
	breakable = True
	rgb = (150, 50, 50)
	

class Foothills(Material):

	id = 4
	singular = 'foothills'
	symbol = 'n'
	image = "foothills.png"
	rgb = (150, 125, 100)
	spawnable = True


class WallBrick(Material):

	id = 5
	singular = 'stone brick'
	symbol = 'H'
	image = "wall-brick.png"
	passable = False
	transparent = False

class Mountain(Material):

	id = 6
	singular = 'a mountain'
	symbol = '^'
	image = "mountain.png"
	passable = False
	transparent = False
	rgb = (200, 200, 200)
	r = 50

class Peak(Material):

	id = 7
	singular = 'a high peak'
	symbol = 'A'
	image = "peaks.png"
	passable = False
	transparent = False
	rgb = (255, 255, 255)


class Water(Material):

	id = 8
	singular = 'still water'
	symbol = '~'
	image = "water.png"
	passable = False
	rgb = (50, 50, 120)
	#rgb = (255, 0, 0)
	r = 60

class WallStone(Material):
	id = 9
	singular = 'cobblestone'
	symbol = '&'	
	image = "wall-stone.png"
	passable = False
	breakable = True
	transparent = False
	rgb = (150, 150, 150)


class Tree(Material):
	id = 10
	singular = 'a tree'
	symbol = '@'
	image = "tree.png"
	passable = False
	breakable = True
	transparent = False
	rgb = (120, 75, 0)
	
	@classmethod
	def drop(cls):
		return Plank.id
	

class Well(Material):
	id = 11
	singular = 'a well'
	symbol = 'T'
	image = "well.png"
	passable = False

class Door(Material):
	id = 12
	singular = 'a door'	
	symbol = 'O'
	image = "door.png"
	passable = False
	breakable = True
	transparent = False
	
class Rock(Material):
	id = 13
	singular = 'a pile of rocks'
	symbol = 'R'
	image = "rocks.png"
	passable = False
	breakable = True
	transparent = False
	rgb = (80, 80, 80)
	
	@classmethod
	def drop(cls):
		return WallStone.id
	
class DeadTree(Material):

	id = 14
	singular = 'a dead tree'
	symbol = '@'
	image = "tree-dead.png"
	passable = False
	breakable = True
	rgb = (120, 75, 0)
	
	@classmethod
	def drop(cls):
		return Plank.id
	
class Sand(Material):
	id = 15
	singular = 'sand'
	symbol = 'R'
	image = "sand.png"
	passable = True
	breakable = False
	rgb = (200, 175, 50)
	spawnable = True

class Plank(Material):

	id = 16
	singular = 'plank'
	symbol = 'H'
	image = "planks.png"
	breakable = True
	rgb = (120, 75, 0)
	
lookup = {}
lookup[Void.id] = Void
lookup[Grass.id] = Grass
lookup[Brush.id] = Brush
lookup[FloorBrick.id] = FloorBrick
lookup[Foothills.id] = Foothills
lookup[WallBrick.id] = WallBrick
lookup[Mountain.id] = Mountain
lookup[Peak.id] = Peak
lookup[Water.id] = Water
lookup[WallStone.id] = WallStone
lookup[Tree.id] = Tree
lookup[Well.id] = Well
lookup[Door.id] = Door
lookup[Rock.id] = Rock
lookup[DeadTree.id] = DeadTree
lookup[Sand.id] = Sand
lookup[Plank.id] = Plank

def gritify(color, jitter):
	
	rgb = [0, 0, 0]	
	
	for i in range(3):
		c = color[i] + randint(-jitter, jitter)
		if c < 0:
			c = 0
			
		if c > 255:
			c = 255
			
		rgb[i] = c
	
	newColor = (rgb[0], rgb[1], rgb[2])
	return newColor
