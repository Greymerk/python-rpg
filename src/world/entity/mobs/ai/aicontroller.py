'''
Created on 2013-05-12

@author: brian
'''

import task

class AIController(object):

	tasks = task

	def __init__(self):
		self.aiList = []
		self.active = True
	   
	def act(self):

		if not self.active:
			return

		for ai in self.aiList:
			
			if(ai.condition()):
				ai.do()
				return   
		
	def addAI(self, ai):
		self.aiList.append(ai)
		
	def save(self):
		
		data = {}
		data['active'] = self.active
		
		return data
	
	def load(self, data):
		
		self.active = data['active']
	