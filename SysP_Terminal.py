# -*- coding: utf-8 -*-
"""
A program to describe the management of end-of-life care.

@author: icromwell
"""
class Terminal:
    def __init__(self, params):
        self._params = params

    def Process(self, entity):
        #Terminal disease - end-of-life care
        entity.resources.append(("Treatment - End of Life", entity.allTime))
        entity.events.append(("End-of-life care", entity.allTime))
        entity.utility.append(("End of life", self._params['Util_EoL'], entity.allTime))
        entity.allTime = entity.time_DeadofDisease      # Advance clock to death

    
####################################################
# VARIABLES CREATED IN THIS STEP:
#
#   adv_hadSalvage - flag indicating that the entity has received salvage surgery
#   adv_reirrad - flag indicating that the entity has received a second round of RT
#   adv_chemoCount - a counter for the number of cycles of advanced chemotherapy received
#   chemoLimit - the maximum number of cycles of chemo an entity can receive
#   EoLMonth - a counter to denote the number of months into the terminal phase an entity has come    
        