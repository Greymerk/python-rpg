import pygame
from src.util import Vector2

class EntityControl(object):

	def __init__(self, player):
		self.player = player
		
	def notify(self, entity, event):
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			if self.player.action is None:
				if entity in self.player.party:
					self.player.setLeader(entity)
			