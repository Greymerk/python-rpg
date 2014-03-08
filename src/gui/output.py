import pygame

class Output(object):

	def __init__(self, surface, inBuffer):
		self.surface = surface
		self.buffer = inBuffer
		self.fontobject = pygame.font.Font(None,24)

	def draw(self):
		self.surface.fill((0,0,0))
		
		count = 0
		for line in self.buffer[-16:]:
			self.surface.blit(self.fontobject.render('>> ' + line, 1, (255,255,255)), (0, 16*count))
			count += 1	

	def append(self, message):
		self.buffer.append(message)
