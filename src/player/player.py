import time
import sys

import os

from pickle import Pickler
from pickle import Unpickler


from actions import cardinals
from actions import lookup

import pygame
from pygame.locals import *
from pygame.color import THECOLORS

class Player:

	def __init__(self, world):
		self.world = world
		
		self.log = ['Welcome']
		self.world.log = self.log
		
		self.lastAction = 0
		self.load()
		self.world.friendly = self.party.members
		self.lastTarget = None

		self.avatar = self.party.getLeader()
		self.viewingMap = False
		self.action = None
		self.turnDelay = 0.2

		self.screenshot = None #initialized by the GameView class

	# Called on every frame
	# Return true if the player hasn't used his or her turn yet
	# Return false to allow the rest of the world to take a turn
	def turn(self):

		if self.action is not None:
			finished = self.action.nextStep()
			if(finished):
				self.action = None
				self.lastAction = time.time()
				return False
			else:
				return True
		'''
		if not self.party.getLeader().isAlive():
			if(time.time() - self.lastAction > self.turnDelay):
				self.lastAction = time.time()
				return False
		'''
		
		if not self.party.getLeader().isAlive():
			leader = self.party.resetLeader()
			self.avatar = leader
			self.log.append(leader.name + " is now the leader.")
			
		event = pygame.event.get()

		for e in event:
			if(e.type == QUIT):
				self.world.quit()
			elif(e.type == KEYDOWN):

				if(e.key == K_f):
					pygame.display.toggle_fullscreen()

				if(e.key == K_m):
					self.viewingMap = True

				if(e.key == K_PRINT):
					self.screenshot()

				if(e.key in lookup):
					self.action = lookup[e.key](self)
					return True
				
				# select unit to control (deliberately off by one)
				if(e.key - 49 in range(9)):
					leader = self.party.setLeader(e.key - 49)
					if leader is not None:
						self.avatar = leader
						self.log.append(leader.name + " is now the leader.")
					
			elif(e.type == KEYUP):
				
				if(e.key == K_m):
					self.viewingMap = False

		if(time.time() - self.lastAction > self.turnDelay):	

			pressed = pygame.key.get_pressed()
			result = ''

			for direction in cardinals.cardinals.keys():
				if pressed[direction]:
					e = self.party.getLeader()
					newPos = e.position[0] + cardinals.cardinals[direction][0], e.position[1] + cardinals.cardinals[direction][1]
					succeeded = e.move(cardinals.cardinals[direction])
					if succeeded:
						msg = cardinals.names[direction]
					else:
						msg = "Blocked by " + self.world.look(newPos)
					self.log.append(msg)
					self.lastAction = time.time()
					return False
			
			if pressed[K_SPACE]:
				self.log.append('Pass Turn')
				self.lastAction = time.time()
				return False
			
		return True
					

	
	def save(self):
		data = {}
		data['members'] = self.party.save()

		f = open('save/player', 'w')
		p = Pickler(f)
		p.dump(data)
		f.close()
		
	def load(self):

		if not os.path.isfile('save/player'):
			self.party = self.world.loadParty(None)
			return

		f = open('save/player', 'r')
		p = Unpickler(f)
		data = p.load()
		f.close()	

		if 'members' in data.keys():
			self.party = self.world.loadParty(data['members'])
		else:
			self.party = self.world.loadParty(None)
			

