'''
Created on 2013-05-23

@author: brian
'''

import pygame
from pygame.color import THECOLORS
from src.util import Vector2
from cell import Cell

class Viewport(object):

	def __init__(self, surface, pos, world, player, images):
		self.images = images
		self.surface = surface
		self.pos = pos
		self.world = world
		self.player = player
		self.reticule = pygame.transform.scale2x(images.get("reticule"))				   
	
	def display(self, info):
		self.fontobject = pygame.font.Font(None,24)
		for i, line in enumerate(info):
			self.surface.blit(self.fontobject.render(line[0], 1, (255,255,255)), (16, (i + 1) * 16))	
		
	def draw(self):
		if(self.player.viewingMap):
			self.drawMap()
			return
			
		self.drawGame()

	
	def drawGame(self):
		self.surface.fill(THECOLORS["black"])
		camPos = self.player.party.getLeader().position

		for row in range(17):
			for col in range(17):
				relPos = camPos[0] - 8 + col, camPos[1] - 8 + row
				cell = self.world.getTile(relPos)
				ground = cell.getGround()
				imgName = ground.getImage(relPos)
				image = self.images.get(imgName, relPos)
				dest = (col * 32), (row * 32)
				if not self.player.party.canSee(relPos):
					continue
				self.surface.blit(image, dest)

		for e in self.world.getAllEntities():
			e.draw(self.surface, camPos, self.images, self.visible)
		
		if self.player.action is not None:
			if hasattr(self.player.action, 'location'):
				if self.player.action.location is not None:
					x = 32 * (8 + self.player.action.location[0])
					y = 32 * (8 + self.player.action.location[1])
					self.surface.blit(self.reticule, (x, y))


	def drawMap(self):
		
		self.surface.fill(THECOLORS["wheat4"])
		
		x, y = self.player.party.getLeader().position
		x, y = (int(x) >> 4) - 8, (int(y) >> 4) - 8
			  
		for row in range(17):
			for col in range(17):
				img = self.world.chunkManager.getMap(x + col, y + row)
				if img is None:
					continue
				
				dest = (col * 32), (row * 32)
				self.surface.blit(img, dest)
			  
		x, y = self.player.party.getLeader().position  
		leftChunk, topChunk = (int(x) >> 4) - 8, (int(y) >> 4) - 8
					
		for mob in self.world.mobManager.mobs:

				
			mobX, mobY = int(mob.position[0]), int(mob.position[1])
			mobLeft, mobTop = mobX >> 4, mobY >> 4
			 
			posx, posy = ((mobLeft - leftChunk) * 32) + ((mobX % 16) * 2), ((mobTop - topChunk) * 32) + ((mobY % 16) * 2)
				
			self.surface.set_at((posx, posy), (255, 0, 0))
			self.surface.set_at((posx, posy + 1), (255, 0, 0))
			self.surface.set_at((posx + 1, posy), (255, 0, 0))
			self.surface.set_at((posx + 1, posy + 1), (255, 0, 0))
			
		for e in self.world.friendly:

				
			mobX, mobY = int(e.position[0]), int(e.position[1])
			mobLeft, mobTop = mobX >> 4, mobY >> 4
			 
			posx, posy = ((mobLeft - leftChunk) * 32) + ((mobX % 16) * 2), ((mobTop - topChunk) * 32) + ((mobY % 16) * 2)
				
			self.surface.set_at((posx, posy), (0, 0, 255))
			self.surface.set_at((posx, posy + 1), (0, 0, 255))
			self.surface.set_at((posx + 1, posy), (0, 0, 255))
			self.surface.set_at((posx + 1, posy + 1), (0, 0, 255))
			
		leader = self.player.party.getLeader()
		avatarX, avatarY = int(leader.position[0]), int(leader.position[1])
		avatarLeft, avatarTop = avatarX >> 4, avatarY >> 4
		 
		posx, posy = ((avatarLeft - leftChunk) * 32) + ((avatarX % 16) * 2), ((avatarTop - topChunk) * 32) + ((avatarY % 16) * 2)
			
		self.surface.set_at((posx, posy), (255, 255, 0))
		self.surface.set_at((posx, posy + 1), (255, 255, 0))
		self.surface.set_at((posx + 1, posy), (255, 255, 0))
		self.surface.set_at((posx + 1, posy + 1), (255, 255, 0))
		
		
	def visible(self, pos):
			
		camPos = self.player.party.getLeader().position
		
		relx = pos[0] - camPos[0]  
		rely = pos[1] - camPos[1] 
		
		if abs(relx) > 8 or abs(rely) > 8:
			return False
			
		return self.player.party.canSee(pos)
		
	def getElement(self, pos):
		vec = Vector2(pos)
		vec -= self.pos
		rel = Vector2(int(vec[0] / 32) - 8, int(vec[1] / 32) - 8)
		rel += self.player.avatar.position
		return self.world.getEntityFromLocation(rel)
		
		
