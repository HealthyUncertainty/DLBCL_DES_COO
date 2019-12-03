# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:34:59 2019

@author: icromwell
"""

class ClinicalPrescription:
    def __init__(self, params):
        self._params = params
    
    def Process(self, entity):
        if hasattr(entity, 'recurrence') == False:
            entity.recurrence = 0
            
        if entity.recurrence == 0:
            entity.time_Recurrence = entity.allTime + entity.TTE['CRtoFail']
            entity.time_DeadofDisease = entity.allTime + entity.TTE['CRtoDeath']
            entity.stateNum = 3.0
            entity.currentState = "3.0 - Entity undergoing first-line treatment"
        elif entity.recurrence == 1:
            # Entity does not experience second recurrence
            entity.time_Recurrence = 77777
            entity.time_DeadofDisease = entity.allTime + entity.TTE['FailtoDeath']
            entity.stateNum = 6.0
            entity.currentState = "6.0 - Entity undergoing second-line treatment"