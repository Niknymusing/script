import pyaudio
import wave
 
FORMAT = pyaudio.paInt16
CHANNELS = 2
SAMPLE_RATE = 44100
FRAMES_PERBUFF = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
 
audio = pyaudio.PyAudio()
info = pyaudio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
            if (pyaudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", pyaudio.get_device_info_by_host_api_device_index(0, i).get('name'))

stream = pyaudio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=FRAMES_PERBUFF,
                    input_device_index=1) #see output of available audio devices to select one.
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=SAMPLE_RATE, input=True,
                frames_per_buffer=FRAMES_PERBUFF)
print("recording...")
frames = []
 
for i in range(0, int(SAMPLE_RATE / FRAMES_PERBUFF * RECORD_SECONDS)):
    data = stream.read(FRAMES_PERBUFF)
    frames.append(data)
print("finished recording")
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(SAMPLE_RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()