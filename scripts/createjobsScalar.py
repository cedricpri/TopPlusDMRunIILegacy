import os, sys, stat
import ROOT as r
from array import array



listOfModelsRaw = ['TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_300_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_350_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_50_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_40_Mphi_100_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_55_Mphi_100_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_250_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_100_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_500_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_51_Mphi_100_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_20_Mphi_100_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_400_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_450_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_45_Mphi_100_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_150_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_30_Mphi_100_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_200_TuneCP5_13TeV_madgraph_mcatnlo_pythia8',
'TTbarDMJets_Dilepton_scalar_LO_Mchi_49_Mphi_100_TuneCP5_13TeV_madgraph_mcatnlo_pythia8']



templateCONDOR = """#!/bin/bash
pushd CMSSWRELEASE/src
eval `scramv1 runtime -sh`
pushd
python EXENAME INPUTFILE MODEL WORKINGPATH 
"""


########################## Main program #####################################
if __name__ == "__main__":

    nameOfInputFile = sys.argv[1]
    cmsswRelease = sys.argv[2]
    workingpath = os.getcwd()
    executable = workingpath + "/read.py"
 
    for i in listOfModelsRaw:

        template = templateCONDOR
        template = template.replace('CMSSWRELEASE', cmsswRelease)
        template = template.replace('EXENAME', executable) 
        template = template.replace('INPUTFILE', nameOfInputFile) 
        template = template.replace('MODEL', i) 
        template = template.replace('WORKINGPATH', workingpath) 

        f = open('send_' + i + '.sh', 'w')
        f.write(template)
        f.close()
        os.chmod('send_' + i + '.sh', 0755)     
    













     

