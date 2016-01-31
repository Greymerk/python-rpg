import pygame

class Status(object):

	def __init__(self, surface, player, images):
		self.surface = surface
		self.player = player
		self.images = images
		self.font = pygame.font.Font(None,16)
		self.size = 32
		
	def draw(self):
		self.surface.fill((0,0,0))
		leader = self.player.avatar
		for i, ability in enumerate(leader.abilities):
			image = self.images.get(ability.icon)
			rect = pygame.Rect((i * self.size, 0),((i + 1) * self.size, self.size))
			self.surface.blit(image, rect)
			self.surface.blit(self.font.render(str(pygame.key.name(self.player.ABILITY_KEYS[i])).upper(), 1, (200,200,200)), (i * self.size,0)) 
