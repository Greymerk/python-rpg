'''
Created on 2013-05-28

@author: brian
'''

from pygame.color import THECOLORS
from entities.projectiles import Arrow
from random import randint

class BowShot(object):
    
    color = THECOLORS['chocolate'] 
    heal = False
        
    def __init__(self, caster, location):
        self.caster = caster
        self.target = location
        
        self.weapon = caster.inventory.weapon
        self.range = self.weapon.range
        self.damage = self.weapon.damage
        casterName = self.caster.getName()
        
        self.entityHit = self.caster.world.getEntityFromLocation(self.target)
        if not self.entityHit is None:
            targetName = self.entityHit.getName()
            self.caster.world.log.append(casterName + ' shot ' + targetName + ' with a ' + self.weapon.__class__.__name__)
        else:
            self.caster.world.log.append(casterName + ' shot nothing!')
        
        self.projectile = Arrow(caster.position, location, self.__class__.color, self.entityHit)
        self.done = False
     
    def update(self):
        self.projectile.update()
        if self.projectile.done:
            if not self.entityHit is None:
                self.entityHit.inflict(self.caster, randint(self.damage[0], self.damage[1]))
            self.done = True
            return True
        
        return False
        
    def draw(self, surface, position):
        if not self.done:
            self.projectile.draw(surface, position)

    def validTarget(self, actor, target):

        if not target.isAlive():
            return False

	if target in self.actor.getFriends():
            return False

	return True
    
class MagicBowShot(BowShot):
    
    color = THECOLORS['magenta']

    
