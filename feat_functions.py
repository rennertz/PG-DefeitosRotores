import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import scipy.stats as stats
from scipy import signal
from scipy import integrate

# TODO: extrair Entropia, Média, Curtose dos sete sinais (6 acc e microfone)


def extract_features(file_adress):
    # reduz a frequência da aquisição 'ratio' vezes, tomando apenas 1 a cada 'ratio' amostras temporais
    # note: 50 kHz é a frequência de aquisição original dos dados! 
    ratio = 50
    sampling_freq = 50000/ratio

    # poupa para a leitura apenas as linhas múltiplas de 'ratio' e lista as demais para exclusão em 'skip'
    skip = [i for i in range(0, 250000) if i % ratio]
    signals = pd.read_csv(file_adress, header=None,
                          names=['tacometro', 'ax1', 'rad1', 'tg1',
                                 'ax2', 'rad2', 'tg2', 'microfone'],
                          skiprows=skip)

    # produz a transformada de Fourrier para cada sinal real. 
    # a rfft representa apenas a metade relevante da transformada. Sinais reais produzem transformadas simétricas
    signals_fft = signals.apply(np.fft.rfft, axis=0, norm="ortho")
    # obtém valor absoluto a partir dos complexos
    fft_amplitude = signals_fft.apply(np.abs)

    # gera o eixo da frequência, dado que a frequência de Nyquist é sampling_freq/2
    fft_amplitude['freq_ax'] = np.linspace(0, sampling_freq/2+1, 
    									 fft_amplitude.shape[0])

    # gera as features, começando pela fundamental
    fundamental = extract_fundamental(fft_amplitude)
    # extrai o index da fundamental
    index = fft_amplitude.index[fft_amplitude['freq_ax'] == fundamental] 

    features = {'fundamental': fundamental}
    features.update(extract_n_harmonics(fft_amplitude, index))
    features.update(extract_phase_angles(signals_fft, index))
    features.update(extract_time_statistics(signals))
    features.update(estract_vel_rms(signals, sampling_freq))

    return features


def extract_fundamental(fft_df):
    # dentre os 3 maiores picos na fft do tacômetro, deve retornar o de menor frequência
    # assim, evita-se o mascaramento da fundamental pelas harmonicas

    candidates = [0, 0, 0]
    for i in range(3):
        index = fft_df['tacometro'].argmax()
        candidates[i] = fft_df.freq_ax[index]
        for j in range(-2, 3):
            fft_df['tacometro'][index+j] = 0

    return min(candidates)


def extract_n_harmonics(fft_df, fund_index, n_harmonics=3):
    # extrai todos os valores nos n primeiros harmônicos, exceto para o tacometro e freq_ax
    fft_df = fft_df.drop(['tacometro', 'freq_ax'], axis=1)

    harmonic_features = {}
    idx = fund_index[0]
    for i in range(1, n_harmonics+1):
        # resgata na frequência os valores na harmonica i
        # a partir do maior valor encontrado em um intervalo de +/- 5 Hz em torno da posição i*fundamental
        harm_values = fft_df.iloc[idx*i-25:idx*i+26].max()
        
        # adiciona às features com o respectivo sulfixo do harmonico i
        harmonic_features.update({k+'_{}h'.format(i): v for k, v in harm_values.items()})

    return harmonic_features

def extract_phase_angles(fft_df, fund_index):
    # extrai todos os valores nos n primeiros harmônicos, exceto para o tacometro e freq_ax
    fft_df = fft_df.drop(['microfone'], axis=1)
    
    # resgata FFT na fundamental para cada eixo
    fft_df = fft_df.iloc[fund_index].squeeze()
    # calcula o angulo de fase 
    angle = fft_df.apply(np.angle, deg=True)

    # subtrai o ângulo de fase de cada eixo em relação ao do tacômetro antes de descarta-lo
    angle = angle - angle['tacometro']
    angle.pop('tacometro')
    # recupera ângulo para o intervalo -180 a 180 graus
    angle = (angle + 180) % 360 - 180

    # retorna features com o respectivo sulfixo
    return {k+'_phase': v for k, v in angle.items()}


def extract_time_statistics(time_df):
    # extrai entropia, média e curtose para os sinais, exceto para o tacometro
    time_df = time_df.drop('tacometro', axis=1)

    # entropia
    step = 0.2
    bin_range = np.arange(-10, 10+step, step)
    entropias = {}
    for i, col in enumerate(time_df.columns.values[:]):
        out = pd.cut(time_df[col], bins = bin_range, include_lowest=True, right=False, retbins=True)[0]
        entropias[col] = stats.entropy(out.value_counts())

    entropias = {k+'_entr':v for k,v in entropias.items()}

    # média    ## REMOVIDAS POR NÂO FAZEREM SENTIDO FÍSICO 
    # medias = time_df.mean().to_dict()
    # medias = {k+'_mean': v for k,v in medias.items()}

    # curtose
    curtoses = time_df.kurtosis().to_dict()
    curtoses = {k+'_kurt':v for k, v in curtoses.items()}

    # RMS
    rms = time_df.pow(2).sum().pow(1/2).to_dict()
    rms = {k+'_rms':v for k, v in rms.items()}

    # reúne todos os valores
    time_statistics = entropias
    # time_statistics.update(medias)
    time_statistics.update(curtoses)
    time_statistics.update(rms)

    return time_statistics


def estract_vel_rms(time_df, sampl_freq):
    # transforna-se o sinal de m/s² para mm/s²
    acc_mmps2 = time_df.drop(['tacometro', 'microfone'], axis=1) *1000

    # instancia o filtro passa alta arbitrário em 10 Hz 
    sos = signal.butter(6, 10, 'highpass', fs=sampl_freq, output='sos')

    # calcula velocidade pela integral (trapezoidal) dos sinais
    velocity_filtered = pd.DataFrame()
    dt = 1/sampl_freq
    for col in acc_mmps2.columns:
        velocity_filtered[col] = integrate.cumtrapz(y=np.array(acc_mmps2[col]), dx=dt, initial=0)
        velocity_filtered[col] = signal.sosfilt(sos, velocity_filtered[col])

    vel_rms = velocity_filtered.apply(rms).to_dict()

    return {k+'_vel_rms':v for k, v in vel_rms.items()}


def rms(x):
    return np.sqrt(x.dot(x)/x.size)