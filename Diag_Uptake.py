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