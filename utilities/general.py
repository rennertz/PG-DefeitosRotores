import sys
import shutil
from pathlib import Path
import os
import pandas as pd
import numpy as np

# realiza a leitura dos sinais reduzindo a frequência da aquisição 'ratio' vezes, 
# tomando apenas 1 a cada 'ratio' amostras temporais
RATIO = 50


def configure_normal_path():
    '''configura a pasta normal para sua correta digestão'''

    source_dir = "mafaulda/normal"
    file_names = os.listdir(source_dir)

    target_dir = "mafaulda/normal/0"
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)


def read_compressed_csv(file_path, ratio = RATIO):
    '''Lê o arquivo, poupando as linhas múltiplas de "ratio"''' 
    
    # lista as linhas para exclusão em 'skip'
    skip = [i for i in range(0, 250000) if i % ratio]
 
    signals = pd.read_csv(
        file_path, 
        header=None,
        names=['tacometro', 'ax1', 'rad1', 'tg1','ax2', 'rad2', 'tg2', 'microfone'],
        skiprows=skip,
    )

    return signals


def generate_fft(signals, ratio = RATIO):
    # Nova frequência de aquisição. Note: 50 kHz é a frequência de aquisição original dos dados! 
    sampling_freq = 50000/ratio

    # produz a transformada de Fourrier para cada sinal real. 
    # a rfft representa apenas a metade relevante da transformada. Sinais reais produzem transformadas simétricas
    signals_fft = signals.apply(np.fft.rfft, axis=0, norm="ortho")

    # gera o eixo da frequência, dado que a frequência de Nyquist é sampling_freq/2
    signals_fft['freq_ax'] = np.linspace(0, sampling_freq/2, 
                                           signals_fft.shape[0])
                                           
    # obtém valor absoluto a partir dos complexos
    fft_amplitude = signals_fft.apply(np.abs)

    return signals_fft, fft_amplitude


def print_status_bar(status):
    '''define e exibe barra de status ao usuário'''
    sys.stdout.write('\r')
    sys.stdout.write('    [{:20}] {:.3f}%'.format(
                     round(status*20)*'=', 100*status))
    sys.stdout.flush()