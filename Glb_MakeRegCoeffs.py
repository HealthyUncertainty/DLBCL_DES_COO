# -*- coding: utf-8 -*-
"""
Create a probabilistically-sampled input table for each entity's time-to-event coefficients

@author: icromwell
"""

import numpy
from Glb_Estimates import Estimate

class MakeEstimates:
    def __init__(self, inputs, cohort):
        self._inputs = inputs
        if cohort == 0:
            self.scenario = 'GenPop'
        if cohort == 1:
            self.scenario = 'Under60'
        if cohort == 2:
            self.scenario = 'Over60'
        
    def Process(self, entity):
        regtable = self._inputs
        regout = {}
        for param, value in regtable.items():
            regtest[param] = {}
            for valkey, secvalue in value.items():
                if valkey == self.scenario:
                    regtest[param] = secvalue
    
        entity.regcoeffs = regout

