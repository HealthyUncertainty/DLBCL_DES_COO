# -*- coding: utf-8 -*-
"""
This file checks the passage of time at the beginning of each loop of 'Sequencer.py'. 
If events have occurred since the last check, (i.e., disease progression, aging, 
natural death, etc.) the appropriate changes are made to the entity's attributes.

@author: icromwell
"""
def CheckTime(entity, estimates, natHist, QALY):
    
    "Update entity age"
    entity.age = entity.startAge + int(entity.allTime/365.25)
    
    "Check for natural death"
    if entity.allTime > entity.natHist_deathAge:
        entity.allTime = entity.natHist_deathAge
    if int(round((entity.allTime - entity.natHist_deathAge),3)) == 0:
        entity.allTime = entity.natHist_deathAge            # The simulation concludes with the entity's death            
        entity.time_death = entity.allTime                  # The time of death is recorded
        entity.death_type = 2                               # The entity has died of natural causes
        entity.death_desc = "Dead of Natural Causes"
        entity.stateNum = 100                               # The entity is dead
        entity.currentState = "Dead"
    
    else:
        # Has entity been scheduled to die of disease?           
        if hasattr(entity, 'time_DeadofDisease'):
            # Disease within last 3 months of life
            time_EOL = entity.time_DeadofDisease - 90     
        else:
            # If entity doesn't have DoD time, insert placeholder
            entity.time_DeadofDisease = 999999
            time_EOL = 99999

        # Has entity been scheduled to experience a recurrence?            
        if hasattr(entity, 'time_Recurrence'):
            pass
        else:
            # If entity doesn't have recurrence time, insert placeholder
            entity.time_Recurrence = 99999

        # Check for death from cancer          
        if entity.allTime >= entity.time_DeadofDisease:
            # The simulation concludes with the entity's death
            entity.allTime = entity.time_DeadofDisease
            # The time of death is recorded
            entity.time_death = entity.time_DeadofDisease       
            # The entity has died of disease
            entity.death_type = 1
            entity.death_desc = "Dead of Disease"
            entity.stateNum = 100
            entity.currentState = "Dead"

        # If entity has reached end of life state (last 3 months of life)               
        elif entity.allTime >= time_EOL:
            # Entity is in the "terminal disease" health state
            entity.stateNum = 5.0               
            entity.currentState = "End of Life"                
            entity.endOfLife = 1

        # Recurrence (SEE FOOTNOTE 1)             
        # If recurrence happens before the next system process event
        elif entity.time_Sysp >= entity.time_Recurrence:
            # Recurrence occurs before EOL (i.e., >90 days before death)
            if entity.time_Recurrence < time_EOL:   
                entity.allTime = entity.time_Recurrence
                # Future recurrence set to impossible date (SEE FOOTNOTE 2)
                entity.time_Recurrence = 666666
                # Flag entity as having active recurrence
                entity.recurrence = 1
                entity.cancerStage = "Recur"
                # Entity returns for diagnostic workup and possible treatment
                entity.stateNum = 3.0
                entity.currentState = "Treatment for recurrence"
                
            elif entity.time_Recurrence >= time_EOL:    # EOL occurs before recurrence
            # If entity is currently more than 3 months from death, set next system process time as EOL date
                entity.allTime = entity.time_EOL
                # Future recurrence set to impossible date (SEE FOOTNOTE 2)
                entity.time_Recurrence = 666666
                # Entity is in the "terminal disease" health state
                entity.stateNum = 5.0
                entity.currentState = "End of Life"                
                entity.endOfLife = 1
           
            # ERROR                    
            else:
                entity.stateNum = 99
                entity.currentState = "ERROR - recurrence has not been scheduled properly - look at Glb_Checktime.py"
                
        # Next scheduled system process event occurs before recurrence but after EOL
        elif entity.time_Sysp >= time_EOL:
            # Advance clock to EOL
            entity.allTime = time_EOL
            # Future recurrence set to impossible date (SEE FOOTNOTE 2)
            entity.time_Recurrence = 666666
            # Entity is in the "terminal disease" health state
            entity.stateNum = 5.0               
            entity.currentState = "End of Life"                
            entity.endOfLife = 1
                
        # If no disease event is scheduled before next system process event
        elif entity.allTime < entity.time_Sysp:
            entity.loopcount = 0 # Reset loop counter
            entity.allTime = entity.time_Sysp
            
        elif entity.allTime == entity.time_Sysp:
            # An error in the code might cause this kind of statement to loop if neither allTime
            #   or time_Sysp change. If that happens, this will catch it and return an eror.
            if hasattr(entity, 'loopcount') == False:
                entity.loopcount = 1
            else:
                if entity.loopcount < 1000: # An arbitrarily high number
                    entity.loopcount += 1
                else:
                    entity.failstate = entity.stateNum
                    entity.stateNum = 99
                    entity.currentState = ("ERROR - entity caught in Sysp/allTime loop - look at Glb_Checktime.py. This error happened when the entity was in stateNum", entity.failState)
            
        else:
            #ERROR
            entity.stateNum = 99
            entity.currentState = "ERROR - time_Sysp conflict - look at Glb_Checktime.py"                    
    
####################################################
# FOOTNOTES:
#
#   1 - Because the base case of this model relies on 'time to DETECTED recurrence' data, the time at which an entity
#   DEVELOPS a recurrence is treated as synonymous to the time that recurrence is DETECTED. If this model is updated
#   with recurrence rates from natural history or a clinical trial, then "stateNum" and "cancerStage" should only be
#   updated after a follow-up appointment (i.e., in the 'SysP_Followup' program).
#
#   2 - By setting the recurrence time impossibly late, the program won't reach the point where 'allTime' is greater
#   than 'time_Recurrence'. If the person DOES experience a subsequent recurrence, 'time_Recurrence' will be reset by
#   the 'RecurTx' System Process    