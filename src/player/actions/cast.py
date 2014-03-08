'''
Created on 2013-05-26

@author: brian
'''

import string

from cardinals import cardinals
import pygame

from pygame.locals import *
from entities.abilities import *

from entities.items import Spellbook
class Cast(object):
	 
    hotkeys = {}
    hotkeys[K_m] = MagicMissile
    hotkeys[K_f] = Fireball
    hotkeys[K_h] = HealBolt
    hotkeys[K_r] = Resurrection

      
    def __init__(self, player):
        self.player = player
        self.projectile = None
        self.casting = False
        self.targetLocation = None
        self.spell = None
        self.location = None
        
        if self.player.party.getLeader().inventory.offhand.__class__ is Spellbook:
            self.spellList = self.player.party.getLeader().inventory.offhand.spellList
        else:
            self.spellList = None
            self.player.log.append("Spellbook must be equipped to cast spells!")
	    return
        
        
        
        self.options = []
        self.options.append('Select a spell:')
	for i in Cast.hotkeys:
		if Cast.hotkeys[i] in self.spellList:
			key = string.upper(chr(i))
			self.options.append(key + ': ' + Cast.hotkeys[i].__name__)
        
    def nextStep(self):
        
        if self.spellList is None:
            return True
        
        if self.casting:
            if self.player.party.getLeader().spell is None:
                entity = self.player.world.getEntityFromLocation(self.targetLocation)
                if entity is None:
                    self.player.log.append('Nothing hit!')
                return True   
            return False
        
        e = pygame.event.poll()

        if e is None:
            return False

        if e.type != KEYDOWN:
            return False
        
        if e.key in [K_ESCAPE, K_SPACE]:
            self.player.log.append('Cancelled')
            return True
        
        if self.spell is None:
            if e.key in Cast.hotkeys.keys():
                spell = Cast.hotkeys[e.key]
                
                if not spell in self.spellList:
                    return False
                
                self.spell = spell
                
                self.location = (0,0)
                
                if self.player.lastTarget is not None:
                    if self.player.party.getLeader().canHit(self.player.lastTarget.position, Fireball.range) and self.player.lastTarget.isAlive():
                        self.location = self.player.lastTarget.position[0] - self.player.party.getLeader().position[0], self.player.lastTarget.position[1] - self.player.party.getLeader().position[1]    
            return False
        

        if self.location != (0,0) and e.key in [K_RETURN, K_c]:
            pos = self.player.party.getLeader().position
            target = (pos[0] + self.location[0], pos[1] + self.location[1])   
            self.player.party.getLeader().cast(self.spell, target)
            self.targetLocation = target
            entity = self.player.world.getEntityFromLocation(target)
            if entity is not None:
                self.player.lastTarget = entity
            self.casting = True
            return False
        
        if e.key in cardinals.keys():
            pos = self.player.party.getLeader().position
            direction = cardinals[e.key]
            newLocation = pos[0] + self.location[0] + direction[0], pos[1] + self.location[1] + direction[1]
            if not self.player.party.getLeader().canHit(newLocation, self.spell.range):
                return False
            self.location = self.location[0] + direction[0], self.location[1] + direction[1]
            return False
            
        return False
    
    
