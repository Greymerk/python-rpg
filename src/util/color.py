import time
import colorsys

class Color(object):


	@staticmethod
	def rainbow():
		t = time.time()
		r = t - int(t)
		return colorsys.hls_to_rgb(r, 127, -1)
