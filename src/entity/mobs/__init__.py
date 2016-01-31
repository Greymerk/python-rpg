from orc import Orc
from rat import Rat
from snake import Snake
from spider import Spider
from headless import Headless
from ettin import Ettin
from fighter import Fighter
from mage import Mage
from bard import Bard
from priest import Priest
from skeleton import *

lookup = {}
lookup['Orc'] = Orc
lookup['Rat'] = Rat
lookup['Snake'] = Snake
lookup['Spider'] = Spider
lookup['Headless'] = Headless
lookup['Ettin'] = Ettin
lookup['Fighter'] = Fighter
lookup['Mage'] = Mage
lookup['Bard'] = Bard
lookup['Priest'] = Priest
lookup['SkeletalWarrior'] = SkeletalWarrior
lookup['SkeletalMage'] = SkeletalMage
lookup['SkeletalArcher'] = SkeletalArcher

hostiles = []
hostiles.append(Orc)
hostiles.append(Rat)
hostiles.append(Snake)
hostiles.append(Spider)
hostiles.append(Headless)
hostiles.append(Ettin)
hostiles.append(SkeletalWarrior)
hostiles.append(SkeletalMage)
hostiles.append(SkeletalArcher)
