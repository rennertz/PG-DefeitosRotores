# bibliotecas mais importantes
import pandas as pd
import numpy as np
from scipy.signal import decimate, butter, sosfilt

class Measurement():
    def __init__(self, address, ratio=10, verbose=False):
        # reduz o a frequência de amostragem 'ratio' vezes, tomando apenas 1 a cada 'ratio' sinais
        self.ratio = ratio
        self.sampling_freq=50000/ratio

        self.time = self.read_file(address, ratio)
        self.time_acc = self.time.drop(['tacometro','microfone'], axis=1)

        self.freq, self.phase = self.fft_transform(self.time, self.sampling_freq)
        self.freq_acc = self.freq.drop(['tacometro', 'microfone'], axis=1)
        
        self.rotacao_calc, self.rotacao_calc_idx = self.extract_rotacao_calc(self.freq)
        
        
        if verbose:
            print("\nSinal com shape {}".format(self.time.shape))
            print("a frequência de aquisição foi reduzida de 50kHz para {}kHz\n".format(self.sampling_freq/1000))
        
    
    def read_file(self, address, ratio):
        '''lê dados no tempo, aplica downsamplig e filtra componentes abaixo de 0.5 Hz'''
        
        signals = pd.read_csv(
            address, 
            header=None, 
            names=['tacometro','ax1','rad1','tg1','ax2','rad2','tg2','microfone'],
        )
        
        if ratio > 1:
            signals = signals.apply(decimate, axis=0, q=ratio)
        
        sos = butter(6, 0.5, 'highpass', fs=self.sampling_freq, output='sos')
        for col in signals.columns:
            signals[col] = sosfilt(sos, signals[col])


        # reordena colunas
        return signals[['rad1','rad2','tg1','tg2','ax1','ax2','tacometro','microfone']]


    def fft_transform(self, signals_df, sampling_freq):
        '''aplica transformada de Fourrier e converte para valores absolutos'''
        
        signals_fft = signals_df.apply(np.fft.rfft, axis=0, norm="ortho")
        signals_fft_amplitude = signals_fft.apply(np.abs)
        signals_fft_phase = signals_fft.apply(np.angle, deg=True)

        # adiciona eixo da frequência
        # OBS: a frequência de Nyquist é sampling_freq/2
        freq_ax = np.linspace(0, sampling_freq/2, signals_fft.shape[0])
        signals_fft_amplitude['freq_ax'] = freq_ax
        signals_fft_phase['freq_ax'] = freq_ax

        return signals_fft_amplitude, signals_fft_phase
    
    
    def extract_rotacao_calc(self, fft_df):
        tachometer_fft = fft_df['tacometro'].copy(deep=True)
        candidates = [0, 0, 0]

        # separa os 3 maiores picos na fft do tacômetro
        for i in range(3):
            index = tachometer_fft.argmax()
            candidates[i] = fft_df.freq_ax[index]

            # retira da próxima iteração os valores adjacentes ao pico separado
            for j in range(-2, 3):
                tachometer_fft[index+j] = 0

        # deve retornar pico o de menor frequência, evitando o mascaramento da rotacao_calc pelas harmonicas
        rotacao_calc = min(candidates)
        index = fft_df.index[fft_df['freq_ax'] == rotacao_calc]

        return rotacao_calc, index[0]
