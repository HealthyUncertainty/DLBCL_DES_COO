# -*- coding: utf-8 -*-
"""
Create a diagnostic test based on user-defined attributes

@author: icromwell
"""

class MakeTest:
    def __init__(self, testchars):
        self._testchars = testchars
        
    def Process(self):
        diag_test = {}
        for param in self._testchars:
            name = param[0]
            attribute = param[1]
            typeno = int(param[2])
            level = param[3]
            value = float(param[4])
            if typeno == 1 and value == 1:
                diag_test[name] = {'type': typeno, 'attribute': attribute, 'level': level}
            elif typeno == 1:
                pass
            elif typeno == 0:
                diag_test[name] = {'type': typeno, 'attribute': attribute, 'level': value}
            elif typeno == None:
                diag_test[name] = {'type': 0, 'attribute': attribute, 'level': value}
            elif level == None:
                diag_test[name] = {'type': typeno, 'attribute': attribute, 'level': value}
            else:
                print("Invalid 'TypeNo' and/or 'Level' Please ensure that the 'TestChars' sheet in 'InputParameters.xlsx' is completed properly")
        return(diag_test)