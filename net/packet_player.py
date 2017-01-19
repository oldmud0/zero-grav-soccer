import codecs

from packet_entity import EntityPacket

class PlayerPacket(EntityPacket):
	id = 3
	size = 25
	
	def encode():
		pass
	
	def decode(data):
		ent_data = super(PlayerPacket).decode(data)
		ply_data = struct.unpack("b", data[-1:])
		
		ply_data_unpacked = [bool(ply_data & (1 << n)) for n in range(4)]
		
		return ent_data + ply_data_unpacked