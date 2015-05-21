'''
Created on 2013-05-02

@author: brian
'''

import pygame
from pygame.locals import *
from cardinals import cardinals

class Destroy:

	def __init__(self, player):
		self.player = player
		self.world = player.world
		self.direction = None
		self.finished = False
		self.player.log.append('Gather... Pick a direction')

	def nextStep(self):

		if(self.direction is not None):
			x = self.player.party.getLeader().position[0] + self.direction[0]
			y = self.player.party.getLeader().position[1] + self.direction[1]
			
			tile = self.world.getTile((x, y)).getName()
			
			if(self.world.getTile((x, y)).isBreakable()):
				material = self.world.destroy((x, y))
				self.player.avatar.pocket(material)
				self.player.log.append('Successfully gethered ' + tile)
			else:
				self.player.log.append('Unable to gether ' + tile)
					
			return True

		e = pygame.event.poll()

		if e is None:
			return False

		if e.type != KEYDOWN:
			return False
	
		if(e.key in cardinals.keys()):
			self.direction = cardinals[e.key]
			return False
		elif(e.key == K_ESCAPE):
			self.player.log.append('Cancelled')
			return True
		
		return False
