'''
Código responsável por estruturar o dataset PRINCIPAL do projeto

Este dataset deve conter TODAS as características julgadas
relevantes para o terinamento do modelo ML


NOTICE
 - Novas features podem ser adicionadas em feat_functions.extract_features
'''

import os
import pandas as pd
import numpy as np
from feat_functions import extract_features
import sys  # para imprimir status de importação

import time  # permite marcar o tempo de execução
start_time = time.time()

# define barra de status a ser mostrada ao usuário
def print_status_bar(status):
    sys.stdout.write('\r')
    sys.stdout.write('    [{:20}] {:.3f}%'.format(
                     round(status*20)*'=', 100*status))
    sys.stdout.flush()


# instancia o DataFrame com as primeiras colunas
df = pd.DataFrame(columns=['defeito', 'severidade', 'rotacao', 'fundamental'])

# abre a pasta de cada defeito
for fault in ['horizontal-misalignment', 'vertical-misalignment', 'imbalance']:
    print('\nCarregando', fault)
    instance_time = time.time()

    # abre a subpasta de cada severidade do defeito
    for i, severity in enumerate(os.listdir("mafaulda/" + fault)):

        # abre cada arquivo, cujo nome indica a velocidade de rotação
        for j, rotation in enumerate(os.listdir("mafaulda/" + fault + '/' + severity)):
            
            # identifica o tipo de defeito e assigna sua severidade 
            # além disso, exibe barra de status para o usuário (de acordo com o tipo de falha)
            if fault == 'horizontal-misalignment':
                data = {'defeito': 'desalinhamento_horizontal',
                        'severidade': float(severity[:-2]) }

                print_status_bar((i+j/48)/4)

            elif fault == 'vertical-misalignment':
                data = {'defeito': 'desalinhamento_vertical',
                        'severidade': float(severity[:-2]) }

                print_status_bar((i+j/49)/6)

            elif fault == 'imbalance':
                data = {'defeito': 'desbalanceamento',
                        'severidade': float(severity[:-1]) }

                print_status_bar((i+j/48)/7)

            
            # recupera o nome do arquivo como rotaçao
            data.update({'rotacao': float(rotation[:-4]) })

            # extrai características (toma muito tempo!)
            features = extract_features("mafaulda/{}/{}/{}".format(fault, severity, rotation))
            data.update(features)

            # adiciona o novo dado ao dataframe
            df = df.append(data, ignore_index=True)
    

    print('\n    Execução em {:.3f} segundos'.format(
          time.time()-instance_time))



print('\nCarregando condição normal')
instance_time = time.time()

# abre a pasta de condição normal e abre cada arquivo
for i, rotation in enumerate(os.listdir("mafaulda/normal")):

    # identifica a condição normal e recupera o nome do arquivo como rotaçao
    data = {'defeito': 'normal',
            'severidade': 0,
            'rotacao': float(rotation[:-4]) }
    

    # extrai características (toma muito tempo!)
    features = extract_features("mafaulda/normal/" + rotation)
    data.update(features)

    # exibe barra de status para o usuário
    print_status_bar(i/48)

    # adiciona o novo dado ao dataframe
    df = df.append(data, ignore_index=True)
    

print('\n    Execução em {:.3f} segundos\n'.format(time.time()-instance_time))


# Exibe o resumo dos dados
df.info()


# (sobre-)escreve um cvs com todos os dados
f = open("data.csv", "w")
df.to_csv(f, line_terminator='\n', index=False)
f.close()
print('Dados salvos em: data.csv')


# Exibe o tempo total de execução ao usuário
total_duration = time.time()-start_time
print('\nExecução total em {} minutos e {:.3f} segundos'.format(
      int(total_duration//60), total_duration % 60))
