import pyaudio


def get_streamer(callback, chunk):
	""" initialize a new streamer """
	def inner_callback(in_data, frame_count, time_info, status):
		callback(in_data)
		return (None, pyaudio.paContinue)

	audio = pyaudio.PyAudio()
	stream = audio.open(format=pyaudio.paInt16, channels=1,
						rate=44100, input=True, frames_per_buffer=chunk,
						stream_callback=inner_callback)
	return stream

def get_player():
	""" initialize a new player """
	audio = pyaudio.PyAudio()
	stream = audio.open(format = pyaudio.paInt16, channels=1,
				rate = 44100, output = True)
	return stream

def split(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]

