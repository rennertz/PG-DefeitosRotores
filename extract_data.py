#
# Código responsável por estruturar o dataset PRINCIPAL do projeto
#
# Este dataset deve conter TODAS as características julgadas 
# relevantes para o terinamento do modelo ML
#

# NOTICE
#  - Para (sobre-)escrever o dataset, descomente as linhas 124-126
#  - Para extrair as features, descomente as linhas 56,57, 86,87 
#    e 109,110 (o tempo de execução será superior a 5 min)
#  - Novas features podem ser adicionadas em process_fft.extract_features

import os
import pandas as pd
import numpy as np
from process_fft import extract_features
import sys # para imprimir status de importação

import time # permite marcar o tempo de execução
start_time = time.time()

# Extração dos tipos de defeitos presentes
# defect_type=os.listdir("mafaulda")
# for d in defect_type: print(d)

def print_status_bar(status):
	sys.stdout.write('\r')
	sys.stdout.write('    [{:20}] {:.3f}%'.format(round(status*20)*'=', 100*status))
	sys.stdout.flush()

# Extraindo defeitos de desalinhamento
df_desalinhamento = pd.DataFrame(columns=['defect_type','hor_mis', 'ver_mis', 'rot_vel'])
for defeito in ['horizontal-misalignment', 'vertical-misalignment']:
	print('\nCarregando desalinhamento {}'.format(defeito.split('-')[0]))
	instance_time = time.time()

	for i, desalinhamento in enumerate(os.listdir("mafaulda/{}".format(defeito))):
		# para cada valor de desalinhamento
		for j, velocidade in enumerate(os.listdir("mafaulda/{}/{}".format(defeito, desalinhamento))):
			# para cada valor de velocidade de rotação
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
			#features = extract_features("mafaulda/{}/{}/{}".format(defeito, desalinhamento,velocidade))
			#data.update(features)

			# exibe barra de status para o usuário
			if defeito == 'horizontal-misalignment':
				print_status_bar((i+j/48)/4)
			elif defeito == 'vertical-misalignment':
				print_status_bar((i+j/49)/6)

			#finalmente, adiciona o novo dado ao dataframe correspondente
			df_desalinhamento = df_desalinhamento.append(data, ignore_index=True)

	print('\n    Execução em {:.3f} segundos'.format(time.time()-instance_time))


# Extraindo defeitos de desbalanceamento
df_desbalanceamento = pd.DataFrame(columns=['defect_type', 'imbalance', 'rot_vel'])
print('\nCarregando desbalanceamento')
instance_time = time.time()

for i, desbalanceamento in enumerate(os.listdir("mafaulda/imbalance")):
	# para cada valor de desbalanceamento
	for j, velocidade in enumerate(os.listdir("mafaulda/imbalance/{}".format(desbalanceamento))):
		# para cada valor de velocidade de rotação
		# formatar e inserir os valores de desbalanceamento e de velocidade
		data = {'defect_type': 'imbalance',
				'imbalance': desbalanceamento[:-1],
				'rot_vel': velocidade[:-4]}

		# fase de extração de características (toma muito tempo!)
		#features = extract_features("mafaulda/imbalance/{}/{}".format(desbalanceamento, velocidade))
		#data.update(features)

		# exibe barra de status para o usuário
		print_status_bar((i+j/48)/7)

		#finalmente, adiciona o novo dado ao dataframe correspondente
		df_desbalanceamento = df_desbalanceamento.append(data, ignore_index=True)
print('\n    Execução em {:.3f} segundos'.format(time.time()-instance_time))


# Extraindo rotações para funcionamento normal
df_normal = pd.DataFrame(columns=['defect_type',  'rot_vel'])
print('\nCarregando condição normal')
instance_time = time.time()

for i, velocidade in enumerate(os.listdir("mafaulda/normal")):
	# para cada valor de velocidade de rotação
	# formatar e inserir os valores de desalinhamento e de velocidade
	data = {'defect_type': 'normal',
			'rot_vel': velocidade[:-4]}

	# fase de extração de características (toma muito tempo!)
	#features = extract_features("mafaulda/normal/{}".format(velocidade))
	#data.update(features)

	# exibe barra de status para o usuário
	print_status_bar(i/48)

	#finalmente, adiciona o novo dado ao dataframe correspondente
	df_normal = df_normal.append(data, ignore_index=True)

print('\n    Execução em {:.3f} segundos\n'.format(time.time()-instance_time))


# Junta todos os DF de todos os defeitos e exibe o resumo
df_all = pd.concat([df_normal,df_desalinhamento, df_desbalanceamento])
df_all.info()

# (sobre-)escreve um cvs com todos os dados
#f = open("data.csv", "w")
#df_all.to_csv(f,line_terminator='\n',index=False)
#f.close()

total_duration = time.time()-start_time
print('\nExecução total em {} minutos e {:.3f} segundos'.format(int(total_duration//60),total_duration%60))