import os
import pandas as pd
import numpy as np

# Extração dos tipos de defeitos
defect_type=os.listdir("mafaulda")
# for d in defect_type: print(d)

# Extraindo defeitos de desalinhamento horizontal
hor_mis=os.listdir("mafaulda/horizontal-misalignment")
rot_vel=os.listdir("mafaulda/horizontal-misalignment/{}".format(hor_mis[0]))

# Formatando os valores de desalinhamento e de rotação
hor_mis=[hm[:-2] for hm in hor_mis] 
rot_vel=[rv[:-4] for rv in rot_vel]	

# Criando o dataframe rotacoes
titles = {
	'defect_type': [], 
	'hor_mis': [],
	'rot_vel': []
}
rotacoes = pd.DataFrame(titles)

# alimentando o dataframe rotacoes
data = {
	'defect_type': ['hor-mis']*len(rot_vel), 
	'hor_mis': [0.5]*len(rot_vel),
	'rot_vel': rot_vel
}
df = pd.DataFrame(data)

rotacoes = rotacoes.append(df, ignore_index=True)
print(rotacoes)