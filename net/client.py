import socket

class Client:
	
	def __init__(self, address, port):
		self.socket = socket.socket()
		self.socket.connect((address, port))
		self.socket.setblocking(False)
		
	def tick(self):
		try:
			data = self.socket.recv(1024)
			
			if len(data) == 0:
				print("Connection is closing.")
				self.shutdown()
		except socket.timeout:
			pass
		except BlockingIOError:
			pass
		
	def send(self, data):
		try:
			self.socket.sendall(data)
		except socket.timeout:
			self.shutdown()
	
	def shutdown(self):
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()
