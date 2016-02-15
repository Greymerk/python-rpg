

class Cell(object):

	def __init__(self, pos, rel):
		self.pos = pos
		self.rel = rel
		self.observers = []

	def notify(self, event):
		for obs in self.observers:
			obs.notify(self, event)

