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
        # Starting age is sampled from normal distribution
        entity.startAge = self._params['Demo_StartAge']
        
        # Sex: 1 = female, 0 = male
        makeSex = random.random()
        if makeSex < 0.5:
            entity.sex = 'F'
        else:
            entity.sex = 'M'
        
        makeCanhist = random.random()
        if makeCanhist < self._params['Demo_CancerHistory']:
            entity.Canhist = 1
        else:
            entity.Canhist = 0

        "Entities start asymptomatically, at t0"
        entity.utility.append(("Well", self._params['Util_Well'], 0.0))
        
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