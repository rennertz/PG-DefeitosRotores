#
# Código responsável por estruturar o DataFrame PRINCIPAL do projeto
#
# Este DataFrame deve conter TODAS as características julgadas 
# relevantes para o terinamento do modelo ML
#

# TODO: unir os datafames com regas adequadas. Referência:
#		https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#set-logic-on-the-other-axes


import os
import pandas as pd
import numpy as np
from process_fft import extract_features
import sys # para imprimir status de importação

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
	for i, desalinhamento in enumerate(os.listdir("mafaulda/{}".format(defeito))):
		# para cada valor de desalinhamento
		for velocidade in os.listdir("mafaulda/{}/{}".format(defeito, desalinhamento)):
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

			#features = extract_caracteristics("mafaulda/{}/{}/{}".format(defeito, desalinhamento,velocidade))
			#data.update(features)
			df_desalinhamento = df_desalinhamento.append(data, ignore_index=True)

		if defeito == 'horizontal-misalignment':
			print_status_bar(i/3)
		elif defeito == 'vertical-misalignment':
			print_status_bar(i/5)

# Extraindo defeitos de desbalanceamento
df_desbalanceamento = pd.DataFrame(columns=['defect_type', 'imbalance', 'rot_vel'])

print('\nCarregando desbalanceamento')
for i, desbalanceamento in enumerate(os.listdir("mafaulda/imbalance")):
	# para cada valor de desbalanceamento
	for velocidade in os.listdir("mafaulda/imbalance/{}".format(desbalanceamento)):
		# para cada valor de velocidade de rotação
		# formatar e inserir os valores de desbalanceamento e de velocidade
		data = {'defect_type': 'imbalance',
				'imbalance': desbalanceamento[:-1],
				'rot_vel': velocidade[:-4]}

		#features = extract_features("mafaulda/imbalance/{}/{}".format(desbalanceamento, velocidade))
		#data.update(features)
		df_desbalanceamento = df_desbalanceamento.append(data, ignore_index=True)

	print_status_bar(i/6)


# Extraindo rotações para funcionamento normal
df_normal = pd.DataFrame(columns=['defect_type',  'rot_vel'])

print('\nCarregando condição normal')
for i, velocidade in enumerate(os.listdir("mafaulda/normal")):
	# para cada valor de velocidade de rotação
	# formatar e inserir os valores de desalinhamento e de velocidade
	data = {'defect_type': 'normal',
			'rot_vel': velocidade[:-4]}

	#features = extract_features("mafaulda/normal/{}".format(velocidade))
	#data.update(features)
	df_normal = df_normal.append(data, ignore_index=True)

	print_status_bar(i/48)

print('\n')

#print(df_normal)