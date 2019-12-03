# -*- coding: utf-8 -*-
"""
A program to describe an entity under active treatment for cancer. They receive a round of treatment and may experience
adverse effects from that treatment. When they reach the maximum number of treatment rounds they move to follow-up.

@author: icromwell
"""
import random

class TxFirstLine:
    def __init__(self, params):
        self._params = params

    def Process(self, entity, scenario_timing):
        if hasattr(entity, "cycleNum") == False:
            entity.cycleNum = 0

        # Has entity reached maximum number of cycles allowed?
        getsNGS = 0
        if entity.NGScare == 1 and scenario_timing == 'FirstLine':
            getsNGS = 1
            maxCycle = self._params['Tx_First_MaxCycle_NGS']
        else:
            maxCycle = self._params['Tx_First_MaxCycle']
        if entity.cycleNum == maxCycle:
            entity.time_Recurrence = entity.allTime + entity.TTE['CRtoFail']
            entity.time_DeadofDisease = entity.allTime + entity.TTE['CRtoDeath']
            
            # Entity is done treatment and now goes to their first follow-up appointment
            entity.cycleNum = 0 # Reset the cycle count
            entity.events.append(("Completed first line treatment", entity.allTime))
            entity.stateNum = 4.0
            entity.currentState = "4.0 - Start follow-up"
            entity.folupNum = 0

        else:
            # Entity receives a cycle of treatment
            entity.resources.append(("Treatment - First Line - Standard Care", entity.allTime))

            # Does entity experience an adverse event?
            adverse_event = random.random()
            if adverse_event < self._params['Tx_First_ProbAdverseEvent_Standard']:
                entity.resources.append(("Adverse Event - First Line - Standard Care", entity.allTime))
                entity.events.append(("Adverse Event - First Line - Standard Care", entity.allTime))
                entity.utility.append(("Adverse Event - First Line - Standard Care", self._params['Util_First_AdvEvent_Standard'], entity.allTime))
            else:
                entity.utility.append(("Treatment - First Line - Standard Care", self._params['Util_First_Treatment_Standard'], entity.allTime))

            # If entity has the appropriate COO and NGS testing, they may receive experimental care
            if getsNGS == 1:
                entity.resources.append(("Treatment - First Line - NGS-guided Care", entity.allTime))

                # Does entity experience an adverse event?
                adverse_event = random.random()
                if adverse_event < self._params['Tx_First_ProbAdverseEvent_NGS']:
                    entity.resources.append(("Adverse Event - First Line - NGS-guided Care", entity.allTime))
                    entity.events.append(("Adverse Event - First Line - NGS-guided Care", entity.allTime))
                    entity.utility.append(("Adverse Event - First Line - NGS-guided Care", self._params['Util_First_AdvEvent_NGS'], entity.allTime))
                else:
                    entity.utility.append(("Treatment - First Line - NGS-guided Care", self._params['Util_First_Treatment_NGS'], entity.allTime))

            # Record the number of cycles that have occurred
            entity.cycleNum += 1
            # Advance the system clock to the next appointment time
            entity.time_Sysp += self._params['Tx_First_TimeTreat']