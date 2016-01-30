from time import time

def get(pos):
	t = time() / 200 - int(time() / 200)
	t *= 600
	t = int(t)
	i = t % 15 
	return 'water' + str(15 - i) + '.png'

