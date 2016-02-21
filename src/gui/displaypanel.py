import pygame

from src.util import Vector2
from cell import Cell
from status import Status
from options import Options
from output import Output

class DisplayPanel(object):

	def __init__(self, surface, pos, player, images):
		self.surface = surface
		self.pos = pos
		self.player = player
		self.images = images
		
		self.optionsPos = (0,0)
		self.optionsRect = pygame.Rect(self.optionsPos, (Cell.size * 12, Cell.size * 6))
		self.options = Options(self.surface.subsurface(self.optionsRect), self.optionsPos, self.player, images)
		
		self.statusPos = (0, Cell.size * 6 + Cell.size)
		self.statusRect = pygame.Rect(self.statusPos, (Cell.size * 12, Cell.size))
		self.status = Status(self.surface.subsurface(self.statusRect), self.statusPos, self.player, images)
		
		self.logPos = (0, Cell.size * 7 + (Cell.size * 2))
		self.logRect = pygame.Rect(self.logPos, (Cell.size * 12, Cell.size * 8))
		self.log = Output(self.surface.subsurface(self.logRect), self.logPos, self.player.log)
		
		
	def draw(self):
		self.options.draw()
		self.status.draw()
		self.log.draw()
		
	def notify(self, pos, event):
		vec = Vector2(pos)
		vec -= self.pos
		
		point = (int(vec[0]), int(vec[1]))
		if self.optionsRect.collidepoint(point):
			self.options.notify(point, event)
			
		if self.statusRect.collidepoint(point):
			self.status.notify(point, event)
			
		if self.logRect.collidepoint(point):
			self.log.notify(point, event)
		
		
