from scipy.io import wavfile
import numpy as np

ii=0
length=10
halb_length=length//2
frequency=32000

for i in range(0,300):
    print(i)
    origin_wav = wavfile.read('youtube_downloader/wav/'+str(i)+'.wav')[1]
    wav_length = len(origin_wav)
    if wav_length > frequency * length:
        mid = wav_length // 2
        origin_wav = origin_wav[mid-halb_length*frequency : mid+halb_length*frequency]
        wavfile.write('32000_wavs/'+str(ii)+'.wav', frequency, origin_wav)
        ii+=1