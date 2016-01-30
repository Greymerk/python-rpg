from time import time
from random import Random

def get(pos):
	images = []
	images.append("headless0.png")
	images.append("headless1.png")
	images.append("headless2.png")
	images.append("headless3.png")
	p = int(pos[0]) | int(pos[1])
	t = time()
	rand = Random(int(t * 2) + p)
	n = rand.randint(0, 10)
	n += p
	i = n % len(images) 
	return images[i]

