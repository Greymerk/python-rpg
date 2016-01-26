import time
import sys
import os
import json

from src.actions import cardinals
from src.actions import lookup
from src.util import Vector2

import pygame
from pygame.locals import *
from pygame.color import THECOLORS

class Player:

	def __init__(self, world):
		self.world = world
		
		self.log = ['Welcome']
		self.world.log = self.log
		
		self.lastAction = 0
		self.lastTurn = 0
		self.load()
		self.world.friendly = self.party
		self.lastTarget = None

		self.avatar = self.party.getLeader()
		self.viewingMap = False
		self.action = None
		self.turnDelay = 0.3
	
		pygame.key.set_repeat()

		self.screenshot = None #initialized by the GameView class

	# Called on every frame
	# Return true if the player hasn't used his or her turn yet
	# Return false to allow the rest of the world to take a turn
	def turn(self):

		#if self.lastTurn is self.world.time:
		#	return False

		if self.action is not None:
			finished = self.action.nextStep()
			if(finished):
				self.action = None
				self.lastAction = time.time()
				return False
			else:
				return True
		
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

				if(e.key == K_F12):
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

			pygame.event.pump()
			pressed = pygame.key.get_pressed()
			result = ''

			for direction in cardinals.cardinals.keys():
				if pressed[direction]:
					e = self.party.getLeader()
					newPos = e.position[0] + cardinals.cardinals[direction][0], e.position[1] + cardinals.cardinals[direction][1]
					succeeded = e.move(cardinals.cardinals[direction])
					if succeeded:
						msg = cardinals.names[direction]
						self.world.getTile(newPos).getGround().stepSound(self.world.sounds)
					else:
						msg = "Blocked by " + self.world.look(newPos)
						self.world.sounds.get("oomph.wav").play()
					self.log.append(msg)
					self.lastAction = time.time()
					self.lastTurn = self.world.time
					return False
			
			if pressed[K_SPACE]:
				self.log.append('Pass Turn')
				self.lastAction = time.time()
				self.lastTurn = self.world.time
				return False
			
		return True


	def save(self):
		data = {}
		data['members'] = self.party.save()

		with open('save/player', 'w') as f:
			json.dump(data, f, sort_keys=True, indent=4)
		
	def load(self):

		if not os.path.isfile('save/player'):
			self.party = self.world.loadParty(None)
			return

		with open('save/player', 'r') as f:
			data = json.load(f)	

		if 'members' in data.keys():
			self.party = self.world.loadParty(data['members'])
		else:
			self.party = self.world.loadParty(None)
			
