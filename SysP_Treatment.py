# -*- coding: utf-8 -*-
"""
A program to describe an entity under active treatment for cancer. They receive a round of treatment and may experience
adverse effects from that treatment. When they reach the maximum number of treatment rounds they move to follow-up.

@author: icromwell
"""
import random

class IncidentCancer:
    def __init__(self, params, regcoeffs):
        self._params = params
        self._regcoeffs = regcoeffs

    def Process(self, entity):
        if hasattr(entity, "cycleNum") == False:
            entity.cycleNum = 0

        # Has entity reached maximum number of cycles allowed?
        maxCycle = self._params['Tx_MaxCycle']
        if entity.cycleNum == maxCycle:
            # Entity is done treatment and now goes to their first follow-up appointment
            entity.events.append(("Completed treatment", entity.allTime))
            entity.stateNum = 3.9
            entity.currentState = "3.9 - Assign recurrence date"

        else:
            # Entity receives a cycle of treatment
            entity.resources.append(("Treatment - Standard Care", entity.allTime))
            entity.utility.append((self._params['Util_Treatment_Standard'], entity.allTime))

            # Does entity experience an adverse event?
            adverse_event = random.random()
            if adverse_event > self._params['Tx_ProbAdverseEvent_Standard']:
                entity.resources.append(("Adverse Event - Standard Care", entity.allTime))
                entity.events.append(("Adverse Event - Standard Care", entity.allTime))
                entity.utility.append((self._params['Util_AdvEvent_Standard'], entity.allTime))

            # If entity has the appropriate COO and NGS testing, they may receive experimental care
            if entity.GEPcare == 1:
                entity.resources.append(("Treatment - GEP-guided Care", entity.allTime))
                entity.utility.append((self._params['Util_Treatment_GEP'], entity.allTime))

                # Does entity experience an adverse event?
                adverse_event = random.random()
                if adverse_event > self._params['Tx_ProbAdverseEvent_GEP']:
                    entity.resources.append(("Adverse Event - GEP-guided Care", entity.allTime))
                    entity.events.append(("Adverse Event - GEP-guided Care", entity.allTime))
                    entity.utility.append((self._params['Util_AdvEvent_GEP'], entity.allTime))

            # Record the number of cycles that have occurred
            entity.cycleNum += 1
            # Advance the system clock to the next appointment time
            entity.syspTime += self._params['Tx_TimeTreat']