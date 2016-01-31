from time import time
from random import Random

def get(pos):
	p = int(pos[0]) | int(pos[1])
	t = time()
	rand = Random(int(t * 2) + p)
	n = rand.randint(0, 10)
	n += p
	return 'priest' + str(n % 4) + '.png'

