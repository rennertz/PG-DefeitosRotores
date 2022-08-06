<p align=center>
<img alt="capa do repositório" src=https://user-images.githubusercontent.com/61323046/183258464-9c961e87-558f-477d-92d8-9882aac2a1b3.png>
</p>

# PG-DefeitosRotores

## Descrição

Este é o meu Projeto de Graduação em Engenharia Mecânica na UFES, defendido no ano 2021. No [**texto**](https://raw.githubusercontent.com/rennertz/PG-DefeitosRotores/main/thesis.pdf) apresento a fundamentação, a metodologia, os materiais e os resultados obtidos pelo projeto. Neste repositório há os códigos utilizados e ainda vários experimentos que não entraram no trabalho.

Em resumo, aqui você encontra os [módulos python](src) utlizados no processamento dos dados de vibração, o [dataset](data/data.csv) gerado e minhas análises em notebooks Jupyter elencados [**nesse página**](home.md), confira!

<p align="center">
<img alt="notebook" src="https://user-images.githubusercontent.com/61323046/183263639-daa22040-d5fe-4b12-ad13-d0773bd7859c.gif">
</p>

### Objetivo

Neste projeto de ML foi estudado o diagnóstico automático de falhas em rotores a partir dos dados de vibração, utilizando um classificador SVM linear para um problema com quatro classes dedefeito: 

* Condição normal;
* Desbalanceamento;
* Desalinhamento horizontal; e
* Desalinhamento vertical.

Dos sinais de vibração, foi feita a extração de características no domínio do tempo e da frequência. Avaliou-se o desempenho destas características para a determinação do estado de operação do conjunto mecânico. Também se avaliou se o número de acelerômetros (haviam 6 sinais) poderia ser reduzido sem perda de eficácia no diagnóstico.

## Base de dados utilizada

<p align="center">
<img alt="bancada" style="width:160ox" src="https://user-images.githubusercontent.com/61323046/183263920-b36f2fb2-9c30-4260-9724-5d13951502f1.png">
</p>

Para este trabalho, será utilizada a base de dados [MaFaulDa](http://www02.smt.ufrj.br/~offshore/mfs/page_01.html#SEC1), que por sua vez foi gerada com o equipamento ilustrado acima. Ao invés de se utilizar os sinais brutos de vibração no modelo de ML, prefere-se extrair características relevantes dos sinais de vibração. As características escolhidas neste trabalho geraram o dataset [data.csv](https://raw.githubusercontent.com/rennertz/PG-DefeitosRotores/main/data/data.csv), que contém 880 exemplos. 

### Gerando o dataset localmente (via script)

A base MaFaulda pode ser [baixada](http://www02.smt.ufrj.br/~offshore/mfs/page_01.html#SEC2) e descompactada na pasta `mafaulda` do diretório raiz deste projeto. Nesta pasta devem estar presentes ao menos as subpastas `normal`, `horizontal-misalignment`, `vertical-misalignment` e `imbalance`, que são as condições estudadas. 

Montado o diretório, basta executar o script [main.py](main.py) e o arquivo com as características *data.csv* será sobrescrito.
Para verificar as características extraídas, consulte [features.py](src/features.py).
Abaixo uma pré-visualização da execução script. 

<p align="center">
  <img src="https://media.giphy.com/media/qreDqbIdpIINndTqZ2/giphy.gif" />
</p>

