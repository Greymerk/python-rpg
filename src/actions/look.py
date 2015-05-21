'''
Created on 2013-05-02

@author: brian
'''

import pygame
from pygame.locals import *
from cardinals import cardinals

class Look:
    
    def __init__(self, player):
        self.player = player
        self.finished = False
        self.player.log.append('Look... (Choose a direction)')

    def nextStep(self):
                
        e = pygame.event.poll()

        if e is None:
            return False

        if e.type != KEYDOWN:
            return False
            
        if(e.key in cardinals.keys()):
            
            direction = cardinals[e.key]
            x = self.player.party.getLeader().position[0] + direction[0]
            y = self.player.party.getLeader().position[1] + direction[1]
            pos = (x, y)
            result = self.player.world.look(pos)
            self.player.log.append('Thou dost see ' + result)
            return True
        elif(e.key == K_ESCAPE):
            self.player.log.append('Pass')
            return True
        
        return False
