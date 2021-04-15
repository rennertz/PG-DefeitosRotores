import time
from src.processes import iterate_and_extract

# inicia a cronometragem
start_time = time.time()

# extrai características, salva data.csv e exibe o resumo
iterate_and_extract(generate_compressed_mafaulda=False)

# OBS:
# generate_compressed mafaulda é opcional 
# a opção gera uma cópia comprimida da MAFAULDA,
# necessária para gerar plot waterfall


# exibe o tempo de execução total ao usuário
total_duration = time.time()-start_time
print('\nExecução total em {} minutos e {:.1f} segundos'.format(
        int(total_duration//60), total_duration % 60))