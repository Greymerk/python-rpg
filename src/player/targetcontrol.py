import pygame
from src.util import Vector2
from src.util import Cardinal
from src.actions import Cast

# observer of mouse events on viewport spaces
class TargetControl(object):

	def __init__(self, player):
		self.player = player
		
	def notify(self, cell, event):
	
		if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
			spell = self.player.avatar.quickcast
			caster = self.player.avatar
			if self.player.action is None and spell is not None:
				tar = Vector2(cell.rel)
				tar += caster.position
				if(spell.inRange(tar)):
					self.player.action = Cast(self.player, spell)
					self.player.target = tar
				return
	
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
		
			tar = Vector2(cell.rel)
			tar += self.player.avatar.position

			if self.player.action is not None:
				self.player.target = tar
				return
				
			if tar == self.player.avatar.position:
				return
				
			dir = Cardinal.toward(self.player.avatar.position, tar)
			self.player.move(dir) 		
				

		if event.type == pygame.MOUSEMOTION:
			if self.player.action is None:
				return			

			tar = Vector2(cell.rel)
			tar += self.player.avatar.position

			if self.player.action.inRange(tar):
				self.player.reticle = Vector2(cell.rel)
