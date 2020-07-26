from scipy.io import wavfile
import numpy as np

ii=0
length=20
half_length=length//2
frequency=48000

for i in range(0,46):
    print(i)
    temp_wav = wavfile.read('youtube_downloader/wav/'+str(i)+'.wav')[1]
    wav_length = len(temp_wav)
    if (wav_length > frequency * length):
        mid = wav_length // 2
        temp_wav = temp_wav[mid-half_length*frequency : mid+half_length*frequency]
        if (not np.isnan(temp_wav).any()) and (not np.isinf(temp_wav).any()):            
            wavfile.write('48000_wavs/'+str(ii)+'.wav', frequency, temp_wav)
            ii+=1