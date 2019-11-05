# -*- coding: utf-8 -*-
"""
Create a probabilistically-sampled input table for each entity. This allows us
to perform EVPPI.

@author: icromwell
"""

import numpy
from Glb_Estimates import Estimate

class MakeEstimates:
    def __init__(self, inputs):
        self._inputs = inputs
        
    def Process(self, entity):
        # Dirichlet-distributed variables are handled separately from others
        ptable = [(x[0], x[1].sample()) for x in self._inputs.__dict__.items() if isinstance(x[1], Estimate) and x[1].type != 5]
        diritable = [(x[0], x[1]) for x in self._inputs.__dict__.items() if isinstance(x[1], Estimate) and x[1].type == 5]
                
        parameter = {}
        for param, value in ptable:
            parameter[param] = value
            
        maxnum = diritable[len(diritable)-1][1].varnum  # Number of dirichlet variables in table
        dirivars = []
        for num in range(0,maxnum+1):
            diri_list = [x for x in diritable if x[1].varnum == num]
            diri_names = [x[0] for x in diri_list]
            diri_values = [x[1].mean for x in diri_list]
            dirich = numpy.random.dirichlet(diri_values)
            for i in range(0,len(dirich)):
                dirivars.append([diri_names[i], dirich[i]])
        
        for param, value in dirivars:
            parameter[param] = value
            
        entity.params = parameter