import os, sys
import ROOT as r
from array import array







########################## Main program #####################################
if __name__ == "__main__":

    nameOfInputFile = sys.argv[1]
    nameOfModel = sys.argv[2]
    nameOfDir = sys.argv[3]
    nameOfModelGen = 'GenModel_' + nameOfModel
    listOfModels = []
    listOfModelsRaw = []
    listOfModels.append(nameOfModelGen)
    listOfModelsRaw.append(nameOfModel)
    thefile = r.TFile(nameOfInputFile)
    thetree = thefile.Get("Events")
    theRuns = thefile.Get("Runs")
    listOfTrees = []
    listOfRuns = []
    listOfFiles = []
    genEventSumw2_ = array('f', [0.])
    genEventSumw_ = array('f', [0.]) 
    genEventCount_ = array('i', [0])


    for model in listOfModels:
        thefile_ = r.TFile(nameOfDir + '/' + model.replace('genModel', 'nanoLatino').replace('_TuneCP5_13TeV_madgraph_mcatnlo_pythia8', '') + '.root', 'recreate')
        thefile_.cd()
        listOfFiles.append(thefile_)
        thenewtree = thetree.CloneTree(0)
        thenewtree.Reset()
        listOfTrees.append(thenewtree)
        thenewrun = r.TTree("Runs", "Runs")
        thenewrun.Branch("genEventSumw2_", genEventSumw2_, "genEventSumw2_/F")
        thenewrun.Branch("genEventSumw_", genEventSumw_, "genEventSumw_/F")
        thenewrun.Branch("genEventCount_", genEventCount_, "genEventCount_/I")
        listOfRuns.append(thenewrun)


    nevents = thetree.GetEntries()
    for j, ev in enumerate(thetree):
        for i, model in enumerate(listOfModels):
            variable = '(ev.' + model + ' == 1)'
            if(eval(variable)):
                listOfFiles[i].cd()
                listOfTrees[i].Fill()
    

    for j, model in enumerate(listOfModelsRaw):
        vargenEventSumw2_ = 'genEventSumw2_' + model
        vargenEventSumw_ = 'genEventSumw_' + model
        vargenEventCount_ = 'genEventCount_' + model
        if theRuns.FindBranch(vargenEventSumw2_) == 0:
            continue
        genEventSumw2_[0] = 0
        genEventSumw_[0] = 0
        genEventCount_[0] = 0
        for run in theRuns:
            genEventSumw2_[0] += eval('run.' + vargenEventSumw2_)
            genEventSumw_[0] += eval('run.' + vargenEventSumw_)
            genEventCount_[0] += eval('run.' + vargenEventCount_)
        listOfFiles[j].cd()
        listOfRuns[j].Fill()  


          
    for j, tree in enumerate(listOfTrees):
        listOfFiles[j].cd()
        listOfTrees[j].Write()
        listOfRuns[j].Write()
        listOfFiles[j].Close()

    thefile.Close()














     

