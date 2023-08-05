import numpy as np

def mul_input(sep=' ',datatype=str):
    return np.array(input("input separated by space:").split(sep)).astype(datatype)


