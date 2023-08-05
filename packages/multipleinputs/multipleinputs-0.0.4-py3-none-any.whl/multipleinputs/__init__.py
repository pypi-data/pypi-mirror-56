import numpy as np

def mul_input(datatype=str,sep=' '):
    return np.array(input("input separated by space:").split(sep)).astype(datatype)


