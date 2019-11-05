# -*- coding: utf-8 -*-
"""
Apply initial demographic characteristics to a newly-created entity
"""

############################################################################################
# Load some necessary packages and functions
import random
import pickle
import numpy

############################################################################################

"Assign a date of natural death"
with open('deathm.pickle', 'rb') as f:  # Load previously-created arrays
    deathage_M = pickle.load(f)
with open('deathf.pickle', 'rb') as f:
    deathage_F = pickle.load(f)

class ApplyInitDemo:
    def __init__(self, params):
    
        self._params = params

    def Process(self, entity):
        # A function to apply the initial characteristics to each person"
        
        # Starting age is sampled from normal distribution
        entity.startAge = self._params['Demo_startage']
        
        # Sex: 1 = female, 0 = male
        makeSex = random.random()
        if makeSex < 0.5:
            entity.sex = 'F'
        else:
            entity.sex = 'M'
        
        # Smoking status: 1 = ever smoker, 0 = never smoker
        # Alcohol use: 1 = heavy user, 0 = not heavy user
        makeCanhist = random.random()
        if makeCanhist < self._params['Demo_cancerhistory']:
            entity.Canhist = 1
        else:
            entity.Canhist = 0

        "Entities start asymptomatically, at t0"
        entity.OPLStatus = 0
        entity.hasCancer = 0
        entity.diseaseDetectable = 0
        entity.diseaseDetected = 0
        entity.cancerDetected = 0
        entity.utility.append(("Well", self._estimates.Util_Well.sample(), 0.0))
        
        "Assign date of all-cause death"
        if entity.sex == 'F':  
            nh_deathage = numpy.random.choice(deathage_F) + random.random()         # Sample an age at death from natural causes
        elif entity.sex == 'M':
            nh_deathage = numpy.random.choice(deathage_M) + random.random()
        nh_deathspan = nh_deathage - entity.startAge                     # Calculate the amount of time remaining before entity creation and death
        entity.natHist_deathAge = abs(nh_deathspan)*365        # Convert years to days

        "Update state"
        
        entity.currentState = "Demographic Characteristics Applied"
        entity.stateNum = 0.1


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