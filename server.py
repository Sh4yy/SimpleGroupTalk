import socket
import select
import struct


class Streamer:

	def __init__(self, port, ip, CHUNK_SIZE=1024):
		""" initialize a new streamer """
		
		self.CHUNK_SIZE = CHUNK_SIZE

		# initalize the socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((port, ip))
		self.sock.listen()
		self.sock.setblocking(False)

		# create a list of input/output sockets
		self.inputs = [self.sock]
		self.outputs = []
		self.usernames = {}

	def _get_username(self, sock):
		""" get username from sock """

		try:
			len_data = sock.recv(4)
			if not len_data: return self._close(sock)
			head_len = struct.unpack('!i', len_data)[0]
			user_data = sock.recv(head_len)
			if not len: return self._close(sock)
			username = user_data.decode()
			return username
		except Exception as e:
			print(f"Get username failed {e}")

	def _accept(self, sock):
		""" socket is receiving a new connection """
		connection, addr = sock.accept()
		connection.setblocking(False)
		## process user name
		username = self._get_username(connection)
		if not username: return

		self.usernames[connection] = username
		self.inputs.append(connection)
		print(f'New connection {username} {addr[0]}:{addr[1]}')

	def _broadcast(self, sock, data):
		""" broadcast the input data """

		username = self.usernames[sock]
		head_len = struct.pack('!i', len(username))
		user_data = head_len + username.encode()
		payload = user_data + data

		for recp in self.inputs:
			try:
				if recp is sock or recp is self.sock:
					continue
				recp.send(payload)
			except Exception as e:
				print(f'Broadcast failed {e}')

	def _close(self, sock):
		""" close and remove a given socket """
		if sock in self.inputs:
			self.inputs.remove(sock)
		if sock in self.outputs:
			self.outputs.remove(sock)
		if sock in self.usernames:
			username = self.usernames[sock]
			del self.usernames[sock]
			print(f'Closed connection {username}')
		sock.close()

	def _read(self, sock):
		""" socket is ready to read """
		data = sock.recv(self.CHUNK_SIZE)
		if not data:
			return self._close(sock)

		self._broadcast(sock, data)

	def _process(self):
		""" process a loop """
		read_sock, _, _ = select.select(self.inputs, [], self.inputs)
		for read in read_sock:

			if read is self.sock:
				self._accept(read)
			else:
				self._read(read) 

	def serve(self, forever=True):
		""" start serving the server """
		if not forever:
			self._process()
			return

		while True:
			self._process()


def main():

	PORT, IP = "0.0.0.0", 12345
	streamer = Streamer(PORT, IP, CHUNK_SIZE=1024)
	streamer.serve(forever=True)


if __name__ == '__main__':
	main()

