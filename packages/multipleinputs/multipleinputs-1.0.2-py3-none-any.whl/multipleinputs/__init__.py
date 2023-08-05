
"""
Params:

datatype: the datatype in which the input is parsed to. default: 'str'
sep: the separator between different console inputs. default: ' '
"""

import numpy as np

def mul_input(sep=' ',datatype='str'):
    return np.array(input("input separated by space:").split(sep)).astype(datatype)


