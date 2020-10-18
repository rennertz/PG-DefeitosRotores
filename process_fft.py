import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy.signal import periodogram

def extract_features(file_adress):
	# reduz o samplig frequency 'ratio' vezes, tomando apenas 1 a cada 'ratio' sinais
	ratio = 50
	sampling_freq=50000/ratio # a ser usado no fft
	skip=[i for i in range(0,250000) if i%ratio] # poupa apenas as linhas múltiplas de 'ratio'
												 # e lista as demais para exclusão

	signals = pd.read_csv(file_adress, header=None, 
                      	  names=['tachometer','ac1rad','ac1ax','ac1tg','ac2rad','ac2ax','ac2tg','microphone'],
                      	  skiprows=skip)

	# produz o FFT para cada sinal
	signals_fft = signals.apply(np.fft.rfft, axis=0) # sinal real, logo rfft representa 
													 # apenas metade da transformada
	signals_fft = signals_fft.apply(np.abs) # Obtém valor absoluto a partir dos complexos

	# gera o eixo da frequência, dado que a frequência de Nyquist é sampling_freq/2
	signals_fft['freq_ax'] = np.linspace(0, sampling_freq/2+1, signals_fft.shape[0]) 


	# agora geramos as features, começando pela fundamental
	fundamental = extract_fundamental(signals_fft)
	features = {'fundamental': fundamental}


	# extraimos o index da fundamental
	index = signals_fft.index[signals_fft['freq_ax'] == fundamental]

	# extrímos todos os valores nas três primeiros harmônicos, exceto para o tacômetro e freq_ax
	first_h = signals_fft.iloc[index].to_dict('records')[0]
	secnd_h = signals_fft.iloc[2*index].to_dict('records')[0]
	third_h = signals_fft.iloc[3*index].to_dict('records')[0]
	first_h.pop('tachometer')
	secnd_h.pop('tachometer')
	third_h.pop('tachometer')
	first_h.pop('freq_ax')
	secnd_h.pop('freq_ax')
	third_h.pop('freq_ax')

	# adicionamos um sulfixo para os valores correspondentes a cada harmônico e ADICIONAMOS às features
	features.update({k+'_1h': v for k, v in first_h.items()})
	features.update({k+'_2h': v for k, v in secnd_h.items()})
	features.update({k+'_3h': v for k, v in third_h.items()})

	return features


def extract_fundamental(fft_df):
	# dentre os 3 maiores picos na fft do tacômetro, deve retornar o de menor frequência
	# assim, evita-se o mascaramento da fundamental pelas harmonicas

	candidates = [0, 0, 0]
	for i in range(3):
		index = fft_df['tachometer'].argmax()
		candidates[i] = fft_df.freq_ax[index]
		for j in range(-2,3):
			fft_df.tachometer[index+j] = 0

	return min(candidates)