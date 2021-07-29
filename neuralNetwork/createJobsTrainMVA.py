import os, sys, stat, fnmatch, shutil
import ROOT as r
from array import array
import random
import optparse

templateCONDOR = """#!/bin/bash
pushd CMSSWRELEASE/src
eval `scramv1 runtime -sh`
pushd
python EXENAME
"""

########################## Main program #####################################
if __name__ == "__main__":
    
    # ===========================================                                                        
    # Argument parser                                                                                    
    # ===========================================                                                        
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')

    #Setup
    parser.add_option('-c', '--cmssw', action='store', type=str, dest='cmssw', default="/afs/cern.ch/user/c/cprieels/work/public/TopPlusDMRunIILegacy/CMSSW_10_4_0/") #CMSSW release
    
    #Files to be considered
    parser.add_option('-y', '--year', action='store', type=int, dest='year', default=2018) 
    parser.add_option('-g', '--tag', action='store', type=str, dest='tag', default="") #Tag to identify the training performed
    parser.add_option('-s', '--signalQuery', action='store', type=str, dest='signalQuery', default="TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_100_,DMscalar_Dilepton_top_tWChan_Mchi1_Mphi100_") #Comma separated string to be matched when searching for the files (do not use the nanoLatino prefix!)
    parser.add_option('-m', '--mediator', action='store', type=str, dest='mediator', default="scalar")
    parser.add_option('-b', '--backgroundQuery', action='store', type=str, dest='backgroundQuery', default="TTTo2L2Nu__part,ST_s-channel_ext1,ST_t-channel_antitop,ST_t-channel_top,ST_tW_antitop_ext1,ST_tW_top_ext1") #Comma separated string to be matched when searching for the files
    parser.add_option('-r', '--singleTop', action='store_true', dest='singleTopRegion', default=False)

    #Additional options
    parser.add_option('-t', '--test', action='store_true', dest='test')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    cmssw = opts.cmssw
    year = opts.year
    tag = opts.tag
    signalQuery = opts.signalQuery
    mediator = opts.mediator
    backgroundQuery = opts.backgroundQuery
    singleTopRegion = opts.singleTopRegion
    test = opts.test
    verbose = opts.verbose

    if verbose:
        print("=================================================")
        print("-> OPTIONS USED:")
        print("CMSSW: " + str(cmssw))
        print("Year: " + str(year))
        print("Tag: " + str(tag))
        print("Signal query: " + str(signalQuery))
        print("Mediator: " + str(mediator))
        print("Background query: " + str(backgroundQuery))
        print("Single top region: " + str(singleTopRegion))
        print("=================================================")

    baseDir = os.getcwd() + "/"
 
    if year == 2018:
        signalInputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv7_Full2018v7/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyNomin2018v6loose__susyMT2recoNomin/"
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv6_Full2018v6loose/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyNomin2018v6loose__susyMT2recoNomin/"
    elif year == 2017:
        signalInputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Fall2017_102X_nAODv7_Full2017v7/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyNomin2017v6loose__susyMT2recoNomin/"
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Fall2017_102X_nAODv6_Full2017v6loose/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyNomin2017v6loose__susyMT2recoNomin/"
    elif year == 2016:
        signalInputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Summer16_102X_nAODv7_Full2016v7loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyNomin2016v6loose__susyMT2recoNomin/"
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Summer16_102X_nAODv6_Full2016v6loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyNomin2016v6loose__susyMT2recoNomin/"
    else:
        print("The year option has to be used, and the year should be 2016, 2017 or 2018.")
        exit()

    signalProcesses = [str(item) for item in signalQuery.split(",")]
    backgroundProcesses = [str(item) for item in backgroundQuery.split(",")]

    mediatorString1 = "DM" + mediator
    mediatorString2 = "_" + mediator

    signalFilesToProcess = []
    backgroundFilesToProcess = []
    if inputDir != "":
        
        maxFiles = 20000
        if test: #If the test option is used, then only consider a few files for each process
            maxFiles = 50

        for i, signalProcess in enumerate(signalProcesses):
            if signalProcess != "":
                signalFilesToProcess.append(','.join(fnmatch.filter(os.listdir(signalInputDir), 'nanoLatino*' + mediatorString1 + "*" + signalProcess + '*.root'))) #For now we keep all the signal files as they have less stat
                signalFilesToProcess.append(','.join(fnmatch.filter(os.listdir(signalInputDir), 'nanoLatino*' + mediatorString2 + "*" + signalProcess + '*.root'))) #For now we keep all the signal files as they have less stat
        for i, backgroundProcess in enumerate(backgroundProcesses):
            if backgroundProcess != "":
                backgroundFilesToProcess.append(','.join(fnmatch.filter(os.listdir(inputDir), 'nanoLatino*' + backgroundProcess + '*.root')[:maxFiles])) 
    
    signalFilesToProcessWithFolder = [s.replace('nanoLatino_', signalInputDir + 'nanoLatino_') for s in signalFilesToProcess]
    backgroundFilesToProcessWithFolder = [s.replace('nanoLatino_', inputDir + 'nanoLatino_') for s in backgroundFilesToProcess]

    try:
        #shutil.rmtree('sh')
        os.makedirs('sh')
    except:
        pass #Directory already exists, this is fine

    #If we train the MVA, then we want to pass a list of all the files to process, the python code will know how to deal with it
    executable = baseDir + "/runMVA.py -i \"\" -d " + baseDir

    #Add the files as arguments
    executable = executable + " -s " + ','.join(signalFilesToProcessWithFolder)
    executable = executable + " -b " + ','.join(backgroundFilesToProcessWithFolder).replace(',,', ',')
    executable = executable + " -y " + str(year)
    executable = executable + " -r " + str(singleTopRegion)

    trailer = ""

    if tag != '':
        if singleTopRegion:
            tag = tag + "_ST"
        else:
            tag = tag + "_TTbar"
    else:
        if singleTopRegion:
            tag = "ST"
        else:
            tag = "TTbar"

    executable = executable + " --tags " + str(tag)
    if tag != "":
        trailer = "_" + str(tag) + "_" + mediator
    else:
        trailer = "_" + mediator

    template = templateCONDOR
    template = template.replace('CMSSWRELEASE', cmssw)
    template = template.replace('EXENAME', executable) 
                
    f = open('sh/send_trainMVA_' + str(year) + "_" + str(signalProcesses[0][:-1]) + trailer + '.sh', 'w')
    f.write(template)
    f.close()
    os.chmod('sh/send_trainMVA_' + str(year) + "_" + str(signalProcesses[0][:-1]) + trailer + '.sh', 0755)     

    print(str(len(signalFilesToProcess)) + " signal process(es) matching the requirements have been found.")
    print(str(len(backgroundFilesToProcess)) + " background process(es) matching the requirements have been found.")
