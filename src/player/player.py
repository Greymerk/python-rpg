import time
import sys
import os
import json

from src.util import Cardinal
from src.actions import lookup
from src.actions import Quit
from src.actions import Cast
from src.util import Vector2
from entitycontrol import EntityControl
from targetcontrol import TargetControl
from abilitycontrol import AbilityControl

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
		self.targetcontrol = TargetControl(self)
		self.abilitycontrol = AbilityControl(self)
		self.lastAction = 0
		self.lastTurn = 0
		self.load() #party
		self.reticle = (0, 0)
		self.target = None
		for entity in self.party:
			entity.observers.append(self.entitycontrol)
			for ability in entity.abilities:
				ability.observers.append(self.abilitycontrol)
		self.world.friendly = self.party
		self.lastTarget = None

		self.avatar = self.party.getLeader()
		self.viewingMap = False
		self.debug = False
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
				self.target = None
				self.lastAction = time.time()
				return False
			else:
				return True
		
		if not self.party.getLeader().isAlive():
			leader = self.party.resetLeader()
			self.avatar = leader
			self.log.append(leader.name + " is now the leader.")
			
		events = pygame.event.get()

		mods = pygame.key.get_mods()

		for e in events:
			if(e.type == QUIT):
				self.world.quit()
			elif(e.type == KEYDOWN):

				if e.key == K_m:
					self.viewingMap = not self.viewingMap

				if e.key == K_F2:
					self.screenshot()

				if e.key == K_F3:
					self.debug = not self.debug

				if e.key == K_F12:
					self.action = Quit(self)
				
				if e.key in lookup:
					self.action = lookup[e.key](self)
					return True
				
				for i, k in enumerate(Player.ABILITY_KEYS):
					if e.key == k and len(self.avatar.abilities) > i:
						spell = self.avatar.abilities[i]
						if not spell.ready():
							self.log.append('Ability on cooldown!')
							return True
						self.action = Cast(self, spell)
						
				# select unit to control (deliberately off by one)
				if(e.key - 49 in range(len(self.party.members))):
					self.setLeader(self.party.members[e.key - 49])
					
			elif(e.type == KEYUP):
				pass
				
			
			elif e.type == pygame.MOUSEBUTTONUP or e.type == pygame.MOUSEMOTION:
				last = self.lastAction
				self.mouse_event(e)
				if last != self.lastAction:
					# A turn was completed via a mouse
					return False


		if(time.time() - self.lastAction > self.turnDelay):	

			pygame.event.pump()
			pressed = pygame.key.get_pressed()
			result = ''

			for direction in Cardinal.key_map.keys():
				if pressed[direction]:
					self.move(Cardinal.key_map[direction])
					return False
			
			if pressed[K_SPACE]:
				self.log.append('Pass Turn')
				self.lastAction = time.time()
				self.lastTurn = self.world.time
				return False
			
		return True
	
	def move(self, direction):
		e = self.party.getLeader()
		newPos = Vector2(e.position)
		newPos += Vector2(Cardinal.values[direction])
		succeeded = e.move(Cardinal.values[direction])
		if succeeded:
			msg = Cardinal.names[direction]
			self.world.getTile(newPos).getGround().stepSound(self.world.sounds)
		else:
			msg = "Blocked by " + self.world.look(newPos)
			self.world.sounds.get("oomph.wav").play()
		self.log.append(msg)
		self.lastAction = time.time()
		self.lastTurn = self.world.time

	def setLeader(self, entity):
		if not entity in self.party:
			return
			
		i = self.party.members.index(entity)
		self.avatar = self.party.setLeader(i)		

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
			
	def mouse_event(self, event):
		self.game.view.notify(pygame.mouse.get_pos(), event)
