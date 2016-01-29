'''
Created on 2013-05-23

@author: brian
'''

import pygame
from pygame.color import THECOLORS

class Viewport(object):

	def __init__(self, surface, world, player, images):
		self.images = images
		self.surface = surface
		self.world = world
		self.player = player
		self.previousPosition = None
		self.mapOverlay = images.get("map-overlay")
		self.reticule = pygame.transform.scale2x(images.get("reticule"))
		self.grid = [None]*289
		self.mapCache = {}
		self.viewCache = None
		self.currentTurn = None
		self.cameraPosition = None
			
	def update(self):	  
		
		leader = self.player.party.getLeader()

		if self.currentTurn == self.world.time and leader.position == self.cameraPosition:
			return

		self.currentTurn = self.world.time
		self.viewCache = None
		self.cameraPosition = leader.position

		if leader is not None:
			x, y = int(leader.position[0]), int(leader.position[1])
		else:
			x, y = 0, 0

		tileX, tileY = x - 8, y - 8
		chunkX, chunkY = (x >> 4) - 8, (y >> 4) - 8
		
		for row in range(17):
			for col in range(17):
				tilePos = (tileX + col, tileY + row)
				if not self.player.party.canSee(tilePos):
					t = None
				else:
					t = self.world.getTile((tileX + col, tileY + row))
				self.grid[row*17+col] = t

				newMap = self.updateMap(chunkX + col, chunkY + row)
				if newMap is not None:
					self.mapCache[(chunkX + col, chunkY + row)] = newMap 



	def updateMap(self, x, y):
		
		if (not self.world.chunkManager.isLoaded(x, y)) and (x, y) in self.mapCache.keys():
			return None
		
		return self.world.chunkManager.getMap(x, y)

				   
	
	def display(self, info):
		self.fontobject = pygame.font.Font(None,24)
		for i, line in enumerate(info):
			self.surface.blit(self.fontobject.render(line[0], 1, (255,255,255)), (10, i * 16))	
		
	def draw(self):
		
		self.surface.fill((0,0,0))
		if(self.player.viewingMap):
			self.drawMap()
			return
			
		self.drawGame()

	
	def drawGame(self):

		camPos = self.player.party.getLeader().position
		
		if self.viewCache is None:
		
			self.viewCache = self.surface.copy()
			
			for row in range(17):
				for col in range(17):
					cell = self.grid[row * 17 + col]
					if cell is None:
						continue

					ground = cell.getGround()
					relPos = camPos[0] - 8 + col, camPos[1] - 8 + row
					imgName = ground.getImage(relPos)
					image = self.images.get(imgName, relPos)
					dest = (col * 32), (row * 32)

					self.viewCache.blit(image, dest)
		
		self.surface.blit(self.viewCache, (0,0))

		

		for e in self.world.getAllEntities():
			e.draw(self.surface, camPos, self.images, self.visible)
		
		if self.player.action is not None:
			if hasattr(self.player.action, 'location'):
				if self.player.action.location is not None:
					x = 32 * (8 + self.player.action.location[0])
					y = 32 * (8 + self.player.action.location[1])
					self.surface.blit(self.reticule, (x, y))
	
	def drawMap(self):
		
		self.surface.fill(THECOLORS["papayawhip"])
		
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
		
		self.surface.blit(self.mapOverlay, (0,0))
		
	def visible(self, pos):
			
		camPos = self.player.party.getLeader().position
		
		relx = pos[0] - camPos[0]  
		rely = pos[1] - camPos[1] 
		
		if abs(relx) > 8 or abs(rely) > 8:
			return False
			
		return self.player.party.canSee(pos)


