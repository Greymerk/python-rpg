from ability import Ability

from attack import Attack
from bowshot import *
from magicmissile import *
from chainbolt import ChainBolt
from poisonbolt import PoisonBolt
from healbolt import HealBolt
from resurrection import Resurrection
from explosion import Explosion

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
