'''
Created on 2013-05-03

@author: brian
'''


import pygame
from pygame.locals import *
from pygame.color import THECOLORS
from src.util import Vector2

from card import Card

class Options(object):

	def __init__(self, surface, pos, player, images):
		
		self.surface = surface
		self.pos = pos
		self.player = player
		self.tileSize = 32
		
		self.party = []
		for i in range(6):
			p = (0, self.tileSize * i)
			rect = pygame.Rect(p, (396, self.tileSize))
			self.party.append(Card(self.surface.subsurface(rect), p, i, player, images))
		self.selected = 0
		self.player = player

		self.fontobject = pygame.font.Font(None,24)

	def draw(self):
		pygame.event.pump()
		pressed = pygame.key.get_pressed()

		self.surface.fill(THECOLORS["black"])
		if not hasattr(self.player.action, 'options'):
			self.drawParty()
			return
		
		options = self.player.action.options
		if options is None:
			self.drawParty()
			return
		  
		count = 0
		for line in options:
			self.surface.blit(self.fontobject.render('>> ' + str(line) + ' - ' + str(options[line]), 1, (255,255,255)), (0, 16*count))
			count += 1

	def drawParty(self):
		count = 0
		for i, e in enumerate(self.player.world.friendly.members):
			self.party[i].draw()

			
	def getMaxLines(self):
		return self.surface.get_height()/16
		
	def notify(self, pos, event):
		v = Vector2(pos)
		v -= self.pos
		y = int(v[1] / 32)
		if y in range(len(self.party)):
			card = self.party[y]
			card.notify(v, event)
			
			
