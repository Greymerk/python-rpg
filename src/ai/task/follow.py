'''
Created on 2013-05-25

@author: brian
'''

from src.util import Vector2

class Follow(object):
    
    def __init__(self, actor):
        self.actor = actor
        self.target = None
        
    def condition(self):
        
        self.target = None
        
        leader = self.actor.getLeader()
        if leader is not None:
            if self.actor.distance(leader.position) > 3:
                self.target = leader
        else:
            pass #TODO: Follow leader mob type 
        
        return self.target is not None
	
    def do(self):
        
        x = self.target.position[0] - self.actor.position[0]
        y = self.target.position[1] - self.actor.position[1]
        
        direction = (self.sign(x), 0) if abs(x) > abs(y) else (0, self.sign(y))
        alternative = (self.sign(x), 0) if abs(x) <= abs(y) else (0, self.sign(y))
        
        pos = self.actor.position
        
        if self.actor.world.isLocationPassable(Vector2(int(pos[0] + direction[0]), int(pos[1] + direction[1]))):
            self.actor.move(direction)
        else:
            self.actor.move(alternative)
        
        
    @staticmethod
    def sign(n):
        return -1 if n < 0 else 1 
    
