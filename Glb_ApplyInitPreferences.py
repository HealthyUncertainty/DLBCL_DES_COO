# -*- coding: utf-8 -*-
"""
Create a probabilistically-sampled preferences table for each entity.

@author: icromwell
"""

def getrand(mean, SE):
    return numpy.random.normal(mean, SE)

import numpy
class ApplyInitPreferences:
    def __init__(self, inputs):
        self._inputs = inputs

    def Process(self, entity):
        preftable = self._inputs        
        preferences = {}
        for top_level_key, top_level_value in preftable.items():
            preferences[top_level_key] = {}
            if "mean" in top_level_value:
                preferences[top_level_key]['target'] = top_level_value['target']
                preferences[top_level_key]['attribute'] = top_level_value['attribute']
                preferences[top_level_key]['value'] = getrand(top_level_value['mean'], top_level_value['SE'])
            else:
                for second_level_key, second_level_value in top_level_value.items():    
                    preferences[top_level_key]['target'] = second_level_value['target']
                    preferences[top_level_key]['attribute'] = second_level_value['attribute']
                    preferences[top_level_key][second_level_key] = {}
                    preferences[top_level_key][second_level_key]['value'] = getrand(second_level_value['mean'], second_level_value['SE'])

        entity.preferences = preferences