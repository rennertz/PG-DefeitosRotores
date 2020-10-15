import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy.signal import periodogram

def extract_features(file_adress):
	# reduz o samplig frequency 'ratio' vezes, tomando apenas 1 a cada 'ratio' sinais
	ratio = 50
	sampling_freq=50000/ratio # a ser usado no fft
	skip=[i for i in range(0,250000) if i%ratio] # poupa apenas as linhas múltiplas de 'ratio' e lista as demais para exclusão

	signals = pd.read_csv(file_adress, header=None, 
                      	  names=['ac1rad','ac1ax','ac1tg','ac2rad','ac2ax','ac2tg','tachometer','microphone'],
                      	  skiprows=skip)

	complex_fft = np.fft.rfft(signals['tachometer'])
	real_fft = np.abs(complex_fft)
	freq_axis = np.linspace(0, sampling_freq/2+1, len(real_fft)) # a frequência de Nyquist é sampling_freq/2
	fundamental = freq_axis[real_fft.argmax()]

	return {'fundamental': fundamental}