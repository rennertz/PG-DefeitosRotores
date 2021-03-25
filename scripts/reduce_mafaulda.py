'''
Código responsável por compactar a base MaFaulDa ao 
(1) reduzir a taxa de amostragem 
(2) reduzir a precisão da representação decimal em texto
(3) condensar cada sequência de ensaios em um úníco arquivo
'''

import os
import pandas as pd
import numpy as np
import sys  # permite imprimir status de importação
from pathlib import Path  # permite ao programa criar pastas
import time  # permite marcar o tempo de execução

# realiza a leitura dos sinais reduzindo a frequência da aquisição 'ratio' vezes, 
# tomando apenas 1 a cada 'ratio' amostras temporais
RATIO = 50


# define barra de status a ser mostrada ao usuário
def print_status_bar(status):
    sys.stdout.write('\r')
    sys.stdout.write('    [{:20}] {:.3f}%'.format(
                     round(status*20)*'=', 100*status))
    sys.stdout.flush()


def read_reduced_csv(file_path, ratio = RATIO):
    # poupa para a leitura apenas as linhas múltiplas de 'ratio' e lista as demais para exclusão em 'skip'
    skip = [i for i in range(0, 250000) if i % ratio]
    # Nova frequência de aquisição. Note: 50 kHz é a frequência de aquisição original dos dados! 

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
    # obtém valor absoluto a partir dos complexos
    signals_fft = signals_fft.apply(np.abs)

    # gera o eixo da frequência, dado que a frequência de Nyquist é sampling_freq/2
    signals_fft['freq_ax'] = np.linspace(0, sampling_freq/2, 
                                           signals_fft.shape[0])

    return signals_fft


# (sobre-)escreve um cvs com todos os dados
def save_file(file_path, df):
    with open(file_path, "w") as f:
        df.to_csv(f, line_terminator='\n', float_format = "%.4f" , index=False)
    
    print('    Dados salvos em: ' + file_path)


def iterate_and_reduce():

    # cria estrutura de pastas que receberá os novos arquivos
    for folder in ['horizontal-misalignment', 'vertical-misalignment', 'imbalance', 'normal']:
        Path("../mafaulda_reduced/"+folder).mkdir(parents=True, exist_ok=True)


    # abre a pasta de cada defeito
    for condition in ['horizontal-misalignment', 'vertical-misalignment', 'imbalance', 'normal']:
        num_severities = len(os.listdir(f"mafaulda/{condition}"))

        print('\nCarregando', condition)
        instance_time = time.time()

        # abre a subpasta de cada severidade do defeito
        for i, severity in enumerate(os.listdir("mafaulda/" + condition)):
            num_rotations = len(os.listdir(f"mafaulda/{condition}/{severity}"))
            
            # instancia os DataFrames
            df_time = pd.DataFrame(columns=['rotacao'])
            df_freq = pd.DataFrame(columns=['rotacao'])

            # abre cada arquivo, cujo nome indica a velocidade de rotação
            for j, rotation in enumerate(os.listdir(f"mafaulda/{condition}/{severity}")):

                # exibe barra de status para o usuário (de acordo com o tipo de falha)
                print_status_bar( (i + (j+1) / num_rotations) / num_severities)
                
                # aponta o arquivo e faz a leitura resumida
                signals = read_reduced_csv(f"mafaulda/{condition}/{severity}/{rotation}")
                signals_fft = generate_fft(signals)

                # recupera o nome do arquivo como rotaçao
                signals['rotacao'] = rotation[:-4]
                signals_fft['rotacao'] = rotation[:-4]

                # adiciona o novo dado ao dataframe
                df_time = df_time.append(signals, ignore_index=True)
                df_freq = df_freq.append(signals_fft, ignore_index=True)


            print(' ')
            save_file(f'../mafaulda_reduced/{condition}/{severity}.csv', df_time)
            save_file(f'../mafaulda_reduced/{condition}/{severity}_fft.csv', df_freq)
            print('\n')


        print('\n    Execução em {:.3f} segundos'.format(
            time.time()-instance_time))


if __name__ == "__main__":
    start_time = time.time()

    iterate_and_reduce()

    # Exibe o tempo total de execução ao usuário
    total_duration = time.time()-start_time
    print('\nExecução total em {} minutos e {:.3f} segundos'.format(
        int(total_duration//60), total_duration % 60))