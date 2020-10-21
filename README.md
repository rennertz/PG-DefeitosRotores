# PG-DefeitosRotores

Projeto de Graduação em Engenharia Mecânica na UFES, 2020

Aqui você encontra os módulos que foram usados no trabalho. O texto será disopnibilizado assim que for entregue e aprovado pela banca.

## Objetivo

Processamento de sinais de vibração, extração de features no domínio da frequência e treinamento de modelo de regressão para predição de severidade para cada defeito do conjunto mecânico. Os defeitos analisados serão:

* Desbalanceamento
* Desalinhamento horizontal
* Desalinhamto vertical

## Base de dados utilizada

Para este trabalho, será utilizada a base de dados [MaFaulDa](http://www02.smt.ufrj.br/~offshore/mfs/page_01.html#SEC1). Se o seu objetivo for prontamente desenvolver modelos ML em cima das mesma base e com as mesmas características utilizadas, basta utilizar o arquivo pronto [data.csv](data.csv). No entanto, é encorajada a interação com os scripts do repositório. Você poderá fazer sujestões de melhoria e eventuais acréscimos de features dentro do arquivo [feat_functions.py](feat_functions.py).

### Gerando a matriz de características localmente (via script)

Note que a base MaFaulda não está presente no repositório. Ela deve ser baixada e descompactada em uma pasta nomeada `mafaulda` dentro do diretorio raiz. Nesta pasta devem estar presentes ao menos as subpastas `normal`, `horizontal-misalignment`, `vertical-misalignment` e `imbalance`, que são as condições estudadas. Montado e carregado o diretório, basta executar o script [extract_data.py](extract_data.py) e o arquivo com as características [data.csv](data.csv) será sobrescrito. Abaixo uma previsualização do script sendo executado.

![Exemplo de carregamento](https://media.giphy.com/media/qreDqbIdpIINndTqZ2/giphy.gif)
