# -*- coding: utf-8 -*-
"""
A program to read and apply costs from a completed simulation. 

The program reads in unit costs from an Excel file and applies them to each instance
of the resource from the ResourceList array output from the Sequencer. It returns a
list of discounted costs

@author: icromwell
"""
############################################################################################
# Load some necessary packages and functions

from openpyxl import load_workbook                  # Load the import function
import numpy
import math
import random

"Import values from the table"

##################################################################################################


class Analyze_Output:
    def __init__(self, costdict, disc_o, disc_c):
        self._CostDict = costdict
        self._Disc_O = disc_o
        self._Disc_C = disc_c

    def CostEst(self, unit):
        if unit in self._CostDict.keys():
            pass
        else:
            print ("The 'Costs' sheet in 'InputParameters.xlsx' does not have an entry for: ", unit)
        
        """A function to estimate the unit cost from a mean and standard error"""
        # Fee-for-service and other fixed-value resources have a unit cost equal to the mean
        if self._CostDict[unit][0] == 1:
            samp_value = self._CostDict[unit][1]
        
        # Other kinds of costs are sampled from a gamma distribution based on their mean and sd
        elif self._CostDict[unit][0] == 2:
            x = self._CostDict[unit][1]
            y = self._CostDict[unit][2]
            gdist_shape = x**2/y**2                                    # A formula to produce the shape parameter
            gdist_scale = y**2/x                                       # A formula to produce the scale parameter
            samp_value = numpy.random.gamma(gdist_shape, gdist_scale)
            
        # Return an error if no variable type is specified
        else:
            print("Please specify a variable TypeNo for", unit, "in InputParameters.xlsx")
            
        return samp_value

    def EntityCost(self, entity):
        """A function to calculate the costs experienced by each entity"""
        # Create a list with costs generated by each entity
        resourcelist = entity.resources
        maxlen = len(resourcelist)-1
        if maxlen < 0:
            pass
        else: 
            if resourcelist[maxlen][1] > entity.natHist_deathAge:
                del(resourcelist[maxlen])
        costList = []
        for name, time in resourcelist:
            if resourcelist == []:   # If no costs have been generated
                costlist.append(0)
            else:
                unit = name
                # Years elapsed for the discounting function
                year = float(time/365)     
                # Apply a discount rate for future costs
                discRate_cost = 1 / (1 + self._Disc_C)**year              
                costList.append(self.CostEst(unit)*discRate_cost)
        return sum(costList)
    
    def EntitySurvival(self, entity):
        """A function to calculate LYG and QALY for each entity"""
        # Load the entity's utility list from the model output
        ent_util = []
        for i in range(len(entity.utility)):
            ent_util.append([int(round(entity.utility[i][2], 0)), entity.utility[i][1]])
        # If entity has multiple utility values at t0, use only the last one
        if ent_util[len(ent_util)-1][0] == 0:
            # It's possible for an entity to live less than a day. We round up to 1 day just so the
            #   math doesn't crap out on us
            ent_util.append([1,0])
        while ent_util[1][0] == 0:
            del(ent_util[0])

        # Define the daily discount rate
        discountrate = self._Disc_O
        disc_rate = 1 - (1 - discountrate)**(1 / 365)
        
        day = 0
        LYG = 0
        QALY = 0
        # For each row in the survival/utility list 'ent_util'
        for h in (1,len(ent_util)-1):
            # The utility value is read from the second column
            Util = ent_util[h-1][1]
            # Each day and quality-adjusted day is discounted at a daily rate
            while day < ent_util[h][0]:
                LYG += (1/365)*(1+disc_rate)**(-day)
                QALY += (Util/365)*(1+disc_rate)**(-day)
                day +=1
        
        return [LYG, QALY]
