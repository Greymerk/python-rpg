

class Ability(object):

	def __init__(self, unit, ability):
		self.caster = unit
		self.ability = ability
		self.observers = []

	def notify(self, event):
		for obs in self.observers:
			obs.notify(self, event)
