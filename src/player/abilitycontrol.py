import pygame
from src.util import Vector2
from src.actions import Cast

# observer of mouse events on viewport spaces
class AbilityControl(object):

	def __init__(self, player):
		self.player = player
		
	def notify(self, ability, event):
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			if self.player.action is None:
				self.player.setLeader(ability.caster)
				self.player.action = Cast(self.player, ability.ability)
