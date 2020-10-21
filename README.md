# PG-DefeitosRotores

Projeto de Graduação em Engenharia Mecânica na UFES, 2020

Aqui você encontra os módulos que foram usados no trabalho. O texto será disopnibilizado assim que for entregue e aprovado pela banca.

## Objetivo

Processamento de sinais de vibração, extração de features no domínio da frequência e treinamento de modelo de regressão para predição de severidade para cada defeito do conjunto mecânico. Os defeitos analisados serão:

* Desbalanceamento
* Desalinhamento horizontal
* Desalinhamto vertical

## Base de dados utilizada

Para o meu trabalho, será utilizada a base de dados [MAFAULDA](http://www02.smt.ufrj.br/~offshore/mfs/page_01.html#SEC1). A base não está presente no repositório. Ela deve ser baixada e descompactada em uma pasta nomeada 'mafaulda' dentro do diretorio raiz. Mais especificamente, nesta pasta devem estar presentes as condições 'normal', 'horizontal-misalignment', 'vertical-misalignment' e 'imbalance'. Montado e carregado o diretório, a extração é feita automaticamente pela execução do script [extract_data.py](extract_data.py). Será gerado o arquivo [data.csv](data.csv) com as características extraídas.

Se o seu objetivo for prontamente desenvolver modelos ML em cima das mesma base e com as mesmas características, as etapas anteriores não serão necessárias. Basta utilizar imediatamente o arquivo [data.csv](data.csv). No entanto, é encorajado a interação com o script, sujestões de melhoria e eventuais acréscimos de features.

![Exemplo de carregamento](https://media.giphy.com/media/qreDqbIdpIINndTqZ2/giphy.gif)
