BASE DE DADOS MÁQUINA ROTATIVA (ROTORKIT)

Medições sem defeito: 49
Medições com Desbalanceamento do rotor: 333
Medições com Desalinhamento vertical: 301
Medições com Desalinhamento horizontal: 197
Medições com Mancais defeituosos não invertidos: 558
Medições com Mancais defeituosos invertidos: 513
TOTAL MEDIÇÕES: 1951


O nome de cada arquivo corresponde ao tipo de defeito 
Por exemplo, o arquivo desal_H_0,5mm.mat corresponde aos sinais com desalinhamento horizontal de 0,5 mm. 

normal:		sem defeito
desal_H:	desalinhamento horizontal 
desal_V: 	desalinhamento vertical
desbal: 	desbalanceamento
mancal_1_I	Mancal defeituoso número 1 na posição invertida (exterior)
mancal_2_I	Mancal defeituoso número 2 na posição invertida (exterior)
mancal_3_I	Mancal defeituoso número 3 na posição invertida (exterior)
mancal_1_n_I	Mancal defeituoso número 1 na posição não invertida (interior)
mancal_2_n_I	Mancal defeituoso número 2 na posição não invertida (interior)
mancal_3_n_I	Mancal defeituoso número 3 na posição não invertida (interior)


Os arquivos estão em formato struct do MATLAB. A última coluna ("ch") do struct contém os sinais da máquina, sendo matrizes de tamanho 250000x8 

As 8 colunas correspondem a:

COLUNA 1: SINAL DO TACOMETRO (permite estimar a frequência de rotação da máquina)
COLUAS 2-4: SINAIS DOS ACELERÓMETRO DO MANCAL INTERNO (nas direções, axial, radial e tangencial)
COLUNAS 5:7: SINAIS DO ACELERÓMETRO TRIAXIAL DO MANCAL EXTERNO (nas direções axial, radial e tagencial)
COLUNA 8: SINAL CORRESPONDENTE AO MICROFONE

Os sinais foram adquiridos com uma taxa de aquisição de 
50.000 amostras durante 5 segundos, totalizando 250.000 amostras (linhas para cada coluna)

Para maiores informações consultar a monografia:

http://monografias.poli.ufrj.br/monografias/monopoli10012506.pdf


Rafael Zambrano López
rafael.lopez@smt.ufrj.br
