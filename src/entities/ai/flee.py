'''
Created on 2013-05-25

@author: brian
'''

'''
Created on 2013-05-25

@author: brian
'''

class Flee(object):
    
    def __init__(self, actor):
        self.actor = actor
        self.target = None
        
    def condition(self):
        
        if float(self.actor.health) / self.actor.maxHealth > 0.2:
            return False
        
        self.target = None
        
        for entity in self.actor.getEnemies():
            if self.actor.canSee(entity.position):
                self.target = entity
        
        return self.target is not None
    
    def do(self):
        
        x = self.actor.position[0] - self.target.position[0] 
        y = self.actor.position[1] - self.target.position[1] 
        
        direction = (self.sign(x), 0) if abs(x) > abs(y) else (0, self.sign(y))
        alternative = (self.sign(x), 0) if abs(x) <= abs(y) else (0, self.sign(y))
        
        pos = self.actor.position
        
        if self.actor.world.isLocationPassable((pos[0] + direction[0], pos[1] + direction[1])):
            self.actor.move(direction)
        else:
            self.actor.move(alternative)
        
        
    @staticmethod
    def sign(n):
        return -1 if n < 0 else 1 
    
