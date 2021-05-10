"""
Coleção de funções para extração das características julgadas
relevantes para o terinamento do modelo ML
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy import signal
from scipy import integrate


def extract_features(signals, fft, fft_amplitude, ratio = 10):
    """Função principal, chama as demais funções"""

    # retira o sinal do microfone da análise
    signals.pop('microfone')
    fft.pop('microfone')
    fft_amplitude.pop('microfone')

    # encontra a rotacao_calc e o seu index
    rotacao_calc = get_rotation(fft_amplitude)
    index = fft_amplitude.index[fft_amplitude['freq_ax'] == rotacao_calc] 

    # remove colunas após a determinação da rotação
    signals.pop('tacometro')
    fft.pop('freq_ax')
    fft_amplitude.pop('tacometro')


    # gera o dicionário com as features do experimento
    features = {'rotacao_calc': rotacao_calc}
    features.update(get_n_harmonics(fft_amplitude, index))
    features.update(get_phase_angles(fft, index))
    features.update(get_time_statistics(signals))
    features.update(get_freq_statistics(fft_amplitude))
    # features.update(get_vel_rms(signals, ratio))

    return features


def get_rotation(fft_amplitude_df):
    """Dentre os 3 maiores picos na fft do tacômetro, deve retornar o de menor frequência.
    Assim, evita-se o mascaramento da rotacao_calc pelas harmonicas"""

    # cópia que evita sobrescrição de valores no DataFrame original
    tacometro_copy = fft_amplitude_df['tacometro'].copy()

    candidates = [0, 0, 0]
    for i in range(3):
        index = tacometro_copy.argmax()
        candidates[i] = fft_amplitude_df.freq_ax[index]
        for j in range(-2, 3):
            tacometro_copy[index+j] = 0

    return min(candidates)


def get_n_harmonics(fft_amplitude_df, fund_index, n_harmonics=3):
    """Extrai todos os valores nos n primeiros harmônicos, exceto para o tacometro e freq_ax"""
    fft_amplitude_df = fft_amplitude_df.drop(['freq_ax'], axis=1)

    harmonic_features = {}
    idx = fund_index[0]
    for i in range(1, n_harmonics+1):
        # resgata na frequência os valores na harmonica i
        # a partir do maior valor encontrado em um intervalo de +/- 5 Hz em torno da posição i*rotacao_calc
        harm_values = fft_amplitude_df.iloc[(idx-5)*i:(idx+5)*i].max()
        
        # adiciona às features com o respectivo sulfixo do harmonico i
        harmonic_features.update({k+'_{}h'.format(i): v for k, v in harm_values.items()})

    return harmonic_features


def get_phase_angles(fft_df, fund_index):
    """extrai todos os valores nos n primeiros harmônicos, exceto para o tacometro e freq_ax"""
    
    # resgata FFT na rotacao_calc para cada eixo
    fft_df = fft_df.iloc[fund_index].squeeze()

    # encontra a diferença do ângulo de fase de cada eixo 
    # em relação ao do tacômetro antes de descarta-lo
    fft_df = fft_df / fft_df['tacometro']
    fft_df.pop('tacometro')
    
    # calcula o angulo de fase em radianos
    angle = fft_df.apply(np.angle)

    # retorna features com o respectivo sulfixo
    return {k+'_phase': v for k, v in angle.items()}


def get_time_statistics(time_df):
    """extrai estatísticas do sinal no tempo"""
    
    # valores auxiliares
    absolute_max = time_df.abs().max()
    absolute_average = time_df.abs().mean()

    # valores extraídos
    rms = time_df.pow(2).sum().pow(1/2)
    sra = time_df.abs().pow(1/2).mean().pow(2)
    kurtosis = time_df.kurtosis()
    sqewness = time_df.skew()
    peak_to_peak = time_df.max() - time_df.min()
    crest = absolute_max / rms
    impulse = absolute_max / absolute_average
    margin = absolute_max / sra
    shape = rms / absolute_average
    kurtosis_f = kurtosis / rms.pow(4)
    entropy = calc_entropy(time_df)
    
    rms_dic =           {k+'_timestat_rms':v for k, v in rms.to_dict().items()}
    sra_dic =           {k+'_timestat_sra':v for k, v in sra.to_dict().items()}
    kurtosis_dic =      {k+'_timestat_kurt':v for k, v in kurtosis.to_dict().items()}
    sqewness_dic =      {k+'_timestat_sqew':v for k, v in sqewness.to_dict().items()}
    peak_to_peak_dic =  {k+'_timestat_peak':v for k, v in peak_to_peak.to_dict().items()}
    crest_dic =         {k+'_timestat_crest':v for k, v in crest.to_dict().items()}
    impulse_dic =       {k+'_timestat_impulse':v for k, v in impulse.to_dict().items()}
    margin_dic =        {k+'_timestat_margin':v for k, v in margin.to_dict().items()}
    shape_dic =         {k+'_timestat_shape':v for k, v in shape.to_dict().items()}
    kurtosis_f_dic =    {k+'_timestat_kurt_f':v for k, v in kurtosis_f.to_dict().items()}
    entropy_dic =       {k+'_timestat_entropy':v for k, v in entropy.to_dict().items()}

    time_statistics = {}
    time_statistics.update(rms_dic)
    time_statistics.update(sra_dic)
    time_statistics.update(kurtosis_dic)
    time_statistics.update(sqewness_dic)
    time_statistics.update(peak_to_peak_dic)
    time_statistics.update(crest_dic)
    time_statistics.update(impulse_dic)
    time_statistics.update(margin_dic)
    time_statistics.update(shape_dic)
    time_statistics.update(kurtosis_f_dic)
    time_statistics.update(entropy_dic)

    return time_statistics


def get_freq_statistics(fft_amplitude_df):
    """extrai estatísticas do sinal no tempo"""

    freq_ax = fft_amplitude_df['freq_ax']
    fft_amplitude_df = fft_amplitude_df.drop(['freq_ax'], axis=1)

    sum_axis = fft_amplitude_df.sum()

    freq_center = (freq_ax * fft_amplitude_df.T).T.sum() /  sum_axis
    rmsf = ((freq_ax**2 * fft_amplitude_df.T).T.sum() /  sum_axis).pow(1/2)
    rvf = ((np.subtract.outer(freq_ax.values, freq_center.values)**2 * fft_amplitude_df).sum() /  sum_axis).pow(1/2)

    freq_center_dict = {k+'_freqstat_fc':v for k, v in freq_center.to_dict().items()}
    rmsf_dict = {k+'_freqstat_rmsf':v for k, v in rmsf.to_dict().items()}
    rvf_dict = {k+'_freqstat_rvf':v for k, v in rvf.to_dict().items()}

    freq_statistics = {}
    freq_statistics.update(freq_center_dict)
    freq_statistics.update(rmsf_dict)
    freq_statistics.update(rvf_dict)

    return freq_statistics
    

def get_vel_rms(time_df, ratio=10):
    """integra o sinal da aceleração para a velocidade e extrai o valor-eficaz"""

    # define nova frequência de aquisição. 
    sampling_freq = 50000/ratio
    # note: 50 kHz é a frequência de aquisição original dos dados 

    # instancia o filtro passa alta arbitrário em 10 Hz 
    sos = signal.butter(6, 10, 'highpass', fs=sampling_freq, output='sos')

    # calcula velocidade pela integral (trapezoidal) dos sinais
    velocity_filtered = pd.DataFrame()
    dt = 1/sampling_freq
    for col in time_df.columns:
        velocity_filtered[col] = signal.sosfilt(sos, time_df[col])
        velocity_filtered[col] = integrate.cumtrapz(y=np.array(velocity_filtered[col]), dx=dt, initial=0)

    vel_rms = velocity_filtered.pow(2).sum().pow(1/2).to_dict()

    return {k+'_vel_rms':v for k, v in vel_rms.items()}


def calc_entropy(dataframe):
    entropias = pd.Series()
    
    for col in dataframe.columns.values[:]:
        # divide cada sinal em 100 faixas e faz a contagem para cada faixa
        out = np.histogram(dataframe[col], bins=40)[0]
        # calcula a entropia de shannon
        entropias[col] = stats.entropy(out)
        
    return entropias