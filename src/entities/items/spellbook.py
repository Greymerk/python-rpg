'''
Created on 2013-06-05

@author: brian
'''

from offhand import Offhand

class Spellbook(Offhand):

    def __init__(self):
        self.spellList = []
        
    def remove(self, index):
        if not index in range(len(self.spellList)):
            return
        
        spell = self.spellLIst.pop(index)
        return spell
    
    def add(self, spell):
        
        for s in self.spellList:
            if s.__class__ == spell.__class__:
                return False
            
        self.spellList.append(spell)
        return True
    
    def save(self):
        data = {}
        data['type'] = self.__class__.__name__
        data['spellList'] = self.spellList
        return data
    
    def load(self, data):
        if 'spellList' in data.keys():
            self.spellList = data['spellList']
    
        