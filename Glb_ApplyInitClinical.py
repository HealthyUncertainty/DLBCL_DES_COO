# -*- coding: utf-8 -*-
"""
Apply initial clinical characteristics to a newly-created entity
"""

############################################################################################
# Load some necessary packages and functions
import random
############################################################################################

class ApplyInitClinical:
    def __init__(self, params):
        self._params = params
        self.probGCB = params['Clin_COO_GCB']
        self.probABC = params['Clin_COO_ABC']
        self.probUndef = params['Clin_COO_Undef']
        self.probDhit = params['Clin_COO_Dhit']

    def Process(self, entity):
        # Draw random value to assign COO subgroup
        COOprob = random.random()
        if COOprob <= self.probGCB:
            entity.COO = 'GCB'              
        elif COOprob <= self.probGCB + self.probABC:
            entity.COO = 'ABC'
        elif COOprob <= self.probGCB + self.probABC + self.probUndef:
            entity.COO = 'Undef'          
        elif COOprob <= self.probGCB + self.probABC + self.probUndef + self.probDhit:
            entity.COO = 'Dhit'
            
        if hasattr(entity, 'COO') == True:
            entity.stateNum = 0.2
            entity.currentState = 'Entity characteristics applied - undergoing diagnosis'
        else:
            print("ERROR - Something has gone wrong in 'ApplyInitClinical.py'")
            entity.stateNum = 99
            entity.currentState = "ERROR - Something has gone wrong in 'ApplyInitClinical.py'"

