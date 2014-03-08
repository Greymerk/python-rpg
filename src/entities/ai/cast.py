'''
Created on 2013-05-27

@author: brian
'''

class Cast(object):

    def __init__(self, actor):
        
        self.actor = actor
        self.target = None
        self.selectedSpell = None
        
    def condition(self):
        
        spellList = self.actor.getSpellList()
        
        for spell in spellList:
        
            self.target = None

            for e in self.actor.world.getAllEntities():
                if spell.validTarget(self.actor, e):
                    self.selectedSpell = spell
                    self.target = e
                    return True
                
        return False
    
    def do(self):
        
        if self.target is None:
            return
        
        self.actor.cast(self.selectedSpell, self.target.position)
        
