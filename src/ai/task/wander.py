'''
Created on 2013-05-12

@author: brian
'''

from src.util import Cardinal

class Wander(object):
    
    def __init__(self, actor):
        self.actor = actor
        
    def condition(self):
        return True
    
    def do(self):
        
        direction = Cardinal.choice()
        self.actor.move(direction)
