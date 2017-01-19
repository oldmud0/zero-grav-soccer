class Packet:
	"""Pseudo-abstract class for holding a sendable/receivable packet"""
	
	id = None
	size = 0
	
	def encode():
		pass
	def decode(data):
		pass