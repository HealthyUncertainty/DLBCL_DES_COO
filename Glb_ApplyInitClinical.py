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
            entity.COO = 'Undefined'          
        elif COOprob <= self.probGCB + self.probABC + self.probUndef + self.probDhit:
            entity.COO = 'Dhit'
            
        if hasattr(entity, 'COO') == True:
            entity.stateNum = 0.2
            entity.currentState = 'Entity characteristics applied - undergoing diagnosis'
        else:
            print("ERROR - Something has gone wrong in 'ApplyInitClinical.py'")
            entity.stateNum = 99
            entity.currentState = "ERROR - Something has gone wrong in 'ApplyInitClinical.py'"

####################################################
# VARIABLES CREATED IN THIS STEP:
#
#   startAge - the entity's age at the beginning of the model
#   sex - the entity's binary sex (1: female; 0: male)
#   smokeStatus - whether the entity is a never or ever smoker (1: ever; 0: never)
#   alcStatus - whether or not the entity is a heavy alcohol user (1: yes; 0: no)
#   OPLStatus - whether or not the entity has an active OPL (1: yes; 0: no)
#   hasDentist - whether or not the entity has a dentist who performs screening tests (1: yes; 0: no)
#   hasCancer - whether or not the entity has an active cancer (1: yes; 0: no)
#   diseaseDetected - whether or not the entity has a premalignancy or a cancer that has been detected (1: yes; 0: no)
#   cancerDetected - whether or not the entity has a cancer that has been detected (1: yes; 0: no)
#   natHist_deathAge - the age at which the entity will die of natural causes
#   probOPL - the probability that the entity starts the simulation with a premalignancy