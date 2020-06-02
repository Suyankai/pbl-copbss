import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
from numpy.lib import stride_tricks
from PIL import Image, ImageDraw
import os
import stat
from pathlib import Path

file = open("audios/audios.txt","r") # Read all .wav file path
audio_path = (file.read()).split("\n")

def stft(sig, frameSize, overlapFac=0.5, window=np.hanning):
    win = window(frameSize)
    hopSize = int(frameSize - np.floor(overlapFac * frameSize))
    
    # zeros at beginning (thus center of 1st window should be for sample nr. 0)
    samples = np.append(np.zeros(int(np.floor(frameSize/2.0))), sig)    
    #cols for windowing
    ncols = np.ceil((len(samples) - frameSize) / float(hopSize)) +1
    # zeros at end (thus samples can be fully covered by frames)
    samples = np.append(samples, np.zeros(frameSize))
    
    frames = stride_tricks.as_strided(samples, shape=(int(ncols), frameSize), strides=(int(samples.strides[0]*int(hopSize)), int(samples.strides[0]))).copy()
    frames *= win
    
    return np.fft.rfft(frames)

def logscale_spec(spec, sr=44100, factor=20.):
    timebins, freqbins = np.shape(spec)

    scale = np.linspace(0, 1, freqbins) ** factor
    scale *= (freqbins-1)/max(scale)
    scale = np.unique(np.round(scale))
    
    # create spectrogram with new freq bins
    newspec = np.complex128(np.zeros([timebins, len(scale)]))
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            newspec[:,i] = np.sum(spec[:,int(scale[i]):], axis=1)
        else:        
            newspec[:,i] = np.sum(spec[:,int(scale[i]):int(scale[i+1])], axis=1)
    
    # list center freq of bins
    allfreqs = np.abs(np.fft.fftfreq(freqbins*2, 1./sr)[:freqbins+1])
    freqs = []
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            freqs += [np.mean(allfreqs[int(scale[i]):])]
        else:
            freqs += [np.mean(allfreqs[int(scale[i]):int(scale[i+1])])]
    
    return newspec, freqs

def plotstft(audiopath, binsize=2**10, plotpath="Spectograms/", colormap="jet"):
    #plotpath = os.fchmod(plotpath, stat.S_IWRITE)
    samplerate, samples = wav.read(audiopath)
    s = stft(samples, binsize)
    
    sshow, freq = logscale_spec(s, factor=1.0, sr=samplerate)
    ims = 20.*np.log10(np.abs(sshow)/10e-6) # amplitude to decibel
    
    timebins, freqbins = np.shape(ims)
    
    plt.figure(figsize=(15, 7.5))
    plt.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
    #plt.colorbar()

    #plt.xlabel("time (s)")
    #plt.ylabel("frequency (hz)")
    plt.xlim([0, timebins-1])
    plt.ylim([0, freqbins])

    xlocs = np.float32(np.linspace(0, timebins-1, 5))
    plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 10)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])
    
    if plotpath:
        plt.savefig(os.path.join(plotpath + i + '.png'), bbox_inches="tight")
    else:
        plt.show()
        
    plt.clf()



for i in audio_path:
    plotstft("audios/" + i)





#x , sr = librosa.load(audio_path)
	# print(type(x), type(sr))
	# librosa.load(audio_path, sr=44100)
#if we want to disable sampling librosa.load(audio_path, sr=none)

	#ipd.Audio(audio_path) #to display an audio

	#display waveform
	#%matplotlib inline
	
	#plt.figure(figsize=(14, 5))
	#librosa.display.waveplot(x, sr=sr)

	#display Spectrogram
	#X = librosa.stft(x)
	#Xdb = librosa.amplitude_to_db(abs(X))
	#plt.figure(figsize=(14, 5))
	#librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz') #If to pring log of frequencies  
	#librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log')
	#plt.colorbar()
	#img.save('/absolute/path/to/spectogram.jpg', 'JPEG')

