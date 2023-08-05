#!/anaconda3/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Root_Finding Algorithm
Created on Thu Nov 14 13:56:17 2019
"""

from DualNumber import DualNumber
import ElementaryFunctions as EF

"""
Demo code to find root of an arbitrary function based on our AD framework
"""
def Given_function(x):
    x=DualNumber(x);
    y=EF.Sin(x)*EF.Cos(x)*EF.Tan(x)-EF.Exp(x)*EF.Log(x)*EF.Sqrt(x)*2
    return y #y=sin(x)cos(x)tan(x)-2exp(x)log(x)sqrt(x)
x0=1.2#Initialization of root finding algorithm
Max_iter=int(1e4) #Maximum amout of iterations before stop
Threshold=1e-12;
x=x0
for i in range(Max_iter):
    Current_value=Given_function(x).val
    current_slope=Given_function(x).der
    delta_X=-Current_value/current_slope
    if abs(delta_X)<Threshold:
        break
    else:
        x=x+delta_X
print('The found root of 0=sin(x)cos(x)tan(x)-2exp(x)log(x)sqrt(x) is', x)
print('The numerical solution given by other software is 1.132182161975462')