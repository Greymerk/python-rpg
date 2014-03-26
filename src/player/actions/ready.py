'''
Created on 2013-06-04

@author: brian
'''

import pygame
from pygame.locals import *


class Ready(object):
    
    def __init__(self, player):
        self.player = player
        self.player.log.append('Ready a new weapon')
              
                
    def nextStep(self):

        if(self.choice is not None):
            self.player.party.getLeader().inventory.weapon = self.choices[self.choice]()
            self.player.log.append('Equipped a ' + self.player.party.getLeader().inventory.weapon.__class__.__name__)                 
            return True
                
        e = pygame.event.poll()

        if e is None:
            return False

        if e.type != KEYDOWN:
            return False
        
        if(self.choices.has_key(e.key)):
            self.choice = e.key
        
            return False
    
        elif(e.key == K_ESCAPE):
            self.player.log.append('Cancelled')
            return True
                        
        return False
    
