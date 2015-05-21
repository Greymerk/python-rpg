'''
Created on 2013-05-02

@author: brian
'''


import pygame
from pygame.locals import *
from cardinals import cardinals

class Build:

	def __init__(self, player):
		self.player = player
		self.direction = None
		self.finished = False
		self.player.log.append('Build... (Choose a block)')
		self.choices = {}
		bag = player.avatar.inventory.bag
		for i in range(len(bag)):
			if bag[i] is None:
				continue
				
			self.choices[K_0 + i + 1] = bag[i]

		self.choice = None
		
		self.options = {}
		for i in self.choices.iterkeys():
			self.options[i - K_0] = str(self.choices[i].size) + " : " + self.player.world.materials[self.choices[i].id].__name__
				
	def nextStep(self):

		if len(self.choices) is 0:
			self.player.log.append('Nothing to build with.')
			return True
	
		if(self.direction is not None and self.choice is not None):
			x = self.player.party.getLeader().position[0] + self.direction[0]
			y = self.player.party.getLeader().position[1] + self.direction[1]
			world = self.player.world
			if not world.build((x, y), self.choices[self.choice].id):
				self.player.log.append('Cannot build there')
				return True
			self.choices[self.choice].size -= 1
			bag = self.player.avatar.inventory.bag
			if bag[self.choice - K_0 - 1].size is 0:
				bag[self.choice - K_0 - 1] = None
			return True
				
		e = pygame.event.poll()

		if e is None:
			return False

		if e.type != KEYDOWN:
			return False

		if(self.choice is None):
			if(e.key in self.choices):
				self.choice = e.key
				self.player.log.append('Build... (Choose a direction)')
			elif(e.key == K_ESCAPE):
				self.player.log.append('Cancelled')
				return True
			
			return False
			
		if(self.direction is None):
			if(e.key in cardinals.keys()):
				self.direction = cardinals[e.key]
				return False
			elif(e.key == K_ESCAPE):
				self.player.log.append('Cancelled')
				return True
						
		return False
	
