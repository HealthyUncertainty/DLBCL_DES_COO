# -*- coding: utf-8 -*-
"""
The 'uptake' function of an NGS test.

@author: icromwell
"""
import math
import random

class Uptake:
    def __init__(self, diag_test, entity):
        self._diagtest = diag_test
        self.preftable = entity.preferences
        self.utility = {}
    
    def GetUtility(self, target):
        # Calculate the estimated utility that a patient or an HCP derives from using the test
        v = 0
        for testkey, testchar in self._diagtest.items():
            testattr = testchar['attribute']
            testlevel = testchar['level']
            testtype = testchar['type']
            for prefkey, prefvals in self.preftable.items():
                checkattr = prefvals['attribute']
                checktarget = prefvals['target']
                # Are we calculating utility among patients or HCPs?
                if checktarget == target:
                    # For which attribute?
                    if checkattr == testattr:
                        # Continuous values
                        if testtype == 0:
                            # Utility = test attribute level * marginal preference for attribute
                            v += prefvals['value'] * testlevel
                        # Categorical values
                        else:
                            # What attribute level does the test have?
                            for checklevel, pref in prefvals.items():
                                # Utility = marginal preference for that attribute/level
                                if checklevel == testlevel:
                                    v += pref['value']

        self.utility[target] = {'utility': v}
        
    def Process(self, entity):
        # Will the patient and/or the HCP take up the new test?
        entity.uptake = {}
        for target in self.utility.keys():
            # Draw a random probability
            randprob = random.random()
            # Calculate probability of uptake
            prefprob = math.exp(self.utility[target]['utility'])/(1 + math.exp(self.utility[target]['utility']))
            # Is the uptake probability greater than the random probability?
            if prefprob > randprob:
                entity.uptake[target] = 'Yes'
            else:
                entity.uptake[target] = 'No'
        # Will the patient receive the test?
        if entity.uptake['patient'] == 'Yes':
            if entity.uptake['HCP'] == 'Yes':
                entity.uptake['GetsNGS'] = 'Yes'
            else: entity.uptake['GetsNGS'] = 'No'
        else:
            entity.uptake['GetsNGS'] = 'No'
        
        entity.stateNum = 1.0
        entity.currentState = "1.0 - Undergoing diagnostic testing"