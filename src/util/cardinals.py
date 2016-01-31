
from pygame.locals import *

cardinals = {}
cardinals[K_UP] =	(0,-1)
cardinals[K_DOWN] = 	( 0, 1)
cardinals[K_LEFT] = 	(-1, 0)
cardinals[K_RIGHT] = 	( 1, 0)
#cardinals[K_w] =	(0,-1)
#cardinals[K_s] = 	( 0, 1)
#cardinals[K_a] = 	(-1, 0)
#cardinals[K_d] = 	( 1, 0)

names = {}
names[K_UP] = "North"
names[K_DOWN] = "South"
names[K_LEFT] = "West"
names[K_RIGHT] = "East"
#names[K_w] = "North"
#names[K_s] = "South"
#names[K_a] = "West"
#names[K_d] = "East"