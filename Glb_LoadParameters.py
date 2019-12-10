# -*- coding: utf-8 -*-
"""
Load parameter values from the Excel spreadsheet 'InputParameters'

@author: icromwell
"""
from Glb_Estimates import Estimates
from Glb_Estimates import Estimate

class LoadParameters:
    def __init__(self, inbook):
        self._inbook = inbook

    def getScenario(self):
        sheet = self._inbook["Scenario"]
        scenario = {}
        for line in sheet.rows:
            if line[0].value == 'Scenario':
                # There's no estimate name in this row.
                continue
            name = line[0].value
            val = line[2].value
            scenario[name] = val
        self.Scntable = scenario
    
    # Import parameter estimates from the table
    def getEstimates(self):
        sheet = self._inbook["Inputs"]
        estimates = Estimates()

        for line in sheet.rows:
            if not line[0].value:
                # There's no estimate name in this row.
                continue
            if not line[5].value:
                line[5].value = 0
            setattr(estimates, line[0].value, Estimate(line[1].value, line[2].value, line[3].value, line[4].value))
        
        del(estimates.Parameter)
        self.Ptable = estimates

    # Import Regression Coefficients from the table
    def getRegcoeffs(self):
        regsheet = self._inbook["RegCoeffs"]
        source = []  # A list to hold data

        "Convert the openpyxl object into a useable form"       
        for row in list(regsheet.rows)[1:]:
            args = [cell.value for cell in row]
            source.append(args)
            
        for row in range(len(source)):
            source[row][0] = str(source[row][0])
            source[row][1] = str(source[row][1])
        
        "Create a multi-level dictionary to hold each parameter from the regression model:"            
        config = {}         # creates the blank dictionary
        for param, group, factor, vartype, mean, SE in source:
            SE = SE if SE else 0    # If SE is blank, enter zero
            vartype = vartype if vartype else 0
            mean = mean if mean not in ("ref", None) else 0     # Reference category = 0
            if param not in config:
                config[param] = {}
            if group not in config[param]:
                    config[param][group] = {}
            if factor not in config[param][group]:
                config[param][group][factor] = {}
            if vartype not in config[param][group][factor]:
                config[param][group][factor][vartype] = {"mean": mean, "SE": SE}
        
        self.Regcoeffs = config
    
    # Import cost estimates from the table
    def getCostcoeffs(self):
        costsheet = self._inbook["Costs"]
        cost_estimates = Estimates()
        for line in costsheet.rows:
            if not line[0].value:
                # There's no estimate name in this row.
                continue
            setattr(cost_estimates, line[0].value, Estimate(line[1].value, line[2].value, line[3].value, line[4].value))
        del(cost_estimates.Parameter)
        
        # Create a dictionary of unit costs that the program will read from
        CostDict = {}
        for i in range(0, costsheet.max_row):
            cost_name = str(costsheet.cell(row = i+1, column = 1).value)
            cost_type = costsheet.cell(row = i+1, column = 2).value
            cost_varnum = costsheet.cell(row = i+1, column = 3).value
            cost_mean = costsheet.cell(row = i+1, column = 4).value
            cost_se = costsheet.cell(row = i+1, column = 5).value
            CostDict[cost_name] = (cost_type, cost_mean, cost_se)
        del(CostDict['Parameter'])
        
        self.Costcoeffs = CostDict


    # Import preferences from table
    def getPrefcoeffs(self):
        prefsheet = self._inbook["PrefCoeffs"]
        prefsource = []                                           # A list to hold data
        
        for row in list(prefsheet.rows)[1:]:
            args = [cell.value for cell in row]
            prefsource.append(args)
            
        for row in range(len(prefsource)):
            prefsource[row][0] = str(prefsource[row][0])
            prefsource[row][1] = str(prefsource[row][1])
        
        pconfig = {}         # creates the blank dictionary
        for param, target, attribute, value, typeno, mean, SE in prefsource:
            SE = SE if SE else 0    # If SE is blank, enter zero
            mean = mean if mean not in ("ref", None) else 0     # Reference category = 0
            if param not in pconfig:
                pconfig[param] = {}
            if typeno == 2:
                pconfig[param]= {'target': target, 'attribute': attribute, 'type': typeno, 'mean': mean, 'SE': SE}
            elif typeno == 1:
                pconfig[param][value] = {'target': target, 'attribute': attribute, 'type': typeno, 'mean': mean, 'SE': SE}
            elif value == 'None':
                pconfig[param]= {'target': target, 'attribute': attribute, 'type': typeno, 'mean': mean, 'SE': SE}
            else:
                print("Parameter", param, "needs to have a 'TypeNo' of 1, 2, or a blank 'Value'. Check your input table.")
        
        self.Prefcoeffs = pconfig
    
    # Import test characteristics from table
    def getTestchars(self):
        testcharsheet = self._inbook["TestChars"]
        tcharsource = []

        for row in list(testcharsheet.rows)[1:]:
            args = [cell.value for cell in row]
            tcharsource.append(args)
            
        for row in range(len(tcharsource)):
            tcharsource[row][0] = str(tcharsource[row][0])
            tcharsource[row][1] = str(tcharsource[row][1])
        
        self.Testchars = tcharsource