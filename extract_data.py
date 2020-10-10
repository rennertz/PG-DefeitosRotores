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


# Extração dos tipos de defeitos presentes
# defect_type=os.listdir("mafaulda")
# for d in defect_type: print(d)

# Extraindo defeitos de desalinhamento
df_desalinhamento = pd.DataFrame(columns=['defect_type','hor_mis', 'ver_mis', 'rot_vel'])

for defeito in ['horizontal-misalignment', 'vertical-misalignment']:
	for desalinhamento in os.listdir("mafaulda/{}".format(defeito)):
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

			df_desalinhamento = df_desalinhamento.append(data, ignore_index=True)


# Extraindo defeitos de desbalanceamento
df_desbalanceamento = pd.DataFrame(columns=['defect_type', 'imbalance', 'rot_vel'])

for desbalanceamento in os.listdir("mafaulda/imbalance"):
	# para cada valor de desbalanceamento
	for velocidade in os.listdir("mafaulda/imbalance/{}".format(desbalanceamento)):
		# para cada valor de velocidade de rotação
		# formatar e inserir os valores de desbalanceamento e de velocidade
		data = {'defect_type': 'imbalance',
				'imbalance': desbalanceamento[:-1],
				'rot_vel': velocidade[:-4]}

		df_desbalanceamento = df_desbalanceamento.append(data, ignore_index=True)


# Extraindo rotações para funcionamento normal
df_normal = pd.DataFrame(columns=['defect_type',  'rot_vel'])

for velocidade in os.listdir("mafaulda/normal"):
	# para cada valor de velocidade de rotação
	# formatar e inserir os valores de desalinhamento e de velocidade
	data = {'defect_type': 'normal',
			'rot_vel': velocidade[:-4]}

	df_normal = df_normal.append(data, ignore_index=True)

#print(df_normal)
df_desbalanceamento.info()