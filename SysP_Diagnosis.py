# -*- coding: utf-8 -*-
"""
A program to describe the Diagnosis System Process. Entities will receive a series of
diagnostic tests. The sequence of tests depends on the entity's preferences (i.e., their
uptake status). If they don't receive an NGS test they will get a standard workup. If
they do receive an NGS test they may get it first or they may get it second.

@author: icromwell
"""

import random
import numpy