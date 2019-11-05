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
for testchar in diag_test.values():    
    for top_level_key, top_level_value in preftable.items():    
        if "target" in top_level_value:
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
            topkey = top_level_key
            for i in preftable[topkey].keys():
                checklevel = i
                testlevel = testchar['level']
                if checklevel == testlevel:
                    for second_level_key, second_level_value in top_level_value.items():
                        checktarget = second_level_value['target']
                        # Are we calculating patient or HCP utility?
                        if checktarget == target:
                            # What is the attribute being examined?
                            checkattr = second_level_value['attribute']
                            testattr = testchar['attribute']
                            if checkattr == testattr:            
                                print(checkattr)
                            
                            
                        
                        
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