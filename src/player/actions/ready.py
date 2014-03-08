'''
Created on 2013-06-04

@author: brian
'''

import pygame
from pygame.locals import *
from entities.items import *

class Ready(object):
    
    def __init__(self, player):
        self.player = player
        self.player.log.append('Ready a new weapon')
        self.choices = {}
        self.choices[K_s] = ShortSword
        self.choices[K_n] = LongSword
        self.choices[K_g] = MagicSword
        self.choices[K_b] = ShortBow
        self.choices[K_l] = LongBow
        self.choices[K_m] = MagicBow
        self.choices[K_t] = Staff
        self.choice = None
        
        self.options = []
        self.options.append('Available Weapons:')
        self.options.append('S: ShortSword')
        self.options.append('N: LongSword')
        self.options.append('G: MagicSword')
        self.options.append('B: ShortBow')
        self.options.append('L: LongBow')
        self.options.append('M: MagicBow')
        self.options.append('T: Staff')
            
        
                
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
    
