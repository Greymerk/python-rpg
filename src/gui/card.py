import pygame
from pygame.color import THECOLORS
from src.util import Vector2

class Card(object):

	def __init__(self, surface, pos, index, player, images):
		self.surface = surface
		self.pos = pos
		self.player = player
		self.index = index
		self.images = images
		self.font = pygame.font.Font(None,16)
		self.size = 32
		self.fontobject = pygame.font.Font(None,24)
		
	def draw(self):
		if not self.index in range(len(self.player.party.members)):
			return
		unit = self.player.party.members[self.index]
		self.surface.fill(THECOLORS["black"])
		rect = pygame.Rect((0,0), (self.size, self.size))
		self.surface.blit(unit.getImage(self.images), rect)
		
		if unit is self.player.avatar:
			color = THECOLORS["gold"]
		else:
			color = THECOLORS["gray"]
		
		message = unit.name + ' - ' + str(unit.health) + 'HP'
		self.surface.blit(self.fontobject.render(message, 1, color), (42, 0))
		message = str(unit.position[0]) + ', ' + str(unit.position[1]) 
		self.surface.blit(self.fontobject.render(message, 1, color), (42, 16))
		
		aOffset = 200
		for i, ability in enumerate(unit.abilities):
			image = self.images.get(ability.icon)
			rect = pygame.Rect((i * self.size + aOffset, 0),((i + 1) * self.size + aOffset, self.size))
			self.surface.blit(image, rect)
			self.surface.blit(self.font.render(str(pygame.key.name(self.player.ABILITY_KEYS[i])).upper(), 1, THECOLORS["gray"]), (i * self.size + aOffset,0))
			
	def getElement(self, pos):
		v = Vector2(pos)
		if not self.index in range(len(self.player.party.members)):
			return
		unit = self.player.party.members[self.index]
		v -= self.pos
		if v[0] < 200:
			return unit
		
		
