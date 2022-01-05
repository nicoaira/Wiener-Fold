import random
from Bio.SeqUtils import MeltingTemp as mt
from Bio.Seq import Seq


def DNA(lenght, gc):

    GC = gc
    GC = (GC - 0.0093) / 0.9712
    AT = 1 - GC

    bases = ['A', 'T', 'C', 'G']


    contador_G = 0
    contador_C = 0
    contador_A = 0
    contador_T = 0

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



    return ''.join(seq)

def EXPAR(lenght, gc):
    seq = Seq(DNA(lenght, gc))
    templateX = seq + 'TGTGAGACTC' + seq + 'T'
    return seq, mt.Tm_NN(seq), templateX, mt.Tm_NN(templateX)
