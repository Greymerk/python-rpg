'''
Created on 2013-06-01

@author: brian
'''

from entities.items import itemList

from barehands import BareHands
from weapon import Weapon
from offhand import Offhand

class Inventory(object):
    
    def __init__(self):
        self.weapon = None
        self.offhand = None        
        
    def getWeapon(self):
        
        if self.weapon is None:
            return BareHands()
        
        return self.weapon
    
    def getInventory(self):
        pass
    
    
    def load(self, data):
        if 'weapon' in data.keys():
            self.weapon = Inventory.loadItem(data['weapon'])
        if 'offhand' in data.keys():
            self.offhand = Inventory.loadItem(data['offhand']) 
        
        
    def save(self):
        data = {}
        if self.weapon is not None:
            data['weapon'] = self.weapon.save()
        if self.offhand is not None:
            data['offhand'] = self.offhand.save()
        
        return data
    
    @staticmethod
    def loadItem(data):
        itemType = data['type']
        
        o = itemList[itemType]()
        o.load(data)
        return o
