'''
Coleção de funções para extração das características julgadas
relevantes para o terinamento do modelo ML
'''

import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy import signal
from scipy import integrate
from utilities.general import read_compressed_csv, generate_fft


def extract_features(file_adress):
    '''Função principal, abre o arquivo cvs e utiliza as demais funções'''

    # reduz a frequência da aquisição 'ratio' vezes, tomando apenas 1 a cada 'ratio' amostras temporais
    ratio = 50

    # abre o arquivo e lê linhas selecionadas
    signals = read_compressed_csv(file_adress, ratio)

    # produz a transformada de Fourrier para cada sinal real.
    fft_complex, fft_amplitude = generate_fft(signals, ratio)


    # encontra a fundamental e o seu index
    fundamental = get_fundamental(fft_amplitude)
    index = fft_amplitude.index[fft_amplitude['freq_ax'] == fundamental] 

    # gera o dicionário com as features do experimento
    features = {'fundamental': fundamental}
    features.update(get_n_harmonics(fft_amplitude, index))
    features.update(get_phase_angles(fft_complex, index))
    features.update(get_time_statistics(signals))
    # features.update(get_vel_rms(signals, sampling_freq))

    return features


def get_fundamental(fft_df):
    '''Dentre os 3 maiores picos na fft do tacômetro, deve retornar o de menor frequência.
    Assim, evita-se o mascaramento da fundamental pelas harmonicas'''

    candidates = [0, 0, 0]
    for i in range(3):
        index = fft_df.tacometro.argmax()
        candidates[i] = fft_df.freq_ax[index]
        for j in range(-2, 3):
            fft_df.tacometro[index+j] = 0

    return min(candidates)


def get_n_harmonics(fft_df, fund_index, n_harmonics=5):
    '''Extrai todos os valores nos n primeiros harmônicos, exceto para o tacometro e freq_ax'''

    fft_df = fft_df.drop(['tacometro', 'freq_ax', 'microfone'], axis=1)

    harmonic_features = {}
    idx = fund_index[0]
    for i in range(1, n_harmonics+1):
        # resgata na frequência os valores na harmonica i
        # a partir do maior valor encontrado em um intervalo de +/- 5 Hz em torno da posição i*fundamental
        harm_values = fft_df.iloc[idx*i-5:idx*i+5].max()
        
        # adiciona às features com o respectivo sulfixo do harmonico i
        harmonic_features.update({k+'_{}h'.format(i): v for k, v in harm_values.items()})

    return harmonic_features


def get_phase_angles(fft_df, fund_index):
    '''extrai todos os valores nos n primeiros harmônicos, exceto para o tacometro e freq_ax'''

    fft_df = fft_df.drop(['microfone'], axis=1)
    
    # resgata FFT na fundamental para cada eixo
    fft_df = fft_df.iloc[fund_index].squeeze()
    
    # calcula o angulo de fase em radianos
    angle = fft_df.apply(np.angle)

    # subtrai o ângulo de fase de cada eixo em relação ao do tacômetro antes de descarta-lo
    angle = angle - angle['tacometro']
    angle.pop('tacometro')
    
    # recupera ângulo para o intervalo -pi a pi graus
    angle = (angle + np.pi) % (2*np.pi) - np.pi

    # retorna features com o respectivo sulfixo
    return {k+'_phase': v for k, v in angle.items()}


def get_time_statistics(time_df):
    '''extrai entropia, média e curtose para os sinais, exceto para o tacometro'''

    time_df = time_df.drop('tacometro', axis=1)

    # média    ## REMOVIDAS POR NÂO FAZEREM SENTIDO FÍSICO 
    # medias = time_df.mean().to_dict()
    # medias = {k+'_mean': v for k,v in medias.items()}

    # curtose
    curtoses = time_df.kurtosis().to_dict()
    curtoses = {k+'_kurt':v for k, v in curtoses.items()} 
    
    # entropia
    entropias = calc_entropy(time_df)
    entropias = {k+'_entr':v for k,v in entropias.items()}

    # RMS
    rms = time_df.pow(2).sum().pow(1/2).to_dict()
    rms = {k+'_rms':v for k, v in rms.items()}

    # reúne todos os valores
    # time_statistics.update(medias)
    time_statistics = entropias
    time_statistics.update(curtoses)
    time_statistics.update(rms)

    return time_statistics


def get_vel_rms(time_df, sampl_freq):
    '''transforna-se o sinal de m/s² para mm/s²'''

    acc_mmps2 = time_df.drop(['tacometro', 'microfone'], axis=1) *1000

    # instancia o filtro passa alta arbitrário em 10 Hz 
    sos = signal.butter(6, 10, 'highpass', fs=sampl_freq, output='sos')

    # calcula velocidade pela integral (trapezoidal) dos sinais
    velocity_filtered = pd.DataFrame()
    dt = 1/sampl_freq
    for col in acc_mmps2.columns:
        velocity_filtered[col] = integrate.cumtrapz(y=np.array(acc_mmps2[col]), dx=dt, initial=0)
        velocity_filtered[col] = signal.sosfilt(sos, velocity_filtered[col])

    vel_rms = velocity_filtered.pow(2).sum().pow(1/2).to_dict()

    return {k+'_vel_rms':v for k, v in vel_rms.items()}


def calc_entropy(dataframe):
    entropias = {}
    
    for col in dataframe.columns.values[:]:
        # divide cada sinal em 100 faixas e faz a contagem para cada faixa
        out = np.histogram(dataframe[col], bins=100)[0]
        # calcula a entropia de shannon
        entropias[col] = stats.entropy(out)
        
    return entropias