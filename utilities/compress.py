'''
Código responsável por compactar a base MaFaulDa ao 
(1) reduzir a taxa de amostragem 
(2) reduzir a precisão da representação decimal em texto
(3) condensar cada sequência de ensaios em um úníco arquivo
'''

import os
import pandas as pd
from pathlib import Path  # permite ao programa criar pastas
import time  # permite marcar o tempo de execução
from utilities.general import print_status_bar, configure_normal_path, read_compressed_csv, generate_fft



def iterate_and_compress():
    '''Função principal de compressão. Entrará em cada pasta e irá comprimir todos os arquivos em apenas um'''
    
    configure_normal_path()

    print("\nIniciando compressão da base MAFAULDA\n")

    # cria estrutura de pastas que receberá os novos arquivos
    for folder in ['horizontal-misalignment', 'vertical-misalignment', 'imbalance', 'normal']:
        Path("../mafaulda_reduced/"+folder).mkdir(parents=True, exist_ok=True)


    # abre a pasta de cada defeito
    for condition in ['horizontal-misalignment', 'vertical-misalignment', 'imbalance', 'normal']:
        num_severities = len(os.listdir(f"mafaulda/{condition}"))

        print('Carregando', condition)
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
                signals = read_compressed_csv(f"mafaulda/{condition}/{severity}/{rotation}")
                _, fft_amplitude = generate_fft(signals)

                # recupera o nome do arquivo como rotaçao
                signals['rotacao'] = rotation[:-4]
                fft_amplitude['rotacao'] = rotation[:-4]

                # adiciona o novo dado ao dataframe
                df_time = df_time.append(signals, ignore_index=True)
                df_freq = df_freq.append(fft_amplitude, ignore_index=True)


            print(' ')
            save_file(f'../mafaulda_reduced/{condition}/{severity}.csv', df_time)
            save_file(f'../mafaulda_reduced/{condition}/{severity}_fft.csv', df_freq)


        print('\n    Execução em {:.3f} segundos'.format(
            time.time()-instance_time))

def save_file(file_path, df):
    '''(sobre-)escreve um cvs com todos os dados'''
    
    with open(file_path, "w") as f:
        df.to_csv(f, line_terminator='\n', float_format = "%.4f" , index=False)
    
    print('    Dados salvos em: ' + file_path)


if __name__ == "__main__":
    start_time = time.time()

    iterate_and_compress()

    # Exibe o tempo total de execução ao usuário
    total_duration = time.time()-start_time
    print('\nExecução total em {} minutos e {:.3f} segundos'.format(
        int(total_duration//60), total_duration % 60))