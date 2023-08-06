from rpy2.robjects.vectors import DataFrame, FloatVector, IntVector, StrVector, ListVector
import numpy
from collections import OrderedDict

def recurList(data):
    rDictTypes = [ DataFrame,ListVector]
    rArrayTypes = [FloatVector,IntVector]
    rListTypes=[StrVector]
    if type(data) in rDictTypes:
        return OrderedDict(zip(data.names, [recurList(elt) for elt in data]))
    elif type(data) in rListTypes:
        return [recurList(elt) for elt in data]
    elif type(data) in rArrayTypes:
        return numpy.array(data)
    else:
        if hasattr(data, "rclass"): # An unsupported r class
            raise KeyError('Could not proceed, type {} is not defined'.format(type(data)))
        else:
            return data # We reached the end of recursion
