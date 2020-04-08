import os, sys, stat, fnmatch, shutil
import ROOT as r
from array import array
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
    parser.add_option('-c', '--cmssw', action='store', type=str, dest='cmssw', default="/afs/cern.ch/user/c/cprieels/work/public/TopPlusDMRunIILegacy/CMSSW_10_4_0/") #CMSSW release
    parser.add_option('-y', '--year', action='store', type=int, dest='year', default=2018)
    parser.add_option('-s', '--signalQuery', action='store', type=str, dest='signalQuery', default="TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_100") #String to be matched when searching for the files (do not use the nanoLatino prefix!)
    parser.add_option('-b', '--backgroundQuery', action='store', type=str, dest='backgroundQuery', default="TTTo2L2Nu__part") #String to be matched when searching for the files

    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    cmssw = opts.cmssw
    year = opts.year
    signalQuery = opts.signalQuery
    backgroundQuery = opts.backgroundQuery

    verbose = opts.verbose

    if verbose:
        print("=================================================")
        print("-> OPTIONS USED:")
        print("CMSSW: " + str(cmssw))
        print("Year: " + str(year))
        print("Signal query: " + str(signalQuery))
        print("Background query: " + str(backgroundQuery))
        print("=================================================")

    baseDir = os.getcwd() + "/"
 
    if year == 2018:
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
    elif year == 2017:
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6/"
    elif year == 2016:
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6/" 
    else:
        inputDir = ""
        print("The year option has to be used, and the year should be 2016, 2017 or 2018.")
    #Watch out! The files in these directories will be overwritten

    signalFilesToProcess = []
    backgroundFilesToProcess = []
    if inputDir != "":
        signalFilesToProcess = fnmatch.filter(os.listdir(inputDir), 'nanoLatino*' + signalQuery + '*')
        backgroundFilesToProcess = fnmatch.filter(os.listdir(inputDir), 'nanoLatino*' + backgroundQuery + '*')
        
    try:
        #shutil.rmtree('sh')
        os.makedirs('sh')
    except:
        pass #Directory already exists, this is fine

    #If we train the MVA, then we want to pass a list of all the files to process, the python code will know how to deal with it
    executable = baseDir + "/runMVA.py -i " + inputDir + " -d " + baseDir

    #Add the files as arguments
    executable = executable + " -s " + ','.join(signalFilesToProcess)
    executable = executable + " -b " + ','.join(backgroundFilesToProcess)
    executable = executable + " -y " + str(year)

    template = templateCONDOR
    template = template.replace('CMSSWRELEASE', cmssw)
    template = template.replace('EXENAME', executable) 
                
    f = open('sh/send_trainMVA.sh', 'w')
    f.write(template)
    f.close()
    os.chmod('sh/send_trainMVA.sh', 0755)     

    print(str(len(signalFilesToProcess)) + " signal file(s) matching the requirements have been found.")
    print(str(len(backgroundFilesToProcess)) + " background file(s) matching the requirements have been found.")
