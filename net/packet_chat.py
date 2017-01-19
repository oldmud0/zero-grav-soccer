import codecs

from packet import Packet

class ChatPacket(Packet):
	id = 5
	size = 512
	
	def encode():
		pass
	
	def decode(data):
		return codecs.decode(data[2:], "utf-8")