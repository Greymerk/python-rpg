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
		self.mapOverlay = images.get("map-overlay.png")
		self.reticule = pygame.transform.scale2x(images.get("reticule.png"))
		self.grid = [None]*289
		self.mapCache = {}
		self.currentTurn = None
		self.cameraPosition = None

			
	def update(self):	  
		
		leader = self.player.party.getLeader()

		if self.currentTurn == self.world.time and leader.position == self.cameraPosition:
			return

		self.currentTurn = self.world.time
		self.cameraPosition = leader.position

		if leader is not None:
			x, y = leader.position
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
				
		# get list of tile IDs
		mapData = self.world.chunkManager.getMap(x, y)
		
		if mapData is None:
			return None
		
		# create surface
		imageMap = pygame.Surface((32, 32))
		pixelMap = pygame.PixelArray(imageMap)
				
		for row in range(16):
			for col in range(16):
				cell = mapData[row * 16 + col]
				color = cell.color()
				pixelMap[col * 2	, row * 2] = color
				pixelMap[col * 2	, row * 2 + 1] = color
				pixelMap[col * 2 + 1, row * 2] = color
				pixelMap[col * 2 + 1, row * 2 + 1] = color
				
		return pixelMap.surface
				   
		
		
	def draw(self):
		
		self.surface.fill((0,0,0))
		if(self.player.viewingMap):
			self.drawMap()
		else:
			self.drawGame()

	
	def drawGame(self):

		camPos = self.player.party.getLeader().position

		for row in range(17):
			for col in range(17):
				cell = self.grid[row * 17 + col]
				if cell is None:
					continue

				ground = cell.getGround()
				image = self.images.get(ground.getImage(camPos[0] - 8 + col, camPos[1] - 8 + row))
				dest = (col * 32), (row * 32)

				self.surface.blit(image, dest)

		entitiesOnScreen = []

		for e in list(set(self.world.mobManager.mobs) | set(self.world.friendly)):
			relx = e.position[0] - camPos[0]  
			rely = e.position[1] - camPos[1] 
			
			if abs(relx) > 8 or abs(rely) > 8:
				continue

			if not self.player.party.canSee(e.position):
				continue
			
			entitiesOnScreen.append(e)
			
		entitiesOnScreen.sort(lambda a, b: cmp(a.isAlive(), b.isAlive()))
		
		for e in entitiesOnScreen:
			relx = e.position[0] - camPos[0]  
			rely = e.position[1] - camPos[1] 
			e.draw(self.surface, relx, rely, self.images)
			
		if self.player.action is not None:
			if hasattr(self.player.action, 'location'):
				if self.player.action.location is not None:
					x = 32 * (8 + self.player.action.location[0])
					y = 32 * (8 + self.player.action.location[1])
					self.surface.blit(self.reticule, (x, y))
	
	def drawMap(self):
		
		self.surface.fill(THECOLORS["navajowhite"])
		
		x, y = self.player.party.getLeader().position
		x, y = (x >> 4) - 8, (y >> 4) - 8
			  
		for row in range(17):
			for col in range(17):
				if (x + col, y + row) in self.mapCache.keys():
					dest = (col * 32), (row * 32)
					self.surface.blit(self.mapCache[(x + col, y + row)], dest)
			  
		x, y = self.player.party.getLeader().position	  
		leftChunk, topChunk = (x >> 4) - 8, (y >> 4) - 8
					
		for mob in self.world.mobManager.mobs:

				
			mobX, mobY = mob.position[0], mob.position[1]
			mobLeft, mobTop = mobX >> 4, mobY >> 4
			 
			posx, posy = ((mobLeft - leftChunk) * 32) + ((mobX % 16) * 2), ((mobTop - topChunk) * 32) + ((mobY % 16) * 2)
				
			self.surface.set_at((posx, posy), (255, 0, 0))
			self.surface.set_at((posx, posy + 1), (255, 0, 0))
			self.surface.set_at((posx + 1, posy), (255, 0, 0))
			self.surface.set_at((posx + 1, posy + 1), (255, 0, 0))
			
		for e in self.world.friendly:

				
			mobX, mobY = e.position[0], e.position[1]
			mobLeft, mobTop = mobX >> 4, mobY >> 4
			 
			posx, posy = ((mobLeft - leftChunk) * 32) + ((mobX % 16) * 2), ((mobTop - topChunk) * 32) + ((mobY % 16) * 2)
				
			self.surface.set_at((posx, posy), (0, 0, 255))
			self.surface.set_at((posx, posy + 1), (0, 0, 255))
			self.surface.set_at((posx + 1, posy), (0, 0, 255))
			self.surface.set_at((posx + 1, posy + 1), (0, 0, 255))
			
		
		avatarX, avatarY = self.player.party.getLeader().position
		avatarLeft, avatarTop = avatarX >> 4, avatarY >> 4
		 
		posx, posy = ((avatarLeft - leftChunk) * 32) + ((avatarX % 16) * 2), ((avatarTop - topChunk) * 32) + ((avatarY % 16) * 2)
			
		self.surface.set_at((posx, posy), (255, 255, 0))
		self.surface.set_at((posx, posy + 1), (255, 255, 0))
		self.surface.set_at((posx + 1, posy), (255, 255, 0))
		self.surface.set_at((posx + 1, posy + 1), (255, 255, 0))
		
		self.surface.blit(self.mapOverlay, (0,0))
		

