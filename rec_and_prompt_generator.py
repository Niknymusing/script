import os
import time
import pyaudio
import wave
import tempfile
from playsound import playsound
import numpy as np


rec_time = 5

genres_text_file = "music_genres.txt"
audio_events_text_file = "audio_events.txt"

f = open(genres_text_file , "r")
string1 = f.read()
g = open(audio_events_text_file , "r")
string2 = g.read()
list_of_audio_events = string1.split(',')
list_of_music_genres = string2.split(',')

print(list_of_audio_events)
print(list_of_music_genres)

frames_per_segment = 10
number_of_segments = 30

frame_promtps = {}

scene_embeddings = []

style_embeddings = []

mood_embeddings = []

actors_embeddings = []


def rec_audio(length):

    RECORD_SECONDS = length or 10
    FRAMES_PERBUFF = 2048 
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1 
    SAMPLE_RATE = 44100
    
    p = pyaudio.PyAudio()

    #available audio devices
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=FRAMES_PERBUFF,
                    input_device_index=1) #see output of available audio devices to select one.

    print("* recording started")
    

    frames = []
    nchunks = int(RECORD_SECONDS * SAMPLE_RATE / FRAMES_PERBUFF)
    for i in range(0, nchunks):
        data = stream.read(FRAMES_PERBUFF)
        data = np.frombuffer(data, 'float32')
        frames.append(data) 
    print(len(frames))

    #saving numpy array
    numpydata = np.hstack(frames)

    stream.stop_stream()
    stream.close()
    p.terminate()

    #saving audio file
    wf = wave.open('audio_sample.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return numpydata


frames = rec_audio(rec_time)

print(frames)