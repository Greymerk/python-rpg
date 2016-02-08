import time
import sys
import os
import json

from src.actions import cardinals
from src.actions import lookup
from src.actions import Quit
from src.actions import Cast
from src.util import Vector2
from entitycontrol import EntityControl

import pygame
from pygame.locals import *
from pygame.color import THECOLORS

class Player:

	ABILITY_KEYS = [K_q, K_w, K_e, K_r]

	def __init__(self, game):
		self.game = game
		world = game.world
		self.world = world
		
		self.log = ['Welcome']
		self.world.log = self.log
		
		self.entitycontrol = EntityControl(self)
		self.lastAction = 0
		self.lastTurn = 0
		self.load() #party
		for entity in self.party:
			entity.observers.append(self.entitycontrol)
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

		mods = pygame.key.get_mods()

		for e in event:
			if(e.type == QUIT):
				self.world.quit()
			elif(e.type == KEYDOWN):

				if(e.key == K_f and mods == pygame.KMOD_NONE):
					pygame.display.toggle_fullscreen()

				if(e.key == K_m and mods == pygame.KMOD_NONE):
					self.viewingMap = not self.viewingMap

				if(e.key == K_F12 and mods == pygame.KMOD_NONE):
					self.screenshot()

				if(e.key == K_q and mods == pygame.KMOD_LALT):
					self.action = Quit(self)
				
				if(e.key in lookup and mods & (pygame.KMOD_NONE | pygame.KMOD_NUM)):
					self.action = lookup[e.key](self)
					return True
				
				if mods == pygame.KMOD_NONE:
					for i, k in enumerate(Player.ABILITY_KEYS):
						if e.key == k and len(self.avatar.abilities) > i:
							spell = self.avatar.abilities[i]
							self.action = Cast(self, spell)
						
				
				# select unit to control (deliberately off by one)
				if(e.key - 49 in range(len(self.party))):
					self.setLeader(self.party[e.key - 49])
					
			elif(e.type == KEYUP):
				pass
				
			elif e.type == pygame.MOUSEBUTTONUP:
				mpos = pygame.mouse.get_pos()
				element = self.game.view.getElement(mpos)
				if hasattr(element, 'notify'):
					element.notify(e)

		if(time.time() - self.lastAction > self.turnDelay):	

			pygame.event.pump()
			pressed = pygame.key.get_pressed()
			result = ''

			for direction in cardinals.cardinals.keys():
				if pressed[direction]:
					e = self.party.getLeader()
					newPos = Vector2(e.position)
					newPos += Vector2(cardinals.cardinals[direction])
					succeeded = e.move(Vector2(cardinals.cardinals[direction]))
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

	def setLeader(self, entity):
		if not entity in self.party:
			return
			
		self.party.leader = self.party.members.index(entity)
		self.avatar = self.party.members[self.party.leader]
		self.log.append(self.avatar.name + " is now the leader.")
		
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
			
