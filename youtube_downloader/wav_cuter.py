from scipy.io import wavfile
import numpy as np

ii=0
length=100
halb_length=length//2
frequency=32000

for i in range(0,4):
    print(i)
    origin_wav = wavfile.read('wav/'+str(i)+'.wav')[1]
    wav_length = len(origin_wav)
    if wav_length > frequency*length:
        num_wav = min(100, wav_length//(frequency*length))
        for j in range(0, num_wav):
            temp_wav = origin_wav[j * wav_length//num_wav : j * wav_length//num_wav + length*frequency]
            wavfile.write('32000_wavs/'+str(ii)+'.wav', frequency, temp_wav)
            ii+=1
            print(ii)