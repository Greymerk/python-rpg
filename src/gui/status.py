import pygame
from pygame.color import THECOLORS
from src.util import Vector2

class Status(object):

	def __init__(self, surface, pos, player, images):
		self.pos = pos
		self.surface = surface
		self.player = player
		self.images = images
		self.font = pygame.font.Font(None,16)
		self.size = 32
		
	def draw(self):
		self.surface.fill(THECOLORS["black"])
			
	def getElement(self, pos):
		return None

