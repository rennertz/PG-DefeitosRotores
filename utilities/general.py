import pandas as pd
import numpy as np
from scipy.signal import decimate

RATIO = 10

def read_compressed_csv(file_path, ratio = RATIO):
    '''Realiza a leitura dos sinais reduzindo a frequência da aquisição 'ratio' vezes, 
    tomando apenas 1 a cada 'ratio' amostras temporais'''
 
    signals = pd.read_csv(
        file_path, 
        header=None,
        names=['tacometro', 'ax1', 'rad1', 'tg1','ax2', 'rad2', 'tg2', 'microfone'],
    )

    if ratio > 1:
            signals = signals.apply(decimate, axis=0, q=ratio)
    
    # reordena colunas
    return signals[['tacometro','microfone','ax1','ax2','rad1','rad2','tg1','tg2']]


def generate_fft(signals, ratio = RATIO):
    '''Gera o dataframe com a transformada rápida de fourrier 
    a partir do dataframe dos sinais no tempo'''

    # define nova frequência de aquisição. 
    sampling_freq = 50000/ratio
    # note: 50 kHz é a frequência de aquisição original dos dados 

    # produz a transformada de Fourrier para cada sinal real. 
    signals_fft = signals.apply(np.fft.rfft, axis=0, norm="ortho")
    # note: a rfft apresenta apenas a metade relevante da transformada, 
    # pois sinais reais produzem transformadas simétricas

    # obtém valor absoluto a partir da transformada complexa
    fft_amplitude = signals_fft.apply(np.abs)
    fft_phase = signals_fft.apply(np.angle)

    # gera o eixo da frequência, dado que a frequência de Nyquist é sampling_freq/2
    fft_amplitude['freq_ax'] = np.linspace(0, sampling_freq/2, 
                                           signals_fft.shape[0])
    fft_phase['freq_ax'] = fft_amplitude['freq_ax']
                                           

    return fft_amplitude, fft_phase


def save_file(file_path, df, truncate=False):
    '''(sobre-)Escreve um cvs com todos os dados'''
    
    with open(file_path, "w") as f:
        if truncate:
            df.to_csv(f, line_terminator='\n', float_format = "%.4f" , index=False)
        else:
            df.to_csv(f, line_terminator='\n', index=False)

    print('    Dados salvos em: ' + file_path)