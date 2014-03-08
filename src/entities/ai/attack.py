'''
Created on 2013-05-25

@author: brian
'''



class Attack(object):
    
    def __init__(self, actor):
        self.actor = actor
        self.target = None
    
    def condition(self):
        
        if not self.actor.hostile:
            return False
        
        self.target = None
        self.target = self.actor.getAttackable()
        
        return self.target is not None
        
    def do(self):
        self.actor.attack(self.target.position)
        
             
        