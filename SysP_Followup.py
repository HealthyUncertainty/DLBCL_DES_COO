# -*- coding: utf-8 -*-
"""
Returning for regular post-treatment follow-up appointments.

The entity returns regularly to have their surgical site inspected, and will have
periodic biopsies, lab tests, and imaging done to investigate the presence of progression.

Follow-up is scheduled more frequently at first, and then gradually decreased. After ten
years, the person is assumed to be in remission (i.e., eventually dies from natural causes).

N.B.: Because the rates of recurrence are taken from *detected* cancers in the base case, 
this program does not actually simulate the process of detecting a cancer - cancers are 
assumed to be detected at the time of recurrence. The process is coded anyway to allow 
for the possibility of using other sources of data (e.g., clinical trial data) to investigate
cost-effectiveness scenarios regarding different recurrence- and followup-relevant policy
changes.

@author: icromwell
"""

class Followup:
    def __init__(self, params):
        self._params = params

    def Process(self, entity):
        if entity.time_Sysp > entity.allTime:
            # Have not yet reached next system process event, do nothing
            pass
        else:
            # Newly routed entity has a follow-up number of zero
            if entity.folupNum == 0:
                if entity.recurrence == 0:
                    entity.utility.append(("Undergoing follow-up", self._params['Util_FollowUp'], entity.allTime))
                elif entity.recurrence == 1:
                    entity.utility.append(("Undergoing post-recurrence follow-up", self._params['Util_FollowUp_Recur'], entity.allTime))

            # Record six-month cycle of followup
            entity.folupNum += 1
            folup = str("Follow-up - cycle " + str(entity.folupNum))
            # Has the entity reached 5 years of follow-up?
            if entity.folupNum < 10:
                # No: entity will be scheduled for their next appointment
                # Because this model uses 6-month post-treatment costs, resources occur on a cycle-based schedule
                entity.resources.append((folup, entity.allTime))
                entity.time_Sysp += self._params['Folup_Time_AppInterval']
            else:
                entity.resources.append(("Follow-up - final", entity.allTime))
                entity.events.append(("Entity's cancer is in remission", entity.allTime))
                entity.utility.append((self._params['Util_Remission'], entity.allTime))

                entity.stateNum = 4.8  # Entity is in remission and receives no more care
                entity.currentState = "Remission"
                entity.cancerDetected = 9  # Cancer is in remission and so no further clinical events are scheduled
                entity.time_deadOfDisease = 777777  # Death from disease set to implausibly high value
                entity.time_Recurrence = 666666  # Future recurrence set to implausble date
                entity.time_Sysp = 555555  # No future system process events occur