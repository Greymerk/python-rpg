from attack import Attack
from bowshot import *
from magicmissile import *
from chainbolt import ChainBolt
from poisonbolt import PoisonBolt
from healbolt import HealBolt
from resurrection import Resurrection
from explosion import Explosion

class Ability(object):

	lookup = {}
	lookup["Attack"] = Attack
	lookup["BowShot"] = BowShot
	lookup["MagicMissile"] = MagicMissile
	lookup["PoisonBolt"] = PoisonBolt
	lookup["ChainBolt"] = ChainBolt
	lookup["FireBall"] = FireBall
	lookup["HealBolt"] = HealBolt
	lookup["Resurrection"] = Resurrection
	lookup["Explosion"] = Explosion

	def __init__(self, unit, ability=None):
		self.caster = unit
		self.ability = ability
		self.observers = []

	def notify(self, event):
		for obs in self.observers:
			obs.notify(self, event)
			
	def valid(self, entity):
		
		if not self.caster.canHit(entity.position, self.ability.range):
			return False
			
		if not self.ability.validTarget(self.caster, entity):
			return False
			
		return True
			
	def inRange(self, target):
		return self.caster.canHit(target, self.ability.range)
		
	def cast(self, target):
		return self.ability(self.caster, target, self.ability)
			
	def draw(self, images, surface):
		image = images.get(self.ability.icon)
		surface.blit(image, surface.get_rect())
	
	def save(self):
		data = {}
		data['ability'] = self.ability.__name__
		return data
		
	def load(self, data):
		ability = data['ability']
		self.ability = Ability.lookup[ability]
		

