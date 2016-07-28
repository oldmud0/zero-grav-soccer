import socket, codecs

class Server:
	"""Single-threaded listener.
	Making a server is tricky because there are possibilities
	left and right for malicious input.
	"""
	
	def __init__(self, gamemode, entities, map_path):
		"""Create socket with default options"""
		self.socket = socket.socket()
		self.socket.bind(("0.0.0.0", 27001))
		self.socket.listen(5)
		self.socket.setblocking(False)
		
		self.clients = set()
		
		self.gamemode = gamemode
		self.entities = entities
	
	def tick(self):
		# Accept a client if it is possible
		try:
			client, addr = self.socket.accept()
			client.auth = False
			self.clients.add(client)
		except BlockingIOError:
			pass
			
		# Receive data
		clients = set(self.clients) # copy to prevent removal errors
		for client in clients:
			try:
				data = client.recv(1024)
				
				# Check handshake packet
				if not client.auth and data[:3] == b"\x08\x80" and len(data) > 4:
					client.auth = True
					client.name = codecs.decode(data[3:], "utf-8")
					send_game_info(client)
				elif not client.auth:
					# Probably just internet noise. Drop the client.
					drop_client(client)
				# At this point, it's assumed that client.auth is True
				# Check join team packet
				elif codec
				if len(data) == 0:
					print("Connection with", client.raddr[0], "is closing.")
					self.drop_client(client)
				else:
					print(data)
			except socket.timeout:
				pass
			except BlockingIOError:
				pass
				
	def send_game_info(self, client):
		
	
	def drop_client(self, client):
		client.shutdown(socket.SHUT_RDWR)
		client.close()
		self.clients.remove(client)
	
	def shutdown(self):
		for client in self.clients:
			drop_client(client)
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()