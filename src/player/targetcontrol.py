import pygame
from src.util import Vector2

class TargetControl(object):

	def __init__(self, player):
		self.player = player
		
	def notify(self, location, event):
		pass