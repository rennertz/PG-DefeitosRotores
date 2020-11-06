import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import scipy.stats as stats

# TODO: extrair Entropia, Média, Curtose dos sete sinais (6 acc e microfone)


def extract_features(file_adress):
    # reduz a frequência da aquisição 'ratio' vezes, tomando apenas 1 a cada 'ratio' amostras temporais
    # note: 50 kHz é a frequência de aquisição original dos dados! 
    ratio = 50
    sampling_freq = 50000/ratio

    # poupa para a leitura apenas as linhas múltiplas de 'ratio' e lista as demais para exclusão em 'skip'
    skip = [i for i in range(0, 250000) if i % ratio]
    signals = pd.read_csv(file_adress, header=None,
                          names=['tacômetro', 'ac1rad', 'ac1ax', 'ac1tg',
                                 'ac2rad', 'ac2ax', 'ac2tg', 'microfone'],
                          skiprows=skip)

    # produz a transformada de Fourrier para cada sinal real. 
    # a rfft representa apenas a metade relevante da transformada. Sinais reais produzem transformadas simétricas
    signals_fft = signals.apply(np.fft.rfft, axis=0, norm="ortho")
    # obtém valor absoluto a partir dos complexos
    signals_fft = signals_fft.apply(np.abs)

    # gera o eixo da frequência, dado que a frequência de Nyquist é sampling_freq/2
    signals_fft['freq_ax'] = np.linspace(0, sampling_freq/2+1, 
    									 signals_fft.shape[0])

    # gera as features, começando pela fundamental
    fundamental = extract_fundamental(signals_fft)
    # extrai o index da fundamental
    index = signals_fft.index[signals_fft['freq_ax'] == fundamental] 

    features = {'fundamental': fundamental}
    features.update(extract_n_harmonics(signals_fft, index))
    features.update(extract_time_statistics(signals))

    return features


def extract_fundamental(fft_df):
    # dentre os 3 maiores picos na fft do tacômetro, deve retornar o de menor frequência
    # assim, evita-se o mascaramento da fundamental pelas harmonicas

    candidates = [0, 0, 0]
    for i in range(3):
        index = fft_df['tacômetro'].argmax()
        candidates[i] = fft_df.freq_ax[index]
        for j in range(-2, 3):
            fft_df['tacômetro'][index+j] = 0

    return min(candidates)


def extract_n_harmonics(fft_df, fund_index, n_harmonics=3):
    # extrai todos os valores nos n primeiros harmônicos, exceto para o tacômetro e freq_ax
    fft_df = fft_df.drop(['tacômetro', 'freq_ax'], axis=1)

    harmonic_features = {}
    idx = fund_index[0]
    for i in range(1, n_harmonics+1):
        # resgata na frequência os valores na harmonica i
        # a partir do maior valor encontrado em um intervalo de +/- 5 Hz em torno da posição i*fundamental
        harm_values = fft_df.iloc[idx*i-25:idx*i+26].max()
        
        # adiciona às features com o respectivo sulfixo do harmonico i
        harmonic_features.update({k+'_{}h'.format(i): v for k, v in harm_values.items()})

    return harmonic_features


def extract_time_statistics(time_df):
    # extrai entropia, média e curtose para os sinais, exceto para o tacômetro
    time_df = time_df.drop('tacômetro', axis=1)

    # entropia
    step = 0.2
    bin_range = np.arange(-10, 10+step, step)
    entropias = {}
    for i, col in enumerate(time_df.columns.values[:]):
        out = pd.cut(time_df[col], bins = bin_range, include_lowest=True, right=False, retbins=True)[0]
        entropias[col] = stats.entropy(out.value_counts())

    entropias = {k+'_entr':v for k,v in entropias.items()}

    # média
    medias = time_df.mean().to_dict()
    medias = {k+'_mean': v for k,v in medias.items()}

    # curtose
    curtoses = time_df.kurtosis().to_dict()
    curtoses = {k+'_kurt':v for k, v in curtoses.items()}

    # RMS
    rms = time_df.pow(2).sum().pow(1/2).to_dict()
    rms = {k+'_rms':v for k, v in rms.items()}

    # reúne todos os valores
    time_statistics = entropias
    time_statistics.update(medias)
    time_statistics.update(curtoses)
    time_statistics.update(rms)

    return time_statistics
