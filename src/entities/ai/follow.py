'''
Created on 2013-05-25

@author: brian
'''

class Follow(object):
    
    def __init__(self, actor, classList = []):
        self.actor = actor
        self.classList = classList
        self.target = None
        
    def condition(self):
        
        self.target = None
        
        leader = self.actor.getLeader()
        if leader is not None:
            if self.actor.distance(leader.position) > 3:
                self.target = leader
        else:
            for entity in list(set(self.actor.world.friendly) | set(self.actor.world.mobManager.mobs)):
                if len(self.classList) == 0 or entity.__class__ in self.classList:
                    if self.actor.canSee(entity.position):
                        if self.actor.distance(entity.position) > 3:
                            self.target = entity
                    
        return self.target is not None
    
    def do(self):
        
        x = self.target.position[0] - self.actor.position[0]
        y = self.target.position[1] - self.actor.position[1]
        
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
    
