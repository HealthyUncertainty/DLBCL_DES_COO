# -*- coding: utf-8 -*-
"""
A function to randomly sample time-to-event values from the output of a regression model.

The program reads the regression output from an Excel table. The table contains the following
information:

    Parameter   - the name of the parameter
    Factor      - the Cell-of-Origin (COO) type (note: 'entity.COO', not 'entity.COO_diag')
    VarType     - the type of variable the coefficient is coded as
                    const: the log constant (_cons) of the Weibull GLM regression output
                    shape: the log lambda value (ln_p) from the Weibull GLM regression output
    Group       - the cohort from which time estimates are being drawn: GenPop, Under60, or Over60
    Mean        - the mean estimate of the coefficient
    SE          - the standard error of the estimate of the mean
    
This data is stored in a dictionary called 'regcoeffs'.

When the function is called, it reads the parameter name, cohort group, COO designation, and
variable type from user-specified values in the Sequencer and some values that are endogenous to
the entity. The program  then matches those values to the values from the Excel sheet  to return 
the associated mean and standard error for the shape and intercept coefficients of the Weibull curve.

Based on the level, it randomly draws (from a normal distribution) a value for
the coefficients based on the mean and SE. The sum of the samples estimates for the intercept and
shape are log-transformed into an estimate of time-to-event. If the entity receives GEP-guided
treatment then the logRR of that treatment is factored into the calculation of the shape parameter.

It is important to note that the name of the parameter must match EXACTLY (including being
case-sensitive) between how it appears in the entity and how it appears in the Excel table, or the
function will return an error.

@author: icromwell

Code provided by Stavros Korokithakis of Stochastic Technologies (www.stavros.io)
"""

import math
import numpy

"Define a function to draw estimates of time based on the regression coefficients"

class GenTime:
    def __init__(self, params, regcoeffs):
        self._params = params
        self._regcoeffs = regcoeffs

    def ReadParam(self, entity):
        # Read in the parameter values from the entity's 'regcoeffs' dictionary
        regtable = self._regcoeffs
        # What is the entity's COO?
        COO = entity.COO
        self.TTE = {}
        for name, vals in regtable.items():
            # Pull the mean and SE values for the regression parameters 'const' and 'shape'
            for cootype, secvals in vals.items():
                # For the entity's COO
                if cootype == 'COO':
                    cmean = secvals['const']['mean']
                    cse = secvals['const']['SE']
                    smean = secvals['shape']['mean']
                    sse = secvals['shape']['SE']
                    # Randomly sample these values from a Normal distribution
                    samp_const = numpy.random.normal(cmean, cse)
                    samp_shape = numpy.random.normal(smean, sse)
            self.TTE[name] = {'const': samp_const, 'shape': samp_shape}
    
    def GetVals(self, entity, treatment, scenario):
        # What are the COO subtypes that are eligible to receive experimental treatment?
        COOlist = []
        if scenario[0] == 1:
            COOlist.append('ABC')
        if scenario[1] == 1:
            COOlist.append('Dhit')
        if scenario[2] == 1:
            COOlist.append('GCB')
        if scenario[3] == 1:
            COOlist.append('Undef')
        
        # Does the entity have an eligible subtype?
        eligible = 0
        if entity.COO_diag in COOlist:
            # If the entity has an eligible subtype and got an NGS test, then they get treatment
            if entity.hadNGS == 1:
                eligible = 1
                
        # Estimate entity's survival parameters
        survdict = {}
        for param, coeffs in self.TTE.items():
            Intercept = self.TTE[param]['const']
            Sigma = self.TTE[param]['shape']
            survdict[param] = {'Intercept': Intercept, 'Sigma': Sigma}

        CRtoDeath = survdict['Tx_Tprob_CRtoDeath']
        CRtoFail = survdict['Tx_Tprob_CRtoFail']
        FailtoDeath = survdict['Tx_Tprob_FailtoDeath']
            
        # Will the entity receive an experimental treatment?
        if eligible == 1:
            # Is this the first or second line of treatment?
            secondline = 0
            if entity.recurrence = 1:
                secondline = 1
            # What is the hazard rate associated with the experimental treatment?
            if secondline == 0:
                # Adjust time to recurrence using hazard ratio from first line of treatment
                CRtoFail['Sigma'] += entity.params['Tx_HR_newTx_firstline']
            else:
                # Adjust post-recurrence survival using hazard ratio from second line of treatment
                FailtoDeath['Sigma'] += entity.params['Tx_HR_newTx_secondline']

        # Calculate the shape and scale parameters of the Weibull curve
        shape = 1/Sigma
        scale = math.exp(Intercept + coeff)
        self.shape = shape
        self.scale = scale
            
        else:
            entity.stateNum = 99
            entity.currentState = "Error - something happened in 'Glb_GenTime.py' - check the entity's COO_diag"
            
    # Randomly sample an event time for the entity from a Weibull distribution            
    def estTimeSurv(self):
        estimate_time = numpy.random.weibull(self.shape)*self.scale
        return estimate_time

    # Estimate the probability (CDF) of being alive at a given time
    def estProbSurv(self, time):
        estimate_probability = numpy.math.exp(-(time/self.scale)**self.shape)
        return estimate_probability