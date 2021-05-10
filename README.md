# PG-DefeitosRotores

Este é o meu Projeto de Graduação em Engenharia Mecânica na UFES, defendido no ano 2021. No [**texto**](https://raw.githubusercontent.com/rennertz/PG-DefeitosRotores/main/thesis.pdf) é apresentada a fundamentação, a metodologia, os materiais e os resultados. Neste repositório há os códigos utilizados e ainda vários experimentos que não entraram no trabalho.

Em resumo, aqui você encontra os [módulos python](src) utlizados no processamento dos dados de vibração, o [dataset](data/data.csv) gerado e minhas análises em [**notebooks jupyter**](https://nbviewer.jupyter.org/github/rennertz/PG-DefeitosRotores/blob/main/home.ipynb).

## Descrição

Foi desenvolvido um projeto de AM o diagnóstico automático de falhas em rotores a partir dos dados de vibração, utilizando um classificador SVM linear para um problema com quatro classes dedefeito: 

* Condição normal;
* Desbalanceamento;
* Desalinhamento horizontal; e
* Desalinhamento vertical.

Dos sinais de vibração, foi feita a extração de características no domínio do tempo e da frequência. Avaliou-se a suficiência destas características para a determinação do estado de operação do conjunto mecânico. Também se avaliou a possibilidade de redução do número de acelerômetros (haviam 6 sinais) sem perda de eficácia no diagnóstico.

## Base de dados utilizada

Para este trabalho, será utilizada a base de dados [MaFaulDa](http://www02.smt.ufrj.br/~offshore/mfs/page_01.html#SEC1). Para se desenvolver modelos ML, aconselha-se extrair as características mais relevantes dos sinais de vibração, ao invés de utilizá-los de maneira direta. As características utilizadas neste trabalho estão reunidas no arquivo [data.csv](https://raw.githubusercontent.com/rennertz/PG-DefeitosRotores/main/data/data.csv). Sinta-se livre para utliiza-las nos seus testes. Entretanto, encorajo a interação com os scripts deste repositório. Aceito tanto sugestões de melhoria, quanto acréscimos de features.

### Gerando a matriz de características localmente (via script)

A base MaFaulda não está presente no repositório. Ela deve ser baixada e descompactada na pasta `mafaulda` no diretório raiz. Nesta pasta devem estar presentes ao menos as subpastas `normal`, `horizontal-misalignment`, `vertical-misalignment` e `imbalance`, que são as condições estudadas. Montado o diretório, basta executar o script [main.py](main.py) e o arquivo com as características *data.csv* será sobrescrito. Abaixo uma pré-visualização do script sendo executado.

<p align="center">
  <img src="https://media.giphy.com/media/qreDqbIdpIINndTqZ2/giphy.gif" />
</p>

Para verificar as características extraídas, acesse [features.py](src/features.py)
