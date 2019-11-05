# -*- coding: utf-8 -*-
"""
Create a probabilistically-sampled preferences table for each entity.

@author: icromwell
"""

import numpy
class ApplyInitPreferences:
    def __init__(self, inputs):
        self._inputs = inputs

    def Process(self, entity):
        preftable = self._inputs        
        preferences = {}
        for i in preftable.keys():
            for j in preftable[i].keys():
                if j != 'mean':
                    preferences[i] = {}
            if isinstance(preftable[i][j], dict):    
                for j in preftable[i].keys():
                    preferences[i][j] = numpy.random.normal(preftable[i][j]['mean'], preftable[i][j]['SE'])
            else:
                for j in preftable[i].keys():
                    if j == 'mean':
                        preferences[i] = numpy.random.normal(preftable[i]['mean'], preftable[i]['SE'])

        entity.preferences = preferences