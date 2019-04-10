from time import sleep
from queue import Queue
import socket
import struct
import select
from player import *
from threading import Thread
import os


class VoiceChat:

	def __init__(self, ip, port):
		""" initialize a new Voice Chat """
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.PORT_IP = (ip, port)
		self.data = Queue()
		self.speaking = False
		self.player = get_player()
		self.previous = None

	def connet(self, username):
		""" connect to the server """
		self.sock.connect(self.PORT_IP)

		# setup the username 
		head_len = struct.pack('!i', len(username))
		payload = head_len + username.encode()
		self.sock.send(payload)

	def send(self, data):
		""" send data to the server """
		assert len(data) <= 1024
		self.sock.send(data)

	def close(self):
		""" close connection """
		self.sock.close()

	def play(self, data):
		""" play chunk of data """
		self.player.write(data)

	def _get_username(self):
		""" get username from sock """

		try:
			len_data = self.sock.recv(4)
			if not len_data: return self.close(sock)
			head_len = struct.unpack('!i', len_data)[0]
			user_data = self.sock.recv(head_len)
			if not len: return self.close(sock)
			username = user_data.decode()
			return username
		except Exception as e:
			print(f"Get username failed {e}")

	def clear_ui(self):
		""" clear gui """
		os.system('cls' if os.name == 'nt' else 'clear')

	def recv(self):
		""" recieve data from the server """
		# 4 bytes for name len + 1024 bytes of data

		username = self._get_username()
		if not username: return self.close()
		data = self.sock.recv(1024)
		if not data: return self.close()

		if username != self.previous:
			self.clear_ui()
			self.previous = username
			print(f'Receiving voice from {username}')
		return data

	def broadcast(self, in_data):
		""" broadcast callback """

		if self.speaking:
			self.data.put(in_data)

	def set_talk(self, status):
		if status:
			self.speaking = True
			self.data = Queue()

		else:
			self.speaking = False
			self.data = Queue()
		self.previous = None
		self.clear_ui()

	def serve(self):
		""" start serving """

		def process():
			while True:
				read, write,  _ = select.select([self.sock], [self.sock], [self.sock])

				for sock in read:
					data = self.recv()
					self.play(data)

				for sock in write:
					while not self.data.empty():
							self.sock.send(self.data.get())	
		thread = Thread(target=process)
		thread.start()

def main():

	name = input("Enter your name ")
	voice = VoiceChat("0.0.0.0", 12345)
	voice.connet(name)
	streamer = get_streamer(voice.broadcast, 1024)
	streamer.start_stream()
	voice.serve()
	
	voice.set_talk(False)
	while True:
		if int(input()) == 1:
			voice.set_talk(True)
		else:
			voice.set_talk(False)


if __name__ == '__main__':
	main()