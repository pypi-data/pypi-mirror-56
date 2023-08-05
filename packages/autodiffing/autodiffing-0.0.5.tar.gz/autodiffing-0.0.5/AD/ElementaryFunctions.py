#!/anaconda3/bin/python
# -*- coding: utf-8 -*-

from AD.DualNumber import DualNumber
import numpy as np

def Sin(x):
    '''
    >>> print(Sin(DualNumber(5,1)))
    Derivative: 0.28
    Value: -0.96
    '''
    if data_type_check(x) == 0:
        return DualNumber(np.sin(x._val),np.cos(x._val)*x._der)
    else:
        return DualNumber(np.sin(x),0)

    
def Tan(x):
    '''
    >>> print(Tan(DualNumber(5,1)))
    Derivative: 12.43
    Value: -3.38
    '''
    if data_type_check(x) == 0:
        return DualNumber(np.tan(x._val),(1+np.tan(x._val)*np.tan(x._val))*x._der)
    else:
        return DualNumber(np.tan(x),0)


def Cos(x):
    '''
    >>> print(Cos(DualNumber(5,1)))
    Derivative: 0.96
    Value: 0.28
    '''
    if data_type_check(x) == 0:
        return DualNumber(np.cos(x._val),-1*np.sin(x._val)*x._der)
    else:
        return DualNumber(np.cos(x),0)

def Exp(x):
    '''
    >>> print(Exp(DualNumber(5,1)))
    Derivative: 148.41
    Value: 148.41
    '''
    if data_type_check(x) == 0:
        return DualNumber(np.exp(x._val),np.exp(x._val)*x._der)
    else:
        return DualNumber(np.exp(x),0)

def Power(x,n):
    '''
    >>> print(Power(DualNumber(5,1),2))
    Derivative: 10.00
    Value: 25.00
    '''
    if data_type_check(x) == 0:
        return DualNumber(x._val**n,n*(x._val**(n-1))*x._der)
    else:
        return DualNumber(x**n,0)

def Log(x):
    '''
    >>> print(Log(DualNumber(5,1)))
    Derivative: 0.20
    Value: 1.61
    '''
    if data_type_check(x) == 0:
        return DualNumber(np.log(x._val),(1/x._val)*x._der)
    else:
        return DualNumber(np.log(x),0)

        
def ArcSin(x):
    '''
    >>> print(ArcSin(DualNumber(0.5)))
    Derivative: 1.15
    Value: 0.52
    '''
    if data_type_check(x) == 0:
        return DualNumber(np.arcsin(x._val),1/np.sqrt(1-x._val**2) * x._der)
    else:
        return DualNumber(np.arcsin(x),0)


def ArcCos(x):
    '''
    >>> print(ArcCos(DualNumber(0.5)))
    Derivative: -1.15
    Value: 1.05
    '''
    if data_type_check(x) == 0:
        return DualNumber(np.arccos(x._val),-1/np.sqrt(1-x._val**2) * x._der)
    else:
        return DualNumber(np.arccos(x),0)
            
def ArcTan(x):
    '''
    >>> print(ArcTan(DualNumber(0.5)))
    Derivative: 0.80
    Value: 0.46
    '''
    if data_type_check(x) == 0:
        return DualNumber(np.arctan(x._val),1/(1+x._val**2) * x._der)
    else:
        return DualNumber(np.arctan(x),0)

def Sqrt(x):
    '''
    >>> print(Sqrt(DualNumber(9,1)))
    Derivative: 0.17
    Value: 3.00
    '''
    if data_type_check(x) == 0:
        return DualNumber(np.sqrt(x._val),1/(2*np.sqrt(x._val)) * x._der)
    else:
        return DualNumber(np.sqrt(x),0)
        
def data_type_check(x):
   try:
       float(x._val)+float(x._der)
       return 0  # returns 0 if x is DualNumber
   except AttributeError:
       try:
           float(x)
           return 1 # returns 1 if x is real
       except:
           raise AttributeError('Input must be dual number or real number!')


if __name__ =="__main__":
    import doctest
    doctest.testmod()
        
