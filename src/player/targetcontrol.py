import pygame
from src.util import Vector2

# observer of mouse events on viewport spaces
class TargetControl(object):

	def __init__(self, player):
		self.player = player
		
	def notify(self, cell, event):
		self.player.reticle = Vector2(cell.rel)
