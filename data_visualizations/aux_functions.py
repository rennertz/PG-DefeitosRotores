# funções auxiliares pra análise de variáveis e análise de modelos
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def gera_corr_df(defect_name, df_original, df_normalized, feat_to_eixo, feat_to_type):
    # calcula correlações
    corr = df_original.corr()['severidade']
    # exclui informações não relevantes
    corr = corr.drop(['severidade', 'fundamental', 'fundamental_aprox'])
    corr = corr.to_frame('correlacao')
    corr['normalizado'] = False

    # calcula correlações
    corrnorm = df_normalized.corr()['severidade']
    # exclui informações não relevantes
    corrnorm = corrnorm.drop(['severidade', 'fundamental', 'fundamental_aprox'])
    corrnorm = corrnorm.to_frame('correlacao')
    corrnorm['normalizado'] = True

    corr = pd.concat([corr, corrnorm])

    # recupera nome das features como valores, não como index
    corr.reset_index(inplace=True)
    corr = corr.rename(columns = {'index':'feature'})
    # atribui eixo
    corr['eixo'] = corr['feature'].map(feat_to_eixo)
    # atribui categoria
    corr['categoria'] = corr['feature'].map(feat_to_type)
    # guarda sinal da correlação e torna todas positivas
    corr['positiva'] = corr['correlacao'].apply(lambda x: x>0)
    corr['correlacao'] = corr['correlacao'].abs()
    # classifica como desejado
    corr['normalizado'] = ~corr['normalizado']
    corr = corr.sort_values(ascending=False, by=['eixo', 'normalizado', 'correlacao'])
    corr['normalizado'] = ~corr['normalizado']

    return corr

def plot_correlations(corr):
    # gera plot 1
    fig, axs = plt.subplots(1, 4, figsize=(16,6), sharex=True)
    for i, eixo in enumerate(['radial', 'tangente', 'axial', 'microfone']):
        sns.barplot(y='feature', x='correlacao', data=corr.query('normalizado == False and eixo == "{}" '.format(eixo)),
                    orient='h', ax=axs[i], palette="viridis")
        axs[i].set_title('eixo ' + eixo)
    plt.suptitle('Correlação em cada eixo')
    plt.tight_layout()

    # gera plot 2
    fig, axs = plt.subplots(1, 4, figsize=(16,6), sharex=True)
    for i, eixo in enumerate(['radial', 'tangente', 'axial', 'microfone']):
        sns.barplot(y='feature', x='correlacao', data=corr.query('eixo == "{}" '.format(eixo)), 
                orient='h', ax=axs[i], hue='normalizado')
        axs[i].set_title('eixo ' + eixo)

    plt.suptitle('Ganho ao normalizar por eixo')
    plt.tight_layout()


def plot_detailed_comparisson(feature, defect_name, df_original, df_normalized):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=False, figsize=(20,5))
    fig.suptitle('Variação de "'+ defect_name +'" em relação a "' + feature + '"')

    sns.pointplot(data = df_original, x = 'severidade',
                  y = feature, hue = 'fundamental_aprox', ax=ax1)
    sns.pointplot(data = df_normalized, x = 'severidade',
                  y = feature, hue = 'fundamental_aprox', ax=ax2)

    ax1.set_title('Não normalizado')
    ax2.set_title('Normalizado')
    
    plt.show()

# automatiza plot do slopegraph
def plot_change_correlation(defect_type, df_original, df_normalized, decrescente=False, ax=None, cut=3, **plt_kwargs):

    corr = df_original.corr().abs()['severidade']
    corr = corr.drop(['severidade', 'fundamental', 'fundamental_aprox']).rename('original')

    corr_norm = df_normalized.corr().abs()['severidade']
    corr_norm = corr_norm.drop(['severidade', 'fundamental', 'fundamental_aprox']).rename('normalizado')

    compare = pd.concat([corr, corr_norm], axis=1)
    compare['diff'] = compare['normalizado'] - compare['original']
    compare = compare.sort_values('diff', ascending=decrescente)
    compare = compare.iloc[:cut]
    compare.pop('diff')

    sns.axes_style("white")
    if ax is None:
        ax = plt.gca()
    
    for i, feature in enumerate(compare.index):
        sns.lineplot(x=['1 original', '2 normalizado'], y=compare.iloc[i], color='black', marker='o', ax=ax)
        ax.text(-0.3, compare.iloc[i, 0], "{:.2f}".format(compare.iloc[i, 0]), fontsize=12)
        ax.text(1.05, compare.iloc[i, 1], "{:.2f}  {}".format(compare.iloc[i, 1], feature), fontsize=12)

    # Removendo o eixo y
    ax.axes.get_yaxis().set_visible(False)

    # Removendo os eixos
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_title(defect_type, fontsize=20)

    # Exibindo o gráfico
    plt.tight_layout()
