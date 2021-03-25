import time
from utilities.processes import iterate_and_compress, iterate_and_extract

# inicia a cronometragem
start_time = time.time()

# extrai características, salva data.csv e exibe o resumo
iterate_and_extract()

# opcional para gerar plot waterfall 
# gera uma cópia resumida da MAFAULDA
# iterate_and_compress()

# exibe o tempo de execução total ao usuário
total_duration = time.time()-start_time
print('\nExecução total em {} minutos e {:.3f} segundos'.format(
        int(total_duration//60), total_duration % 60))