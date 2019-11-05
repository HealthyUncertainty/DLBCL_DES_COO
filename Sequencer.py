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
import pickle
from openpyxl import load_workbook                  # Load the import function
import numpy
from Glb_LoadParameters import LoadParameters

#############################################################################################
################################
# STEP 1 - SET UP THE SEQUENCER
"Define the number of entities you want to model"
num_entities = 50000

"Load the data from the Excel spreadsheet"
inbook = load_workbook('InputParameters.xlsx')
loadparams = LoadParameters(inbook)
loadparams.getEstimates()
#loadparams.getCostcoeffs()
loadparams.getRegcoeffs()
loadparams.getPrefcoeffs()
loadparams.getTestchars()

with open('estimates.pickle', 'rb') as f:
    Ptable = pickle.load(f)
#with open('costcoeffs.pickle', 'rb') as f:
 #   Costcoeffs = pickle.load(f)
with open('regcoeffs.pickle', 'rb') as f:
    Regcoeffs = pickle.load(f)
with open('prefcoeffs.pickle', 'rb') as f:
    Prefcoeffs = pickle.load(f)
with open('testchars.pickle', 'rb') as f:
    Testchars = pickle.load(f)

################################
# STEP 2 - CREATE A NEXT-GEN TEST BEING EVALUATED
    
from Diag_MakeTest import MakeTest
maketest = MakeTest(Testchars)
diag_test = maketest.Process()

################################
# STEP 3 - RUN THE SEQUENCER
ResourceList = []
EventsList = []
QALYList = []
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
      
    "Create resource table"
    resources = []
    events = []
    natHist = []
    QALY = []

    while True:
        # Apply Demographic Characteristics to a newly-created entity
        if entity.stateNum == 0.0:
            from Glb_ApplyInitDemo import ApplyInitDemo
            applydemo = ApplyInitDemo(params)
            applydemo.Process(entity)
    
        # Apply Clinical Characteristics to a newly-created entity
        if entity.stateNum == 0.1:
            from Glb_ApplyInitClinical import ApplyInitClinical
            applyclin = ApplyInitClinical(params)
            applyclin.Process(entity)
            
        # Apply preference estimates to a newly-created entity
        if entity.stateNum == 0.2:
            from Glb_ApplyInitPreferences import ApplyInitPreferences
            applypref = ApplyInitPreferences(Prefcoeffs)
            applypref.Process(entity)
            
        # Determine diagnostic pathway from patient and provider preferences
        if entity.stateNum == 0.3:
            from Diag_Uptake import Uptake
            uptake = Uptake(diag_test, entity)
            uptake.GetUtility('patient')
            uptake.GetUtility('HCP')
            uptake.Process(entity)
            
        ### Advance the clock to next scheduled event (NatHist, Sysp, Recurrence, Death) ###
        from Glb_CheckTime import CheckTime
        CheckTime(entity, estimates, natHist, QALY)

        ### Run next scheduled event/process according to state ###
    
        #People with a participating dentist undergo regular screening appointments    
        if entity.stateNum == 1.0:                
            from SysP_ScreenAppt import ScreenAppt
            screenappt = ScreenAppt(estimates, regcoeffs)            
            screenappt.Process(entity)
           
        #People with no dentist wait for disease event        
        if entity.stateNum == 1.8:
            entity.time_Sysp += 1000      #Move system process clock forward by 1000 days (See footnote 1)
                
        #People with a detected premalignancy undergo regular follow-up        
        if entity.stateNum == 2.0:
            from SysP_OPLmanage import OPLManage
            oplmanage = OPLManage(estimates, regcoeffs)            
            oplmanage.Process(entity) 
        
        #People with a detected cancer undergo treatment       
        if entity.stateNum == 3.0:
            from SysP_IncidentCancer import IncidentCancer
            incidentcancer = IncidentCancer(estimates, regcoeffs)
            incidentcancer.Process(entity)        

        #People who have been successfully treated undergo regular follow-up     
        if entity.stateNum == 4.0:
            from SysP_Followup import Followup
            followup = Followup(estimates, regcoeffs)
            followup.Process(entity)
   
        #People whose disease has entered remission after 10 years     
        if entity.stateNum == 4.8:
            #entity is in remission, no further events occur
            entity.allTime = entity.natHist_deathAge + 0.0001
             
        #People with terminal disease receive palliative care     
        if entity.stateNum == 5.0:
            from SysP_Terminal import Terminal
            terminal = Terminal(estimates, regcoeffs)
            terminal.Process(entity)
      
        #The entity is dead      
        if entity.stateNum == 100:
            #print("Entity is", entity.death_desc, "at:", entity.time_death)
            events.append(('Entity dies', entity.time_death))
            entity.utility.append(('Dead', 0, entity.time_death))
            break
        
        # An error has occurred
        if entity.stateNum == 99:
            print("An error has occurred and the simulation must end")
            print(entity.currentState)
            break
        
    EntityList.append(entity)
    ResourceList.append(entity.resources)
    QALYList.append(entity.utility)
    
    # END WHILE
    
looptime_end = time.time()
looptime = round((looptime_end - looptime_start)/60, 2)
print("The sequencer simulated", num_entities, "entities. It took", looptime, "minutes. You can do this.")

################################
# OPTIONAL STEP - SAVE OUTPUTS TO DISK 

numpy.save('EntityList', EntityList)
numpy.save('ResourceList', ResourceList)
numpy.save('EventsList', EventsList)
numpy.save('QALYList', QALYList)

################################
# STEP 3 - ESTIMATE COSTS AND SURVIVAL FOR SIMULATED COHORT
from Glb_AnalyzeOutput import Analyze_Output
output = Analyze_Output(estimates, CostDict)

# Estimate the costs generated by the entities in the population
CohortCost = []
for i in range(len(EntityList)):
    entity = EntityList[i]
    CohortCost.append(output.EntityCost(entity))
    
# Estimate the LYG and QALY generated by the entities in the population
CohortSurvival = np.array([output.EntitySurvival(x) for x in EntityList])
CohortLYG = CohortSurvival[:,0]
CohortQALY = CohortSurvival[:,1]


####################################################
# FOOTNOTE:
#
#   1 - The clock moves forward an arbitrary number of days, but is reset to the next natural
#       history or disease event by 'Glb_Checktime.py'. The purpose of moving the clock forward is
#       simply to prompt advancement to the next event.
