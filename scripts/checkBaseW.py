import os, sys, stat, fnmatch, shutil
import ROOT as r

#Check the baseW value obtained for a sample
processToSearch = "nanoLatino_DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000*"
directoryToSearch = "/eos/user/c/cprieels/work/SignalsPostProcessing/Pablo/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
processCrossSection = 0.0002863

baseWFound = 0.0
baseWComputed = 0.0
totalEventCount = 0
totalSumW = 0

print("Now reading all the trees corresponding to the process given. This might take a while.")

matchingFilesFound = fnmatch.filter(os.listdir(directoryToSearch), processToSearch)
for matchingFileFound in matchingFilesFound:

    print("     --> Opening " + str(matchingFileFound))
    f = r.TFile.Open(directoryToSearch + "/" + matchingFileFound, "read")
    if baseWFound == 0.0:
        for index, ev in enumerate(f.Events):
            baseWFound = ev.baseW

    for index, ev in enumerate(f.Runs):
        totalEventCount += ev.genEventCount_
        totalSumW += ev.genEventSumw_

print("Total event count: " + str(totalEventCount) + " and total sumW: " + str(totalSumW))
print("Now computing the cross section.")

baseWComputed = processCrossSection * 1000 / totalSumW
print("BaseW value found: " + str(baseWFound) + " and value computed: " + str(baseWComputed) + " (" + str(round(baseWComputed*100/baseWFound, 2)) + "%)")
