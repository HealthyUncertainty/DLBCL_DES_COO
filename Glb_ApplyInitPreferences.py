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
            if "mean" in top_level_value:
                preferences[top_level_key] = {'attribute': top_level_value['attribute'], 'type': top_level_value['type'], 'target': top_level_value['target'], 'value': (getrand(top_level_value['mean'], top_level_value['SE']))}
            else:
                preferences[top_level_key] = {}
                for second_level_key, second_level_value in top_level_value.items():
                    preferences[top_level_key][second_level_key] = {'attribute': top_level_value[second_level_key]['attribute'], 'type': top_level_value[second_level_key]['type'], 'target': preftable[top_level_key][second_level_key]['target'], 'value': (getrand(second_level_value['mean'], second_level_value['SE']))}

        entity.preferences = preferences