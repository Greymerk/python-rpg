import time
import colorsys

class Color(object):


	@staticmethod
	def rainbow(r=None):
		if r is None:
			t = time.time()
			r = t - int(t)
		return colorsys.hls_to_rgb(r, 127, -1)
