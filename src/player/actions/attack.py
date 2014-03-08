'''
Created on 2013-05-25

@author: brian
'''
from cardinals import cardinals
import pygame
from pygame.locals import *
from math import sqrt

class Attack(object):

    def __init__(self, player):
        self.player = player
        self.player.log.append("Attack...")
        self.location = 0,0
        
        if self.player.lastTarget is not None:
            if self.player.party.getLeader().canHit(self.player.lastTarget.position):
                self.location = self.player.lastTarget.position[0] - self.player.party.getLeader().position[0], self.player.lastTarget.position[1] - self.player.party.getLeader().position[1]
        
    def nextStep(self):    
        
        e = pygame.event.poll()

        if e is None:
            return False

        if e.type != KEYDOWN:
            return False
        
        if self.location != (0,0) and e.key in [K_RETURN, K_a]:
            pos = self.player.party.getLeader().position
            location = (pos[0] + self.location[0], pos[1] + self.location[1])   
            self.player.party.getLeader().attack(location)

            self.player.lastTarget = self.player.world.getEntityFromLocation(location)
            return True
        
        if(e.key == K_ESCAPE):
            self.player.log.append('Cancelled')
            return True
        
        if e.key in cardinals.keys():
            pos = self.player.party.getLeader().position
            direction = cardinals[e.key]
            newLocation = pos[0] + self.location[0] + direction[0], pos[1] + self.location[1] + direction[1]
            if not self.player.party.getLeader().canHit(newLocation):
                return False
            self.location = self.location[0] + direction[0], self.location[1] + direction[1]
            return False
            
        return False
            