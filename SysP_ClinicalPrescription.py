# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:34:59 2019

@author: icromwell
"""

class ClinicalPrescription:
    def __init__(self, params, regcoeffs):
        self._params = params
        self._regcoeffs = regcoeffs
    
    def Process(self, entity):
        if hasattr(entity, 'recurrence') == False:
            entity.recurrence = 0
            
        if entity.recurrence == 0:
            entity.time_Recurrence = entity.TTE['CRtoFail']
            entity.time_DeadofDisease = entity.TTE['CRtoDeath']
            entity.stateNum = 3.0
            entity.currentState = "3.0 - Entity undergoing first-line treatment"
        elif entity.recurrence == 1:
            # Entity does not experience second recurrence
            entity.time_Recurrence = 77777
            entity.time_DeadofDisease = entity.TTE['FailtoDeath']
            entity.stateNum = 5.0
            entity.currentState = "5.0 - Entity undergoing second-line treatment"