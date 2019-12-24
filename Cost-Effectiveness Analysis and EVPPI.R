###################################################################################
#                                                                                 #
# TITLE: WDMOC - calculate incremental cost-effectiveness of model outputs        #
#                                                                                 #
# AUTHOR: Ian Cromwell, MSc.                                                      #
# DATE: June, 2018                                                                #
#                                                                                 #
# DESCRIPTION: This program reads in .csv files from the WDMOC, containing        #
#               discounted LYG, QALYs, and costs. It produces estimates of the    #
#               ICER, QICER, and Cost-effectiveness planes and CEACs.             #
#                                                                                 #
###################################################################################

### SET WORKING DIRECTORY
'
setwd("H:\PACER\Lymphoma LSARP\Modelling\DLBCL\DES Model\Model Code\DLBCL_DES_COO")
'
### LOAD REQUIRED PACKAGES

library(BCEA)
library(coda)
library(MCMCpack)

### STEP 1: Read in .csv files from the model run
  CEA_Outputs  <- read.table("CEA_Outputs.csv", sep=",", stringsAsFactors=FALSE,)

### STEP 2: Calculate incremental cost, effectiveness
  # A - Intervention
  # B - Comparator
  
  LYG_A  <- CEA_Outputs[,4]
  QALY_A <- CEA_Outputs[,5]
  Cost_A <- CEA_Outputs[,6]
  
  LYG_B  <- CEA_Outputs[,1]
  QALY_B <- CEA_Outputs[,2]
  Cost_B <- CEA_Outputs[,3]
  
  DeltaE <- LYG_A - LYG_B
  DeltaQ <- QALY_A - QALY_B
  DeltaC <- Cost_A - Cost_B
  
  ICER <- round((mean(Cost_A) - mean(Cost_B))/(mean(LYG_A) - mean(LYG_B)), digits=2)
  QICER <- round((mean(Cost_A) - mean(Cost_B))/(mean(QALY_A) - mean(QALY_B)), digits=2)
  
  CEACost <- c('Cost - Alt:', round(mean(Cost_A), digits=2), round(sd(Cost_A), digits=2),"||",
               'Cost - Comp:', round(mean(Cost_B), digits=2), round(sd(Cost_B), digits=2),"||",
               'DeltaC:', round(mean(Cost_A) - mean(Cost_B), digits=2))
  
  CEALYG <- c('LYG - Alt:', round(mean(LYG_A), digits=4), round(sd(LYG_A), digits=4), "||",
              'LYG - Comp:', round(mean(LYG_B), digits=4), round(sd(LYG_B), digits=4), "||",
              'DeltaE:', round(mean(LYG_A) - mean(LYG_B) , digits=4))
  
  CEAQALY <- c('QALY - Alt:', round(mean(QALY_A), digits=4), round(sd(QALY_A), digits=4), "||",
              'QALY - Comp:', round(mean(QALY_B), digits=4), round(sd(QALY_B), digits=4), "||",
              'DeltaE:', round(mean(QALY_A) - mean(QALY_B) , digits=4))
  
  CEASummary <- c(CEACost, CEAQALY)
  
### STEP 3: Run BCEA function to produce CEPlanes, CEACs
  
  n = nrow(CEA_Outputs)
  BCEA_DC <- cbind(Cost_A, Cost_B)
  BCEA_DE <- cbind(LYG_A, LYG_B)
  BCEA_DQ <- cbind(QALY_A, QALY_B)
  
  #BICER <- bcea(e=BCEA_DE, c=BCEA_DC, interventions = c("Alternative", "Comparator"), Kmax=100000)
  BQALY <- bcea(e=BCEA_DQ, c=BCEA_DC, interventions = c("Alternative", "Comparator"), Kmax=100000)
  
  #ceplane.plot(BICER, wtp=100000)
  ceplane.plot(BQALY, wtp=100000)
  
  #ceac.plot(BICER)
  ceac.plot(BQALY)
  
### STEP 4: Conduct EVPPI
  
  # Read in the .csv files with parameter names and sampled values 
  EVPPI_Names  <- read.table("EVPPI_namearray.csv", sep=",", stringsAsFactors=FALSE,)
  EVPPI_Params <- read.table("EVPPI_valsarray.csv", sep=",", stringsAsFactors=FALSE,)
    colnames(EVPPI_Names) <- c("LY", "QALY", "Cost")
  
  
EVPPI_paramvals <- cbind(rate_reduc_ABC, reduc_recur_ABC, c_GEP, c_GEP_recur,
                         q_CR_GEP, q_fail_GEP,
                         rate_reduc_GCB, rate_reduc_undef, rate_reduc_Dhit,
                         reduc_recur_GCB, reduc_recur_undef, reduc_recur_Dhit,
                         c_assay, c_assay_recur,
                         p_ABC, p_GCB, p_undef, p_Dhit
)

VOI <- evppi(c(2,4,5,6), EVPPI_paramvals, plot=TRUE, BCEA.QALY)
minval <- min(which(VOI$evppi >0))
maxval <- which.max(VOI$evppi)
hundval <- which(VOI$k == 100000)
VOI$k[minval]
VOI$evppi[maxval]
VOI$k[maxval]
VOI$evppi[hundval]