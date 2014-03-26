'''
Created on 2013-06-01

@author: brian
'''

class Inventory(object):
    
    def __init__(self, owner, itemList):
        self.bar = [None] * 8
        self.owner = owner
        self.itemList = itemList
        
        
    def getAction(self):

        if len(self.bar) == 0:
            return None
        
        for item in self.bar:
            
            if item is None:
                continue
            
            for e in self.owner.world.getAllEntities():
                
                if not item.ability.validTarget(self.owner, e):
                    continue
                
                if not self.owner.canHit(e.position, item.range):
                    continue

                return item.ability(self.owner, e.position, item) #ability instance
    
    def load(self, data):
        if 'bar' in data.keys():
            bar = data['bar']
            for i in range(len(bar)):
                if bar[i] is None:
                    self.bar[i] = None
                else:
                    self.bar[i] = self.loadItem(bar[i])
        
    def save(self):
        data = {}
        bar = []
        for i in self.bar:
            if i is None:
                bar.append(None)
            else:
                bar.append(i.save())
        data['bar'] = bar
        return data
    
    def loadItem(self, data):
        itemType = data['type']
        
        o = self.itemList[itemType]()
        o.load(data)
        return o
