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

class GenTTE:
    def __init__(self, params, regcoeffs, agecohort):
        self._params = params
        # Specify which age group the survival coefficients are drawn from
        if agecohort == 0:
            self.cohort = 'GenPop'
        elif agecohort == 1:
            self.cohort = 'Under60'
        elif agecohort == 2:
            self.cohort = 'Over60'
        else:
            entity.stateNum = 99
            entity.currentState = "ERROR: the age cohort has not been specified properly - check the value of 'Scenario_AgeCohort' in 'Sequencer.py'"
        
        # Identify the values being used for this age group
        regtable = {}
        for name, vals in regcoeffs.items():
            regtable[name] = {}
            for agegrp, secvals in vals.items():
                if agegrp == self.cohort:
                    values = secvals
            regtable[name] = values
        self.regtable = regtable

    def ReadParam(self, entity):
        regtable = self.regtable
        # What is the entity's COO?
        COO = entity.COO
        self.TTE = {}
        for name, vals in regtable.items():
            # Pull the mean and SE values for the regression parameters 'const' and 'shape'
            for cootype, secvals in vals.items():
            # For the entity's COO
                if cootype == COO:
                    cmean = secvals['const']['mean']
                    cse = secvals['const']['SE']
                    smean = secvals['shape']['mean']
                    sse = secvals['shape']['SE']
                    # Randomly sample these values from a Normal distribution
                    samp_const = numpy.random.normal(cmean, cse)
                    samp_shape = numpy.random.normal(smean, sse)
            self.TTE[name] = {'const': samp_const, 'shape': samp_shape}

    def MakeTTE(self, entity, scenario):
        # What are the COO subtypes that are eligible to receive experimental treatment?
        COOlist = []
        for key, value in scenario.items():
            if value == 1:
                COOlist.append(key)

        # Is the enity eligible for experimental treatment?
        eligible = 0
        if entity.COO_diag in COOlist:
            # Does the entity have an eligible subtype
            if entity.hadNGS == 1:
                # Did the entity get an NGS test?
                if entity.COO == entity.COO_diag:
                    # Is the entity's diagnosed COO accurate?
                    if entity.getsCompanion == 1 or entity.getsCompanion == 9:
                        # Has the entity received the companion diagnostic, or is there none available?
                        eligible = 1
        if hasattr('GotFirstNGS', entity) == True:
            # If the entity has already received NGS-guided treatment, they can't receive it again
            eligible = 0

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
        entity.NGStreat = 0
        if eligible == 1:
            entity.NGStreat = 1
            # Is this the first or second line of treatment?
            secondline = 0
            if entity.recurrence == 1:
                secondline = 1
            # What is the hazard rate associated with the experimental treatment?
            if secondline == 0:
                # Adjust time to recurrence using hazard ratio from first line of treatment
                CRtoFail['Intercept'] += entity.params['Tx_HR_NewTx_Firstline']
                entity.GotFirstNGS = 1
            else:
                # Adjust post-recurrence survival using hazard ratio from second line of treatment
                FailtoDeath['Intercept'] += entity.params['Tx_HR_NewTx_Secondline']

        tproblist = [CRtoDeath, CRtoFail, FailtoDeath]

        timeslist = []
        for tprob in tproblist:
            shape = math.exp(tprob['Sigma'])
            lmbda = math.exp(tprob['Intercept'])
            scale = 1/lmda
            time = numpy.random.weibull(shape)*scale
            timeslist.append(time)

        entity.TTE = {'CRtoDeath': {timeslist[0]}, 'CRtoFail': {timeslist[1]}, 'FailtoDeath': {timeslist[2]}}
