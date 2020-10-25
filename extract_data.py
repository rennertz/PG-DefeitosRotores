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


def print_status_bar(status):
    sys.stdout.write('\r')
    sys.stdout.write('    [{:20}] {:.3f}%'.format(
                     round(status*20)*'=', 100*status))
    sys.stdout.flush()


# Extraindo defeitos de desalinhamento
df_desalinhamento = pd.DataFrame(columns=['defect_type', 'hor_mis', 'ver_mis', 'rot_vel'])
# códigos para desalinhamento horizontal e vertical foram reunidos para evitra repetição
for defeito in ['horizontal-misalignment', 'vertical-misalignment']:
    print('\nCarregando desalinhamento', defeito.split('-')[0])
    instance_time = time.time()

    # para cada valor de desalinhamento
    for i, desalinhamento in enumerate(os.listdir("mafaulda/" + defeito)):
        # para cada valor de velocidade de rotação
        for j, velocidade in enumerate(os.listdir("mafaulda/" + defeito + '/' + desalinhamento)):
            
            # formatar e inserir os valores de desalinhamento e de velocidade
            if defeito == 'horizontal-misalignment':
                data = {'defect_type': 'hor_mis',
                        'hor_mis': desalinhamento[:-2],
                        'ver_mis': np.NaN,
                        'rot_vel': velocidade[:-4]}

            elif defeito == 'vertical-misalignment':
                data = {'defect_type': 'ver_mis',
                        'hor_mis': np.NaN,
                        'ver_mis': desalinhamento[:-2],
                        'rot_vel': velocidade[:-4]}

            # fase de extração de características (toma muito tempo!)
            features = extract_features("mafaulda/{}/{}/{}".format(
                                        defeito, desalinhamento, velocidade))
            data.update(features)

            # exibe barra de status para o usuário (de acordo com o tipo de desalinhamento)
            if defeito == 'horizontal-misalignment':
                print_status_bar((i+j/48)/4)
            elif defeito == 'vertical-misalignment':
                print_status_bar((i+j/49)/6)

            # finalmente, adiciona o novo dado ao dataframe correspondente
            df_desalinhamento = df_desalinhamento.append(data, ignore_index=True)

    print('\n    Execução em {:.3f} segundos'.format(
          time.time()-instance_time))


# Extraindo defeitos de desbalanceamento
df_desbalanceamento = pd.DataFrame(columns=['defect_type', 'imbalance', 'rot_vel'])
print('\nCarregando desbalanceamento')
instance_time = time.time()

# para cada valor de desbalanceamento
for i, desbalanceamento in enumerate(os.listdir("mafaulda/imbalance")):
    # para cada valor de velocidade de rotação
    for j, velocidade in enumerate(os.listdir("mafaulda/imbalance/" + desbalanceamento)):
        # formatar e inserir os valores de desbalanceamento e de velocidade
        data = {'defect_type': 'imbalance',
                'imbalance': desbalanceamento[:-1],
                'rot_vel': velocidade[:-4]}

        # fase de extração de características (toma muito tempo!)
        features = extract_features("mafaulda/imbalance/{}/{}".format(
                                    desbalanceamento, velocidade))
        data.update(features)

        # exibe barra de status para o usuário
        print_status_bar((i+j/48)/7)

        # finalmente, adiciona o novo dado ao dataframe correspondente
        df_desbalanceamento = df_desbalanceamento.append(data, ignore_index=True)
print('\n    Execução em {:.3f} segundos'.format(time.time()-instance_time))


# Extraindo rotações para funcionamento normal
df_normal = pd.DataFrame(columns=['defect_type',  'rot_vel'])
print('\nCarregando condição normal')
instance_time = time.time()

# para cada valor de velocidade de rotação
for i, velocidade in enumerate(os.listdir("mafaulda/normal")):
    # formatar e inserir os valores de desalinhamento e de velocidade
    data = {'defect_type': 'normal',
            'rot_vel': velocidade[:-4]}

    # fase de extração de características (toma muito tempo!)
    features = extract_features("mafaulda/normal/{}".format(velocidade))
    data.update(features)

    # exibe barra de status para o usuário
    print_status_bar(i/48)

    # finalmente, adiciona o novo dado ao dataframe correspondente
    df_normal = df_normal.append(data, ignore_index=True)

print('\n    Execução em {:.3f} segundos\n'.format(time.time()-instance_time))


# Junta todos os DF de todos os defeitos e exibe o resumo
df_all = pd.concat([df_normal, df_desalinhamento, df_desbalanceamento])
df_all.info()

# (sobre-)escreve um cvs com todos os dados
f = open("data.csv", "w")
df_all.to_csv(f, line_terminator='\n', index=False)
f.close()

total_duration = time.time()-start_time
print('\nExecução total em {} minutos e {:.3f} segundos'.format(
      int(total_duration//60), total_duration % 60))
