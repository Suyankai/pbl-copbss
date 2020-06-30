from scipy.io import wavfile
import numpy as np

ii=0
length=20
halb_length=length//2
frequency=16000

for i in range(0,10):
    print(i)
    temp_wav = wavfile.read('wav/'+str(i)+'.wav')[1]
    wav_length = len(temp_wav)
    if wav_length > frequency*length:
        mid = wav_length // 2
        temp_wav = temp_wav[mid-halb_length*frequency:mid+halb_length*frequency]
        wavfile.write('16000_wavs/'+str(ii)+'.wav',frequency,temp_wav)
        ii+=1