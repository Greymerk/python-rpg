'''
Created on 2013-05-26

@author: brian
'''

import entities

class Party(object):
    
    def __init__(self, player):
        
        self.player = player
        self.members = []
        self.leader = 0   
        
    def add(self, entity):
        self.members.append(entity)
        entity.setGroup(self)
        
    def save(self):
        
        data = {}
        
        members = []
        for e in self.members:
            members.append(e.save())
        data['members'] = members
        
        data['leader'] = self.leader
        
        return data
        
    def setLeader(self, index):
               
        if not index in range(len(self.members)):
            return
        
        self.members[self.leader].ai.active = True    
        self.leader = index
        self.members[self.leader].ai.active = False
        self.player.log.append(self.members[self.leader].getName() + " is now the leader.")
        
    def load(self, data):
        
        members = data['members']
        
        for e in members:
            etype = e['type']
            member = entities.lookup[etype](self.player.world)
            member.load(e)
            self.members.append(member)
            member.setGroup(self)
            
        self.leader = data['leader']
            
    def getLeader(self):
        return self.members[self.leader]
    

    def canSee(self, position):

	for e in self.members:
            if e.canSee(position):
                return True

	return False        
        
