import time
from utilities import extract, compress

# inicia a cronometragem
start_time = time.time()


# extrai dados e exibe o resumo
extract.iterate_and_extract()

# gera uma cópia resumida da MAFAULDA
compress.iterate_and_compress()


# exibe o tempo de execução total ao usuário
total_duration = time.time()-start_time
print('\nExecução total em {} minutos e {:.3f} segundos'.format(
        int(total_duration//60), total_duration % 60))