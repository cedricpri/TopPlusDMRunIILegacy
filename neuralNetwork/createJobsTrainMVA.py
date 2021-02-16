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
    parser.add_option('-b', '--backgroundQuery', action='store', type=str, dest='backgroundQuery', default="TTTo2L2Nu__part,ST_s-channel_ext1,ST_t-channel_antitop,ST_t-channel_top,ST_tW_antitop_ext1,ST_tW_top_ext1") #Comma separated string to be matched when searching for the files

    #Additional options
    parser.add_option('-t', '--test', action='store_true', dest='test')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    cmssw = opts.cmssw
    year = opts.year
    tag = opts.tag
    signalQuery = opts.signalQuery
    backgroundQuery = opts.backgroundQuery
    test = opts.test
    verbose = opts.verbose

    if verbose:
        print("=================================================")
        print("-> OPTIONS USED:")
        print("CMSSW: " + str(cmssw))
        print("Year: " + str(year))
        print("Tag: " + str(tag))
        print("Signal query: " + str(signalQuery))
        print("Background query: " + str(backgroundQuery))
        print("=================================================")

    baseDir = os.getcwd() + "/"
 
    if year == 2018:
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7__MCCorr2018v7__l2loose__l2tightOR2018v7/"
        #inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
    elif year == 2017:
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Fall2017_102X_nAODv7_Full2017v7/MCl1loose2017v7__MCCorr2017v7__l2loose__l2tightOR2017v7/"
        #inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6/"
    elif year == 2016:
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Summer16_102X_nAODv7_Full2016v7/MCl1loose2016v7__MCCorr2016v7__l2loose__l2tightOR2016v7/" 
        #inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6/" 
    else:
        inputDir = ""
        print("The year option has to be used, and the year should be 2016, 2017 or 2018.")
    #Watch out! The files in these directories will be overwritten when using the evaluate option

    signalProcesses = [str(item) for item in signalQuery.split(",")]
    backgroundProcesses = [str(item) for item in backgroundQuery.split(",")]

    signalFilesToProcess = []
    backgroundFilesToProcess = []
    if inputDir != "":
        
        maxFiles = 20000
        if test: #If the test option is used, then only consider a few files for each process
            maxFiles = 50

        for i, signalProcess in enumerate(signalProcesses):
            if signalProcess != "":
                signalFilesToProcess.append(','.join(fnmatch.filter(os.listdir(inputDir), 'nanoLatino*' + signalProcess + '*.root'))) #For now we keep all the signal files as then have less stat
        for i, backgroundProcess in enumerate(backgroundProcesses):
            if backgroundProcess != "":
                backgroundFilesToProcess.append(','.join(fnmatch.filter(os.listdir(inputDir), 'nanoLatino*' + backgroundProcess + '*.root')[:maxFiles])) 
        
    try:
        #shutil.rmtree('sh')
        os.makedirs('sh')
    except:
        pass #Directory already exists, this is fine

    #If we train the MVA, then we want to pass a list of all the files to process, the python code will know how to deal with it
    executable = baseDir + "/runMVA.py -i " + inputDir + " -d " + baseDir

    #Add the files as arguments
    executable = executable + " -s " + ','.join(signalFilesToProcess)
    executable = executable + " -b " + ','.join(backgroundFilesToProcess).replace(',,', ',')
    executable = executable + " -y " + str(year)
    if tag != '':
        executable = executable + " --tags " + str(tag)

    template = templateCONDOR
    template = template.replace('CMSSWRELEASE', cmssw)
    template = template.replace('EXENAME', executable) 
                
    f = open('sh/send_trainMVA_' + str(year) + "_" + str(signalProcesses[0][:-1]) + '.sh', 'w')
    f.write(template)
    f.close()
    os.chmod('sh/send_trainMVA_' + str(year) + "_" + str(signalProcesses[0][:-1]) + '.sh', 0755)     

    print(str(len(signalFilesToProcess)) + " signal file(s) matching the requirements have been found.")
    print(str(len(backgroundFilesToProcess)) + " background file(s) matching the requirements have been found.")
