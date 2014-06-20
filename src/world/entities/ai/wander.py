'''
Created on 2013-05-12

@author: brian
'''

from random import choice

class Wander(object):
    
    def __init__(self, actor):
        self.actor = actor
        
    def condition(self):
        return True
    
    def do(self):
        
        direction = choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        self.actor.move(direction)