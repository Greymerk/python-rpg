import pygame
from src.util import Vector2
from src.actions import Cast

# observer of mouse events on viewport spaces
class AbilityControl(object):

	def __init__(self, player):
		self.player = player
		
	def notify(self, ability, event):
		if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
			ability.caster.quickcast = ability
			return
	
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			if self.player.action is None:
				self.player.setLeader(ability.caster)
				if not ability.ready():
					self.player.log.append('Ability on cooldown!')
					return
				self.player.action = Cast(self.player, ability)
