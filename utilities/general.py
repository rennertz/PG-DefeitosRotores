import pandas as pd
import numpy as np


def read_compressed_csv(file_path, ratio = 50):
    '''Realiza a leitura dos sinais reduzindo a frequência da aquisição 'ratio' vezes, 
    tomando apenas 1 a cada 'ratio' amostras temporais'''
    
    # lista as linhas para exclusão em 'skip'
    skip = [i for i in range(0, 250000) if i % ratio]
 
    signals = pd.read_csv(
        file_path, 
        header=None,
        names=['tacometro', 'ax1', 'rad1', 'tg1','ax2', 'rad2', 'tg2', 'microfone'],
        skiprows=skip,
    )

    return signals


def generate_fft(signals, ratio = 50):
    '''Gera o dataframe com a transformada rápida de fourrier 
    a partir do dataframe dos sinais no tempo'''

    # define nova frequência de aquisição. 
    sampling_freq = 50000/ratio
    # note: 50 kHz é a frequência de aquisição original dos dados 

    # produz a transformada de Fourrier para cada sinal real. 
    signals_fft = signals.apply(np.fft.rfft, axis=0, norm="ortho")
    # note: a rfft apresenta apenas a metade relevante da transformada, 
    # pois sinais reais produzem transformadas simétricas

    # gera o eixo da frequência, dado que a frequência de Nyquist é sampling_freq/2
    signals_fft['freq_ax'] = np.linspace(0, sampling_freq/2, 
                                           signals_fft.shape[0])
                                           
    # obtém valor absoluto a partir da transformada complexa
    fft_amplitude = signals_fft.apply(np.abs)

    return signals_fft, fft_amplitude


def save_file(file_path, df, truncate=False):
    '''(sobre-)Escreve um cvs com todos os dados'''
    
    with open(file_path, "w") as f:
        if truncate:
            df.to_csv(f, line_terminator='\n', float_format = "%.4f" , index=False)
        else:
            df.to_csv(f, line_terminator='\n', index=False)

    print('    Dados salvos em: ' + file_path)