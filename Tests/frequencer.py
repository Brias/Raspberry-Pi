import subprocess as sp
import pyaudio
import numpy

command = [FFMPEG_BIN,
        '-i', 'mySong.mp3',
        '-f', 's16le',
        '-acodec', 'pcm_s16le',
        '-ar', '44100',  # ouput will have 44100 Hz
        '-ac', '2',  # stereo (set to '1' for mono)
        '-']

pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)

raw_audio = pipe.proc.stdout.read(88200*4)

# Reorganize raw_audio as a Numpy array with two-columns (1 per channel)

audio_array = numpy.fromstring(raw_audio, dtype="int16")
audio_array = audio_array.reshape((len(audio_array)/2, 2))