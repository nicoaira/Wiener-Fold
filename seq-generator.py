import random
from Bio.SeqUtils import MeltingTemp as mt
from Bio.Seq import Seq


def DNA(lenght):
    return ''.join(random.choice('CGTA') for _ in range(lenght))

seq = Seq(DNA(16))

def EXPAR():
    seq = Seq(DNA(16))
    templateX = seq + 'TGTGAGACTC' + seq + 'T'

    return seq, mt.Tm_NN(seq), templateX, mt.Tm_NN(templateX)

print('Secuencia:', templateX)
print('%0.1f' % mt.Tm_NN(templateX))

print('Trigger X:', seq)
print('%0.1f' % mt.Tm_NN(seq))
