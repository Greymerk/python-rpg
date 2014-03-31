'''
Created on 2013-06-05

@author: brian
'''

class Item(object):

    def __init__(self):
        pass
    
    def load(self, data):
        pass 
    
    def save(self):
        data = {}
        data['type'] = self.__class__.__name__
                
        return data