'''
Código responsável por estruturar o dataset PRINCIPAL do projeto

Este dataset deve conter TODAS as características julgadas
relevantes para o terinamento do modelo ML


NOTICE
 - Novas features podem ser adicionadas em feat_functions.extract_features
'''

import sys
import os
from pathlib import Path
import shutil
import pandas as pd
from . import feat_functions
import time


def iterate_and_extract():
    '''Função principal de extração. Entrará em cada pasta e irá extrair as características'''
    
    configure_normal_path()

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
                features = feat_functions.extract_features(f"mafaulda/{condition}/{severity}/{rotation}")
                data.update(features)

                # adiciona o novo dado ao dataframe
                df = df.append(data, ignore_index=True)
        

        print('\n    Execução em {:.3f} segundos\n'.format(time.time()-instance_time))
    
    return df


def print_status_bar(status):
    '''define e exibe a barra de status ao usuário'''

    sys.stdout.write('\r')
    sys.stdout.write('    [{:20}] {:.3f}%'.format(
                     round(status*20)*'=', 100*status))
    sys.stdout.flush()


def configure_normal_path():
    '''configura a pasta normal para sua correta digestão'''

    source_dir = "mafaulda/normal"
    file_names = os.listdir(source_dir)

    target_dir = "mafaulda/normal/0"
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)


if __name__ == '__main__':

    # inicia a cronometragem
    start_time = time.time()

    # extrai dados e exibe o resumo
    df = iterate_and_extract()
    df.info()

    # (sobre-)escreve um cvs com todos os dados
    with open("data.csv", "w") as file:
        df.to_csv(file, line_terminator='\n', index=False)
    print('Dados salvos em: data.csv')

    # exibe o tempo de execução total ao usuário
    total_duration = time.time()-start_time
    print('\nExecução total em {} minutos e {:.3f} segundos'.format(
          int(total_duration//60), total_duration % 60))
