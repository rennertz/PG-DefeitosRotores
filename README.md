# PG-DefeitosRotores

Este é um projeto de Graduação em Engenharia Mecânica na UFES, ano 2021.

Aqui você encontra os módulos python para o trabalho da base de dados, o dataset gerado e minhas análises em notebook jupyter no [**nbviwer do projeto**](https://nbviewer.jupyter.org/github/rennertz/PG-DefeitosRotores/blob/main/homepage.ipynb). O texto final será disponibilizado assim que for entregue e aprovado pela banca de conclusão de curso.

## Objetivo

A partir de algoritmos de aprendizado de máquina (ML), busca-se identificar e avaliar defeitos em maquinas industriais a partir de sinais de vibração. As categorias de falha analisados serão:

* Desbalanceamento;
* Desalinhamento horizontal; e
* Desalinhamento vertical.

Dos sinais de vibração, será feita a extração de características no domínio do tempo e da frequência. Avaliará-se a suficiência destas características para a determinação do estado de operação do conjunto mecânico, composto de um motor acoplado a um eixo com rotor.

## Base de dados utilizada

Para este trabalho, será utilizada a base de dados [MaFaulDa](http://www02.smt.ufrj.br/~offshore/mfs/page_01.html#SEC1). Se o objetivo do leitor for prontamente desenvolver modelos ML em cima das mesma base e com as mesmas características extraídas, basta utilizar o arquivo pronto [data.csv](data.csv). No entanto, é encorajada a interação com os scripts do repositório. Você poderá fazer sugestões de melhoria e eventuais acréscimos de features.

### Gerando a matriz de características localmente (via script)

Note que a base MaFaulda não está presente no repositório. Ela deve ser baixada e descompactada na pasta `mafaulda` no diretório raiz. Nesta pasta devem estar presentes ao menos as subpastas `normal`, `horizontal-misalignment`, `vertical-misalignment` e `imbalance`, que são as condições estudadas. Montado e carregado o diretório, basta executar o script [extract_data.py](scripts/extract_data.py) e o arquivo com as características *data.csv* será sobrescrito. Abaixo uma pré-visualização do script sendo executado.

![Exemplo de carregamento](https://media.giphy.com/media/qreDqbIdpIINndTqZ2/giphy.gif)

Para verificar as características extraídas, acesse [feat_functions.py](scripts/feat_functions.py)
