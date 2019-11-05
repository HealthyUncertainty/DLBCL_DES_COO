<<<<<<< HEAD
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
        # The marginal utility of testing starts at zero
        v = 0
        # Loop through parameters in the preference table
        for param in self.preftable.keys():
            # Are we calculating patient or HCP utility?
            if param['target'] == target:
                # Identify values for all coefficients
                for attribute in self._diagtest.keys():
                    if param['vartype'] == 2:
                        v += param['mean'] * self._diagtest[attribute]['level']
                    else:
                        level = self._diagtest[attribute]['level']
                        v += param[attribute][level]['mean']
        self.utility[target] = {'utility': v}
        
    def Process(self, entity):
        entity.uptake = {}
        for target in self.utility.keys():
            randprob = random.random()
            prefprob = math.exp(self.utility[target]['utility'])/(1 + math.exp(self.utility[target]['utility']))
            if randprob < prefprob:
                entity.uptake[target] = {'uptake': 'Yes'}
            else:
                entity.uptake[target] = {'uptake': 'No'}
                
                
preftable = entity.preferences
v = 0
test = []
prefkeys = [x for x in preftable.keys()]
for prefval in prefkeys:
    if "target" in preftable[prefval]:
        for testchar in diag_test.values():
            testlevel = testchar['level']
            testattr = testchar['attribute']         
            """
            # Are we calculating patient or HCP utility?
            checktarget = top_level_value['target']
            if checktarget == target:
                checkattr = top_level_value['attribute']
                testlevel = testchar['level']
                testvalue = top_level_value['value']
                # Multiply the test attribute levels by the preference for that level (continuous variable)
                if checkattr == testchar['attribute']:
                    v += testvalue * testlevel
            """
    else:
        checkkey = preftable[prefval].keys()
        for checklevel in checkkey:
            checktarget = preftable[prefval][checklevel]['target']
            if checktarget == target:
                for testchar in diag_test.values():
                    testattr = testchar['attribute']
                    checkattr = preftable[prefval][checklevel]['attribute']
                    print(checkattr)
                    testlevel = testchar['level']
                    print(testlevel)
                    if checklevel == testlevel:
                        print(testlevel)
                        for second_level_key, second_level_value in top_level_value.items():
                            checktarget = second_level_value['target']
                            print(checktarget)
                            # Are we calculating patient or HCP utility?
                                # What is the attribute being examined?
                                checkattr = second_level_value['attribute']
                                
                                print(target, testlevel, checklevel, checkattr, testattr)
                                if checkattr == testattr:            
                                    print(target, checkattr)
                                
                            
                        
                        
                        varlevel = i
                        print(varlevel)
                        if checkattr == testchar['attribute']:
                            print(varvalue)
                    if i == checklevel:
                        print(i)
                for second_level_key, second_level_value in top_level_value.items():
                    for param, testchar in diag_test.items():
                        
                
                
                    

                                test.append(varvalue)

                # What level does the test have for each (categorical) attribute?

                        
                        # Apply the estimated utility for 
                        
                        print(checkattr)
                        :
                            if  == checkattr:
                                print(i)    
                        
                        
                        
                                v += varvalue
                                test.append(testchar['attribute'])
        if preftable[param][attribute]['target'] == target:
            print('True')
            # Identify values for all coefficients
            for attribute in self._diagtest.keys():
                if param['vartype'] == 2:
                    v += param['mean'] * self._diagtest[attribute]['level']
                else:
                    level = self._diagtest[attribute]['level']
                    v += param[attribute][level]['mean']
self.utility[target] = {'utility': v}
=======
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
                entity.uptake['GetsTest'] = 'Yes'
            else: entity.uptake['GetsTest'] = 'No'
        else:
            entity.uptake['GetsTest'] = 'No'
        
        entity.stateNum = 1.0
        entity.currentState = "1.0 - Undergoing diagnostic testing"
>>>>>>> parent of 5469f32... Revert "Preferences and uptake function"
