import differencing
import numpy as np

A = 'ZZZ'
B = 'QWEOIAI'
distArr = differencing.differenceCalculation(A,B)
differencing.prettyPrint(A,B,distArr)