import pygame
from src.util import Vector2

class EntityControl(object):

	def __init__(self, player):
		self.player = player
		
	def notify(self, entity, event):
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			if self.player.action is not None:
				self.player.target = entity.position
				return

			if entity in self.player.party:
				self.player.setLeader(entity)

		if event.type == pygame.MOUSEMOTION:
			if self.player.action is not None:
				rel = Vector2(entity.position)
				rel -= self.player.avatar.position
				self.player.reticle = rel
			
