'''
Created on 2013-05-27

@author: brian
'''

class Cast(object):

    def __init__(self, actor):
        
        self.actor = actor
        self.action = None
        
    def condition(self):

        result = self.actor.inventory.getAction()
        if not result is None:
            self.action = result 
            return True
                
        return False
    
    def do(self):
        
        self.actor.action = self.action
        
