from time import time

def get(pos):
	images = []
	images.append("fighter.png")
	images.append("fighter2.png")
	n = int(pos[0]) * int(pos[1])
	n += int(time())
	i = n % len(images) 
	return images[i]

