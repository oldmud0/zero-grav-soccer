import socket

class Server:
	"""Single-threaded listener"""
	
	def __init__(self):
		"""Create socket with default options"""
		self.socket = socket.socket()
		self.socket.bind(("0.0.0.0", 27001))
		self.socket.listen(5)
		self.socket.setblocking(False)
		
		self.clients = set()
	
	def tick(self):
		# Accept a client if it is possible
		try:
			client, addr = self.socket.accept()
			self.clients.add(client)
		except BlockingIOError:
			pass
			
		# Receive data
		clients = set(self.clients) # copy to prevent removal errors
		for client in clients:
			try:
				data = client.recv(1024)
				if len(data) == 0:
					print("Connection with", client.raddr[0], "is closing.")
					client.shutdown(socket.SHUT_RDWR)
					client.close()
					self.clients.remove(client)
				else:
					print(data)
			except socket.timeout:
				pass
			except BlockingIOError:
				pass
	
	def shutdown(self):
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()