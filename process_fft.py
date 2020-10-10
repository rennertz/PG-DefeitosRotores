import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# TODO: avaliar se vale a pena reduzir a taxa de amostragem já no pd.read_csv
# 		utilizando o atributo skiprows=list(range(0, 250000, 10)

#def extract_fft_from_file(file_adress)

signals = pd.read_csv('mafaulda/horizontal-misalignment/0.5mm/12.288.csv', header=None, 
	names=['ac1rad','ac1ax','ac1tg','ac2rad','ac2ax','ac2tg','tachometer','microphone'])
# um data frame com shape (250000, 8)

# reduz o samplig frequency de 50kHz para 10kHz
signals = signals.iloc[[5*i for i in range(round(250000/5))],:]
fft = np.fft.rfft(signals['ac1rad'])

plt.plot(np.abs(fft))
plt.show()