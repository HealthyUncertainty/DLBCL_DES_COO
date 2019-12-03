# -*- coding: utf-8 -*-
"""
A program to describe the Diagnosis System Process. Entities will receive a series of
diagnostic tests. The sequence of tests depends on the entity's preferences (i.e., their
uptake status). If they don't receive an NGS test they will get a standard workup. If
they do receive an NGS test they may get it first or they may get it second.

'Screentest' applies a user-specified test, which may or may not misclassify the COO.

'GetDiagnosis' uses the test results to determine what the patient's diagnosed COO
(entity.COO_diag) is. Note that entity.COO and entity.COO_diag can have different values.

If the entity receives an NGS test, they can be classified as:
    - ABC
    - GCB
    - Dhit (Double hit)
    - Undefined
    
If the entity does not receive an NGS test, or if the NGS results are 'Undefined'
and they have a conventional test, they can be classified as:
    - ABC
    - Non-ABC

@author: icromwell
"""

import random

class Diagnosis:
    def __init__(self, params):
        self._params = params
        self.Sens_conv = params['Diag_Sensitivity_Conventional']
        self.Spec_conv = params['Diag_Specificity_Conventional']
        self.Sens_NGS = params['Diag_Sensitivity_NGS']
        self.Spec_NGS = params['Diag_Specificity_NGS']
        self.screenpos = random.random()
        self.screenneg = random.random()
        self.misdiagnosis = []
        self.NGStest = 0
        self.convtest = 0
        
    def Screentest(self, entity, seqno):
        # Sequence number determines which test is being performed
        misdiagnosis_conv = 0
        misdiagnosis_NGS = 0
        entity.hadNGS = 0
        if seqno == 1:
            # Conventional testing
            entity.resources.append(('Conventional Diagnostic Test', entity.allTime))
            self.convtest = 1
            # Compare positive test to sensitivity
            if self.screenpos > self.Sens_conv:
                # False positive
                misdiagnosis_conv = 1
                entity.events.append(('False positive - conventional diagnosis', entity.allTime))
            # Compare negative test to specificity
            if self.screenneg > self.Spec_conv:
                # False negative
                misdiagnosis_conv = 1
                entity.events.append(('False negative - conventional diagnosis', entity.allTime))            
        elif seqno == 2:
            # NGS testing
            entity.resources.append(('NGS Diagnostic Test', entity.allTime))
            entity.hadNGS = 1
            self.NGStest = 1
            # Compare positive test to sensitivity
            if self.screenpos > self.Sens_NGS:
                # False positive
                misdiagnosis_NGS = 1
                entity.events.append(('False positive - NGS diagnosis', entity.allTime))
            # Compare negative test to specificity
            if self.screenneg > self.Spec_NGS:
                # False positive
                misdiagnosis_NGS = 1
                entity.events.append(('False negative - NGS diagnosis', entity.allTime))        
        else:
            entity.stateNum = 99
            entity.currentstate = "ERROR - Invalid diagnostic sequence number. Check Sequencer.py"
        
        # If a misdiagnosis occurs, pass that information into the class
        if misdiagnosis_conv == 1:
            self.misdiagnosis.append('conventional')
        if misdiagnosis_NGS == 1:
            self.misdiagnosis.append('NGS')
    
    def GetDiagnosis(self, entity):        
        # If an NGS test has been performed, the entity is diagnosed based on that result
        if self.NGStest == 1:
            if 'NGS' in self.misdiagnosis:
                # NGS misclassifies COO - 'Undefined'
                entity.COO_diag = 'Undef'
                entity.COO_misclassified = 1
                entity.COO_misclassified_NGS = 1
            else:
                entity.COO_diag = entity.COO
            # Undefined on NGS
            if entity.COO_diag == 'Undef':
                # Received conventional testing?
                if self.convtest == 1:
                    # Conventional testing also misclassifies ABC subtype
                    if 'conventional' in self.misdiagnosis:
                        entity.COO_misclassified_conventional = 1
                        # Conventional testing misclassifies COO
                        if entity.COO == 'ABC':
                            entity.COO_diag = 'Non-ABC'
                        else:
                            entity.COO_diag = 'ABC'
                    # Use (accurate) conventional test result
                    else:
                        if entity.COO == 'ABC':
                            entity.COO_diag = 'ABC'
                        else:
                            entity.COO_diag = 'Non-ABC'
        else:
            # Use conventional test result
            if 'conventional' in self.misdiagnosis:
                entity.COO_misclassified = 1
                entity.COO_misclassified_conventional = 1
                # Conventional testing misclassifies COO
                if entity.COO == 'ABC':
                    entity.COO_diag = 'Non-ABC'
                else:
                    entity.COO_diag = 'ABC'
            else:
                if entity.COO == 'ABC':
                    entity.COO_diag = 'ABC'
                else:
                    entity.COO_diag = 'Non-ABC'
                    
        entity.time_Sysp = entity.allTime
        entity.stateNum = 1.5
        entity.currentState = "1.5 - Companion diagnostic testing"