'''
Created on 2013-05-03

@author: brian
'''


import pygame

class Options(object):

    def __init__(self, surface, player):
        
        self.surface = surface
        self.player = player
        

        self.selected = 0
        self.player = player

        self.fontobject = pygame.font.Font(None,24)

    def draw(self):
        self.surface.fill((0,0,0))
        
        if not hasattr(self.player.action, 'options'):
            self.drawParty()
            return
        
        options = self.player.action.options
          
        count = 0
        for line in options:
            self.surface.blit(self.fontobject.render('>> ' + str(line) + ' - ' + str(options[line]), 1, (255,255,255)), (0, 16*count))
            count += 1

    def drawParty(self):
        count = 0
        for e in self.player.world.friendly:
            if count > self.getMaxLines():
                return
            if e.name is not None:
                name = e.name
            else:
                name = e.__class__.__name__
            message = name + ' - ' + str(e.health) + 'HP ' + '(' + str(e.position[0]) + ',' + str(e.position[1]) + ')'  
            self.surface.blit(self.fontobject.render(message, 1, (255,255,255)), (0, 16*count))
            count += 1
            
    def getMaxLines(self):
        return self.surface.get_height()/16
            
            