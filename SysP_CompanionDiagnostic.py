# -*- coding: utf-8 -*-
"""
A program to add companion diagnostics to COO of interest. If the entity does not
have the COO then they do not receive a companion diagnostic and simply go to
treatment.

@author: icromwell
"""

import random

class CompanionDiagnostic:
    def __init__(self, params):
        self._params = params
        
    def Process(self, entity, scenario, COO):
        entity.compDiag = 0
        entity.getsCompanion = 0
        coolist = []
        # Which COO subgroups are eligible for a companion diagnostic?
        for subgroup, value in COO.items():
            if value == 1:
                coolist.append(subgroup)            
        
        # Will the entity receive a companion diagnostic?
        if scenario == 0:
            # No companion diagnostics in this scenario - do nothing
            entity.getsCompanion = 9
        elif entity.hadNGS == 0:
            # Entity didn't receive an NGS test - do nothing
            pass
        elif entity.COO_diag in coolist:
            # Entity's diagnosed COO is eligible, they will receive it
            entity.compDiag = 1
        else:
            entity.stateNum = 99
            entity.currentState = "ERROR: the entity either does not have an eligible COO, or there is a mismatch between 'entity.COO_diag' (check 'SysP_Diagnosis.py') and 'Scenario_COO' (check 'Sequencer.py')"
        
        if entity.compDiag == 1:
            entity.resources.append(("Companion Diagnostic", entity.allTime))
            getsComp = random.random()
            if getsComp < self._params['Diag_CompanionEligible']:
                # Entity is eligible for experimental treatment
                entity.getsCompanion = 1
        
        entity.time_Sysp = entity.allTime
        entity.stateNum = 2.0
        entity.currentState = "2.0 - Going for clinical prescription"