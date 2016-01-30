def get(pos):
	images = []
	images.append("brush")
	images.append("forest")
	images.append("jungle")
	n = int(pos[0]) | int(pos[1])
	i = n % len(images) 
	return images[i]+'.png'

