# -*- coding: utf-8 -*-
"""
The Sequencer is the master file for the model. It creates entities and runs them through the model based
on their current model state, characteristics, history, and underlying probabilistic distrubtions of the 
model parameters.

The sequencer will run "num_entities" entities through the model and output the resources and events experienced
by each entity as a series of lists.

@author: icromwell
"""
############################################################################################
############################################################################################
# LOAD SOME NECESSARY PACKAGES AND FUNCTIONS

import time
from openpyxl import load_workbook                  # Load the import function
import numpy
from Glb_LoadParameters import LoadParameters
import copy

#############################################################################################
################################
# STEP 1 - SET UP THE SEQUENCER

"Load the data from the Excel spreadsheet"
inbook = load_workbook('InputParameters.xlsx')
loadparams = LoadParameters(inbook)
loadparams.getScenario()
loadparams.getEstimates()
loadparams.getCostcoeffs()
loadparams.getRegcoeffs()
loadparams.getPrefcoeffs()
loadparams.getTestchars()

Scntable = loadparams.Scntable
Ptable = loadparams.Ptable
CostDict = loadparams.Costcoeffs
RegDict = loadparams.Regcoeffs
PrefDict = loadparams.Prefcoeffs
Testchars = loadparams.Testchars

################################
# STEP 2 - CREATE A NEXT-GEN TEST BEING EVALUATED
    
from Diag_MakeTest import MakeTest
maketest = MakeTest(Testchars)
diag_test = maketest.Process()

################################
# STEP 3 - DEFINE THE TESTING SEQUENCE AND SCENARIO

Scenario_NGSTest = [0, Scntable['NGSTest']]
if Scntable['TestTiming'] == 1:
    TestTiming = 'FirstLine'
if Scntable['TestTiming'] == 2:
    TestTiming = 'SecondLine'
Scenario_COO = {'ABC': Scntable['COO_ABC'], 'Dhit': Scntable['COO_Dhit'], 'GCB': Scntable['COO_GCB'], 'Undef': Scntable['COO_Undef']}

################################
# STEP 3 - RUN THE SEQUENCER

"Define the number of entities you want to model"
num_entities = Scntable['CohortSize']
timehorizon = Scntable['TimeHorizon']

EntityList = []
looptime_start = time.time()
for i in range(0, num_entities):
    
    entity_num = 'entity' + str(i + 1)                  # Create an entity for each iteration of the model
    from Glb_CreateEntity import Entity
    entity = Entity()
    #print("Entity %2.0f is created"%(i+1))
    if i % (num_entities/20) == 0:
        print("Now simulating entity", i, "of", num_entities)
    
    "Sample parameter values for entity"
    from Glb_MakeEstimates import MakeEstimates
    entity_estimates = MakeEstimates(Ptable)
    entity_estimates.Process(entity)
    params = entity.params
    
    # Apply demographic characteristics to a newly-created entity
    from Glb_ApplyInitDemo import ApplyInitDemo
    applydemo = ApplyInitDemo(params)
    applydemo.Process(entity)

    # Apply Clinical Characteristics to a newly-created entity
    from Glb_ApplyInitClinical import ApplyInitClinical
    applyclin = ApplyInitClinical(params)
    applyclin.Process(entity)
    # Just for debugging purposes
    entity.COO = 'ABC'
        
    # Apply preference estimates to a newly-created entity
    from Glb_ApplyInitPreferences import ApplyInitPreferences
    applypref = ApplyInitPreferences(PrefDict)
    applypref.Process(entity) 
    
    # Clone entity to simulate the 'comparator' and and 'intervention' case
    comp_entity = copy.deepcopy(entity)
    itvn_entity = copy.deepcopy(entity)
    clones = []
    for testscenario in Scenario_NGSTest:
        if testscenario == 0:
            entity = comp_entity
        elif testscenario == 1:
            entity = itvn_entity
        else:
            entity.currentState = "ERROR - NGSTest in 'InputParameters.xls' must be either 0 or 1"
            entity.stateNum = 99

        while True:
            # Determine diagnostic pathway from patient and provider preferences
            if entity.stateNum == 0.3:
                from Diag_Uptake import Uptake
                uptake = Uptake(diag_test, entity)
                uptake.GetUtility('patient')
                uptake.GetUtility('HCP')
                uptake.Process(entity)
                
            ### Advance the clock to next scheduled event (Diagnosis, Treatment, Recurrence, Death) ###
            from Glb_CheckTime import CheckTime
            CheckTime(entity, params)
            
            ### Run next scheduled event/process according to state ###
            
            # Entities undergo some diagnostic testing 
            if entity.stateNum == 1.0:                
            
                # Just for debugging purposes
                entity.uptake['GetsNGS'] = 'Yes'
            
            
                from SysP_Diagnosis import Diagnosis
                diag_firstline = Diagnosis(params)
                if TestTiming == 'FirstLine':
                    if entity.uptake['GetsNGS'] == 'No':
                        # Entities that do not take up NGS tests get conventional test
                        diag_firstline.Screentest(entity, 1)
                    elif testscenario == 0:
                        # Only perform conventional testing on this entity
                        diag_firstline.Screentest(entity, 1)
                    elif testscenario == 1:
                        # Determine test sequence
                        if Scntable['TestSequencing'] == 0:
                            diag_firstline.Screentest(entity, 2)
                        elif Scntable['TestSequencing'] == 1:
                            diag_firstline.Screentest(entity, 1)
                            diag_firstline.Screentest(entity, 2)
                        elif Scntable['TestSequencing'] == 2:
                            diag_firstline.Screentest(entity, 2)
                            diag_firstline.Screentest(entity, 1)
                else:
                    # Only perform conventional testing on this entity
                    diag_firstline.Screentest(entity, 1)               
                # Determine entity's diagnosis based on their test results
                diag_firstline.GetDiagnosis(entity)
                
            # Entities may receive companion diagnostics if they have the COO of interest
            if entity.stateNum == 1.5:
                from SysP_CompanionDiagnostic import CompanionDiagnostic
                companion = CompanionDiagnostic(entity.params)
                companion.Process(entity, Scntable['Companion'], Scenario_COO)
               
            # People receive a prescribed course of treatment
            if entity.stateNum == 2.0:
                # Has entity had their clinical events scheduled?
                if hasattr(entity, 'TTE') == False:
                    # Create time-to-event estimates for entity
                    from Glb_GenTTE import GenTTE
                    gentte = GenTTE(params, RegDict, Scntable['AgeCohort'])
                    gentte.ReadParam(entity)
                    gentte.MakeTTE(entity, Scenario_COO, TestTiming)
                from SysP_ClinicalPrescription import ClinicalPrescription
                prescription = ClinicalPrescription(entity.params)
                prescription.Process(entity)
            
            #People with a diagnosed cancer undergo treatment
            if entity.stateNum == 3.0:
                from SysP_TxFirstLine import TxFirstLine
                txfirstline = TxFirstLine(entity.params)
                txfirstline.Process(entity, TestTiming)
            
            #People who have been successfully treated undergo regular follow-up     
            if entity.stateNum == 4.0:
                from SysP_Followup import Followup
                followup = Followup(entity.params)
                followup.Process(entity)
            
            #People whose disease has entered remission after 10 years     
            if entity.stateNum == 4.8:
                #entity is in remission, no further events occur
                entity.allTime = entity.natHist_deathAge + 0.0001
                 
            # People with recurrence undergo additional diagnostic work
            if entity.stateNum == 5.0:
                diag_secondline = Diagnosis(params)
                # In what order does diagnostic testing occur?
                if TestTiming == 'SecondLine':
                    if entity.uptake['GetsNGS'] == 'No':
                        # Entities that do not take up NGS tests get conventional test
                        diag_secondline.Screentest(entity, 1)
                    elif testscenario == 0:
                        # Only perform conventional testing on this entity
                        diag_secondline.Screentest(entity, 1)
                    elif testscenario == 1:
                        # Determine test sequence
                        if Scntable['TestSequencing'] == 0:
                            diag_secondline.Screentest(entity, 2)
                        elif Scntable['TestSequencing'] == 1:
                            diag_secondline.Screentest(entity, 1)
                            diag_secondline.Screentest(entity, 2)
                        elif Scntable['TestSequencing'] == 2:
                            diag_secondline.Screentest(entity, 2)
                            diag_secondline.Screentest(entity, 1)
                else:
                    # Only perform conventional testing on this entity
                    diag_secondline.Screentest(entity, 1)               
                # Determine entity's diagnosis based on their test results
                diag_secondline.GetDiagnosis(entity)
            
            # Companion diagnostic for second-line treatment
            if entity.stateNum == 5.5:
                from SysP_CompanionDiagnostic import CompanionDiagnostic
                companion = CompanionDiagnostic(entity.params)
                companion.Process(entity, Scntable['Companion'], Scenario_COO)
            
            # An entity receiving second-line treatment
            if entity.stateNum == 6.0:
                from SysP_TxSecondLine import TxSecondLine
                txsecondline = TxSecondLine(entity.params)
                txsecondline.Process(entity, TestTiming)  
            
            # People receive palliative care at the end of their life
            if entity.stateNum == 7.0:
                from SysP_Terminal import Terminal
                terminal = Terminal(entity.params)
                terminal.Process(entity)
          
            #The entity is dead      
            if entity.stateNum == 100:
                #print("Entity is", entity.death_desc, "at:", entity.time_death)
                entity.utility.append(('Dead', 0, entity.time_death))
                break
            
            # An error has occurred
            if entity.stateNum == 99:
                print("An error has occurred and the simulation must end")
                print(entity.currentState)
                break
            
        clones.append(entity)       
        # END WHILE
    EntityList.append(clones)
l
ooptime_end = time.time()
looptime = round((looptime_end - looptime_start)/60, 2)
print("The sequencer simulated", num_entities, "entities. It took", looptime, "minutes.")

################################
# OPTIONAL STEP - SAVE OUTPUTS TO DISK 

#numpy.save('EntityList', EntityList)

################################
# STEP 3 - ESTIMATE COSTS AND SURVIVAL FOR SIMULATED COHORT
from Glb_AnalyzeOutput import Analyze_Output
output = Analyze_Output(CostDict, Scntable['Disc_O'], Scntable['Disc_C'])

# Estimate the costs generated by the entities in the population
Results = []
for clone in EntityList:
    cloneoutput = []
    for member in clone:
    # Estimate the LYG and QALY generated by the entities in the population
        clonesurv = (output.EntitySurvival(member))
        clonecost = (output.EntityCost(member))
        cloneoutput +=(clonesurv + [clonecost])
    Results.append(cloneoutput)

CohortCEA = numpy.array(Results)
numpy.savetxt('CEA_Outputs.csv', CohortCEA, delimiter=",")

################################
# STEP 4 - EXPORT PARAMETER VALUES FOR EVPPI

# Import list of parameter values for each entity
paramlist = [list(EntityList[0].params.keys())]
paramlist[0].sort()
for entity in EntityList:
    sortvals = []
    for name in paramlist[0]:
        sortvals.append(entity.params[name])
    paramlist.append(list(sortvals))
    
# Convert variable names, values to numpy array
# This has to be done separately because numpy arrays can only contain one data type
namearray = paramlist[0]
del(paramlist[0])
valsarray = np.array(paramlist)

# Export names, values to .csv
import csv
with open('EVPPI_namearray.csv', 'w', newline='') as namelist:
     w = csv.writer(namelist, quoting=csv.QUOTE_ALL)
     w.writerow(namearray)
numpy.savetxt('EVPPI_valsarray.csv', valsarray, delimiter=",")


####################################################
# FOOTNOTE:
#
#   1 - The clock moves forward an arbitrary number of days, but is reset to the next natural
#       history or disease event by 'Glb_Checktime.py'. The purpose of moving the clock forward is
#       simply to prompt advancement to the next event.

