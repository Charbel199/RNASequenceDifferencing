import differencing
import editScript
import numpy as np

A = 'zzz'
B = 'abddc'
distArr = differencing.differenceCalculation(A,B)
differencing.prettyPrint(A,B,distArr)
editScripts = editScript.getEditScripts(distArr, A, B)

for editScript in editScripts:
    print(editScript)
