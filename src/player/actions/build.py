'''
Created on 2013-05-02

@author: brian
'''


import pygame
#from terrain import terrain
from pygame.locals import *
from cardinals import cardinals

class Build:

    def __init__(self, player):
        self.player = player
        self.direction = None
        self.finished = False
        self.player.log.append('Build... (Choose a direction)')
        self.choices = {}
        #self.choices[K_c] = terrain.WallStone.id
        #self.choices[K_f] = terrain.FloorBrick.id
        self.choice = None
                
    def nextStep(self):

        if(self.choice is not None):
            x = self.player.party.getLeader().position[0] + self.direction[0]
            y = self.player.party.getLeader().position[1] + self.direction[1]
            tile = self.player.world.getTile((x, y))
            if(tile.isPassable()):
                self.player.world.build((x, y), self.choices[self.choice])
                #self.player.log.append('Successfully placed ' + terrain.lookup[self.choices[self.choice]].singular)
            else:
                self.player.log.append('Cannot build on ' + tile.getName())
                    
            return True
                
        e = pygame.event.poll()

        if e is None:
            return False

        if e.type != KEYDOWN:
            return False

        if(self.direction is not None):
            if(self.choices.has_key(e.key)):
                self.choice = e.key
            
            return False
    
        if(e.key in cardinals.keys()):
            self.direction = cardinals[e.key]
            self.player.log.append('Build... (Choose a block)')
            self.options = []
            self.options.append('Build Options:')
            self.options.append('c: cobblestone')
            self.options.append('f: floor')
            return False
        elif(e.key == K_ESCAPE):
            self.player.log.append('Cancelled')
            return True
        if(self.direction is None):
        
            if(e.key in cardinals.keys()):
                self.direction = cardinals[e.key]
                return False
            elif(e.key == K_ESCAPE):
                self.player.log.append('Cancelled')
                return True
                        
        return False
    
