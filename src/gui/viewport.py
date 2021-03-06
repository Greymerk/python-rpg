'''
Created on 2013-05-23

@author: brian
'''

import pygame
from pygame.color import THECOLORS
from src.util import Vector2
from cell import Cell

class Viewport(object):

	size = 17

	def __init__(self, surface, pos, world, player, images):
		self.images = images
		self.surface = surface
		self.pos = pos
		self.world = world
		self.player = player
		self.reticule = pygame.transform.scale2x(images.get("reticule"))
		self.grid = {}
		
		for x in range(Viewport.size):
			for y in range(Viewport.size):
				pos = Vector2(x * Cell.size, y * Cell.size)
				rel = Vector2(x - Viewport.size / 2, y - Viewport.size / 2)
				cell = Cell(pos, rel)
				cell.observers.append(player.targetcontrol)
				self.grid[(rel[0], rel[1])] = cell
	
	def display(self, info):
		self.fontobject = pygame.font.Font(None,24)
		for i, line in enumerate(info):
			self.surface.blit(self.fontobject.render(line[0], 1, (255,255,255)), (Cell.size / 2, (i + 1) * Cell.size / 2))	
		
	def draw(self):
		if(self.player.viewingMap):
			self.drawMap()
			return
			
		self.drawGame()

	
	def drawGame(self):
		self.surface.fill(THECOLORS["black"])
		camPos = self.player.party.getLeader().position

		for cell in self.grid.values():
			loc = Vector2(camPos)
			loc += cell.rel
			if not self.player.party.canSee(loc):
				continue
			tile = self.world.getTile(loc)
			ground = tile.getGround()
			imgName = ground.getImage(loc)
			image = self.images.get(imgName, loc)
			self.surface.blit(image, (int(cell.pos[0]), int(cell.pos[1])))			

		for e in self.world.getAllEntities():
			e.draw(self.surface, camPos, self.images, self.visible)
		
		if self.player.action is not None:
			if hasattr(self.player.action, 'location'):
				if self.player.action.location is not None:
					'''
					x = 32 * (8 + self.player.action.location[0])
					y = 32 * (8 + self.player.action.location[1])
					'''
					cell = self.grid[self.player.action.location]
					self.surface.blit(self.reticule, cell.pos)

		if self.player.reticle is not None and self.player.action is not None:
			r = Vector2(self.player.reticle)
			r += (8, 8)
			self.surface.blit(self.reticule, (r[0] * 32, r[1] * 32))


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
					
		for mob in self.world.mobManager.mobs:
			self.map_dot(mob.position, THECOLORS["red"])
			
		for e in self.world.friendly:
			self.map_dot(e.position, THECOLORS["azure"])
			
		leader = self.player.party.getLeader()
		self.map_dot(leader.position, THECOLORS["yellow"])		
		
	def visible(self, pos):			
		return self.player.party.canSee(pos)
		
	def notify(self, pos, event):
		vec = Vector2(pos)
		vec -= self.pos
		rel = (int(vec[0] / 32) - 8, int(vec[1] / 32) - 8)
		self.grid[rel].notify(event)
		
	def map_dot(self, pos, color):
		x, y = self.player.party.getLeader().position
		origin = (int(x) >> 4) - 8, (int(y) >> 4) - 8
		cpos = int(pos[0]) >> 4, int(pos[1]) >> 4
		posx = int(((cpos[0] - origin[0]) * 32) + ((pos[0] % 16) * 2))
		posy = int(((cpos[1] - origin[1]) * 32) + ((pos[1] % 16) * 2))
			
		self.surface.set_at((posx, posy), color)
		self.surface.set_at((posx, posy + 1), color)
		self.surface.set_at((posx + 1, posy), color)
		self.surface.set_at((posx + 1, posy + 1), color)

