'''
Created on 2013-05-29

@author: brian
'''

class Fallback(object):
    
    def __init__(self, actor):
        self.actor = actor
        self.target = None
        
    def condition(self):
        
        self.target = None
        
        for entity in self.actor.getEnemies():
            if self.actor.distance(entity.position) < 3:
                self.target = entity
        
        if self.target is None:
            return False
        
        x = self.actor.position[0] - self.target.position[0] 
        y = self.actor.position[1] - self.target.position[1] 
        
        direction = (self.sign(x), 0) if abs(x) > abs(y) else (0, self.sign(y))
        alternative = (self.sign(x), 0) if abs(x) <= abs(y) else (0, self.sign(y))
        
        pos = self.actor.position
        
        if self.actor.world.isLocationPassable((pos[0] + direction[0], pos[1] + direction[1])):
            self.direction = direction
            return True
        
        elif self.actor.world.isLocationPassable((pos[0] + alternative[0], pos[1] + alternative[1])):
            self.direction = alternative
            return True
        
        return False
        
        
    
    def do(self):
        self.actor.move(self.direction)
        
    @staticmethod
    def sign(n):
        return -1 if n < 0 else 1 
    
