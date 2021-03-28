# funções auxiliares pra análise de modelos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.metrics as metrics


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

    resultados = resultados.sort_values(['real', 'rotacao_discreta'])

    return resultados


def gera_df_metricas(prediction, real, modelo=None, regressores=None):
    dados = {
        'modelo': [modelo],
        'dados': [regressores],
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
