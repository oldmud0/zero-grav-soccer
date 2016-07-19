import os

from hud_element import HUDElement

class HUDArrowElement(HUDElement):
	
	path = os.path.join("res", "arrow.png")
	
	def __init__(self):
		super(HUDArrowElement, self).__init__(position)
	
	def action(self):
		# make it point to the ball!
		pass