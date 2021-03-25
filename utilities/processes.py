import os
import sys
import shutil
from pathlib import Path
import os
import pandas as pd
import time
from utilities.general import read_compressed_csv, generate_fft, save_file
from utilities.features import extract_features

def iterate_and_extract():
    '''Código responsável por estruturar o dataset PRINCIPAL do projeto

    Este dataset deve conter TODAS as características julgadas
    relevantes para o terinamento do modelo ML


    NOTICE
    - Novas features podem ser adicionadas em features.extract_features
    '''

    configure_normal_path()

    print("\n  Iniciando extração de características\n")

    # instancia o DataFrame com as primeiras colunas
    df = pd.DataFrame(columns=['condicao', 'severidade', 'rotacao', 'fundamental'])

    # abre a pasta de cada defeito
    for condition in ['horizontal-misalignment', 'vertical-misalignment', 'imbalance', 'normal']:
        num_severities = len(os.listdir(f"mafaulda/{condition}"))
        
        print('Carregando', condition)
        instance_time = time.time()

        # abre a subpasta de cada severidade do defeito
        for i, severity in enumerate(os.listdir(f"mafaulda/{condition}")):
            num_rotations = len(os.listdir(f"mafaulda/{condition}/{severity}"))
            
            severity_numeric = severity.replace('g', '').replace('mm', '')
            severity_numeric = float(severity_numeric)

            # abre cada arquivo, cujo nome indica a velocidade de rotação
            for j, rotation in enumerate(os.listdir(f"mafaulda/{condition}/{severity}")):
                
                # exibe barra de status para o usuário (de acordo com o tipo de falha)
                print_status_bar( (i + (j+1) / num_rotations) / num_severities)

                # identifica o tipo de defeito, a severidade e a rotaçao
                data = {'condicao': condition,
                        'severidade': severity_numeric,
                        'rotacao': float(rotation[:-4]) 
                }

                # extrai características (toma muito tempo!)
                features = extract_features(f"mafaulda/{condition}/{severity}/{rotation}")
                data.update(features)

                # adiciona o novo dado ao dataframe
                df = df.append(data, ignore_index=True)
        

        print('\n    Execução em {:.3f} segundos\n'.format(time.time()-instance_time))
    
    df.info()

    save_file("data.csv", df)

    return df


def iterate_and_compress():
    '''Código responsável por compactar a base MaFaulDa ao: 

    (1) reduzir a taxa de amostragem 
    (2) reduzir a precisão da representação decimal em texto
    (3) condensar cada sequência de ensaios em um úníco arquivo
    '''
        
    configure_normal_path()

    print("\n  Iniciando compressão da base MAFAULDA\n")

    # cria estrutura de pastas que receberá os novos arquivos
    for folder in ['horizontal-misalignment', 'vertical-misalignment', 'imbalance', 'normal']:
        Path("mafaulda_reduced/"+folder).mkdir(parents=True, exist_ok=True)


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

                # adiciona os sinais da rotação específica ao dataframe conjunto
                df_time = df_time.append(signals, ignore_index=True)
                df_freq = df_freq.append(fft_amplitude, ignore_index=True)


            print(' ')
            save_file(f'mafaulda_reduced/{condition}/{severity}.csv', df_time, truncate=True)
            save_file(f'mafaulda_reduced/{condition}/{severity}_fft.csv', df_freq, truncate=True)


        print('\n    Execução em {:.3f} segundos'.format(
            time.time()-instance_time))


def print_status_bar(status):
    '''Define e exibe barra de status ao usuário'''

    sys.stdout.write('\r')
    sys.stdout.write('    [{:20}] {:.3f}%'.format(
                     round(status*20)*'=', 100*status))
    sys.stdout.flush()


def configure_normal_path():
    '''Configura a pasta normal para sua correta digestão'''

    source_dir = "mafaulda/normal"
    file_names = os.listdir(source_dir)

    target_dir = "mafaulda/normal/0"
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)
