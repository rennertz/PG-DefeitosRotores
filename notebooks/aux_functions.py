# funções auxiliares pra análise de variáveis e análise de modelos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.metrics as metrics

#%% Análise de variáveis

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



# %% Análise de modelos

# criará lista com a fundamental discretizada de acordo com a dezena arredondada
def discretizar_fundamental(data_in, feature_list):
    # enconta a posição da fundamental no np.array
    fundamental_list = data_in[:, feature_list.index('fundamental')]

    # cria bins e mapeia fundamentals de acordo
    bins = [0, 15, 25, 35, 45, 55, 65]
    fundamental_decimal = np.digitize(fundamental_list, bins)

    # retorna np.array com as dezenas
    return fundamental_decimal*10 


# retornará o DataFramde com resultados, long-form data
def gera_df_resultados(test_data, feature_list, prediction, real):
    error = prediction - real

    disc_rot = list(discretizar_fundamental(test_data, feature_list))

    resultados = pd.DataFrame({
        'real':        real.tolist(), 
        'pred':  prediction.tolist(), 
        'erro':       error.tolist(), 
        'rotacao_discreta': disc_rot,
    })

    return resultados


def gera_df_metricas(prediction, real, modelo=None):
    dados = {
        'modelo': [modelo],
        'R2':                      metrics.r2_score(real, prediction), 
        'MSE':           metrics.mean_squared_error(real, prediction),
        'RMSE': np.sqrt(metrics.mean_squared_error(real, prediction)),
        'MAE':          metrics.mean_absolute_error(real, prediction),
    }

    return pd.DataFrame(dados)


# produzirá plot padrão, com comparação, erros e histograma
def plota_resultados(results, model_id, fault):
    # cria figura e eixos
    fig, axs = plt.subplots(1, 3, figsize=(15,4))

    fig.suptitle(model_id)
    axs[0].set_ylabel('predição')
    axs[0].set_title('Severidade real x predita')

    axs[1].set_ylabel('erro')
    axs[1].set_title('Severidade real x erro')
    
    axs[2].set_ylabel('frequência')
    axs[2].set_title('histograma do Erro')

    # plota linhas com intervalos de 95% de confiança,
    # real x predito
    sns.lineplot(data=results, x='real', y='pred', ax=axs[0])
    axs[0].axline([0,0], slope=1, dashes=(5, 2))
    # real x erro
    sns.lineplot(data=results, x='real', y='erro', ax=axs[1])
    axs[1].axline([0,0], slope=0, dashes=(5, 2))
    
    # adiciona linhas de referência
    if fault == 'desbalanceamento':
        axs[0].set_xlim(0,35)
        axs[0].set_ylim(0,35)

    else: #imbalance
        axs[0].set_xlim(0,2)
        axs[0].set_ylim(0,2)
    
    #adiciona hiostograma e títulos
    sns.histplot(data=results, x='erro', ax=axs[2])
    plt.tight_layout()

# plotará comparativo real x predito segregado por velocidades
def plota_resultados_segregados(results, model_id, fault=None):
    # plota linhas com intervalos de 95% de confiança,
    g = sns.relplot(data=results, 
                    x='real', y='pred', err_style="bars", col_wrap=3,
                    col='rotacao_discreta', kind="line", height=3, aspect=1)
    g.fig.suptitle(model_id)
    # insere linha de referência
    for i in range(len(g.axes)):
        g.axes[i].axline(xy1=(0, 0), slope=1, color="gray", dashes=(5, 2))
        # assegura escala igual entre eixos
        if fault == 'desbalanceamento':
            g.axes[i].set_xlim(0,35)
            g.axes[i].set_ylim(0,35)
        else: #imbalance
            g.axes[i].set_xlim(0,2)
            g.axes[i].set_ylim(0,2)

    plt.tight_layout()
