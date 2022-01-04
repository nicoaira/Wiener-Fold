import random
from Bio.SeqUtils import MeltingTemp as mt
from Bio.Seq import Seq
from random import sample
import pandas as pd


columns = ['gc_objetivo','gc_obtenido']
df = pd.DataFrame(columns = columns)





# def DNA(lenght):
#     return ''.join(random.choice('CGTA') for _ in range(lenght))
#
# seq = Seq(DNA(16))

resultados = []

for gc_objetivo in range(37, 50):


    GC = gc_objetivo/100

    GC = (GC - 0.0093) / 0.9712
    AT = 1 - GC

    bases = ['A', 'T', 'C', 'G']

    gran_seq = ''
    num_seq = 15000

    contador_G = 0
    contador_C = 0
    contador_A = 0
    contador_T = 0

    for j in range(num_seq):
        lenght = 16


        gc_n = GC*lenght
        at_n= AT*lenght


        seq = []

        a_rep = 0
        t_rep = 0
        c_rep = 0
        g_rep = 0



        for i in range(lenght):

            base = ''.join(random.choices(
            bases,
            weights = [
            at_n * (1 - a_rep),
            at_n * (1 - t_rep),
            gc_n * (1 - c_rep),
            gc_n * (1 - g_rep)])
            )


            # Penalize repetitions
            a_rep = 0.03 * (seq[-4:].count('A'))**2
            t_rep = 0.03 * (seq[-4:].count('T'))**2
            c_rep = 0.1 * (seq[-4:].count('C'))**2
            g_rep = 0.1 * (seq[-4:].count('G'))**2





            if base == 'G' or base == 'C' and gc_n-1 > 0:
                gc_n -= 1
            elif base == 'A' or base == 'T' and gc_n-1 > 0:
                at_n -= 1


            seq.append(str(base))



        seq = ''.join(seq)

        gran_seq += seq

        contador_G += seq.count('GGGG')
        contador_C += seq.count('CCCC')
        contador_A += seq.count('AAAA')
        contador_T += seq.count('TTTT')


    print('4G', contador_G*100/num_seq)
    print('4C', contador_C*100/num_seq)
    print('4A', contador_A*100/num_seq)
    print('4T', contador_T*100/num_seq)


    G = gran_seq.count('G')
    C = gran_seq.count('C')
    A = gran_seq.count('A')
    T = gran_seq.count('T')

    print('G', G)
    print('C', C)
    print('A', A)
    print('T', T)

    print('GC% OBTENIDO: ', (G + C)*100/(G+A+C+T))
    print('GC% OBEJETIVO: ', gc_objetivo)
    print('GC% DIFERENCIA: ', gc_objetivo - ((G + C)*100/(G+A+C+T)))

    resultados.append({
    'gc_objetivo': GC,
    'gc_obtenido': (G + C)/(G+A+C+T)
    })

df = pd.DataFrame(resultados)

df.to_csv('gc.csv', index = False)
