'''
Created on 2013-05-27

@author: brian
'''

class Cast(object):

	def __init__(self, actor):
		
		self.actor = actor
		
	def condition(self):

		result = self.actor.getAction()
		if result is None:
			return False
			
		self.actor.action = result
		return True

	def do(self):
		pass

