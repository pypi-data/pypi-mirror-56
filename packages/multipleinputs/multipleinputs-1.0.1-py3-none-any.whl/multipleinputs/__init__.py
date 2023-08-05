
"""
Params:

datatype: the datatype in which the input is parsed to. default: 'str'
sep: the separator between different console inputs. default: ' '
"""

import numpy as np

def mul_input(datatype='str',sep=' '):
    return np.array(input("input separated by space:").split(sep)).astype(datatype)


