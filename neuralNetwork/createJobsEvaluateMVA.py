import os, sys, stat, fnmatch, shutil
import ROOT as r
from array import array
import optparse

templateCONDOR = """#!/bin/bash
pushd CMSSWRELEASE/src
eval `scramv1 runtime -sh`
pushd
python EXENAME WORKINGPATH 
"""

########################## Main program #####################################
if __name__ == "__main__":
    
    # ===========================================                                                        
    # Argument parser                                                                                    
    # ===========================================                                                        
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-c', '--cmssw', action='store', type=str, dest='cmssw', default="/afs/cern.ch/user/c/cprieels/work/public/TopPlusDMRunIILegacy/CMSSW_10_4_0/") #CMSSW release
    parser.add_option('-y', '--year', action='store', type=int, dest='year', default=2018)
    parser.add_option('-q', '--query', action='store', type=str, dest='query', default="*") #String to be matched when searching for the files

    parser.add_option('-t', '--test', action='store_true', dest='test') #Only process a few files and a few events, for testing purposes
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    cmssw = opts.cmssw
    year = opts.year
    query = opts.query

    test = opts.test
    verbose = opts.verbose

    if verbose:
        print("=================================================")
        print("-> OPTIONS USED:")
        print("CMSSW: " + str(cmssw))
        print("Year: " + str(year))
        print("Query: " + str(query))
        print("Test: " + str(test))
        print("=================================================")

    workingpath = os.getcwd()
 
    if year == 2018:
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
    elif year == 2017:
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6/"
    elif year == 2016:
        inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6/" 
    else:
        inputDir = ""
        print("The year option has to be used, and the year should be 2016, 2017 or 2018.")

    filesToProcess = []
    if inputDir != "":
        filesToProcess = fnmatch.filter(os.listdir(inputDir), 'nanoLatino*' + query + '*')

    if test: #If the test option is used, then only process a single file
        try:
            filesToProcess = [filesToProcess[0]]
        except:
            print("No file matching the requirements has been found.")

    try:
        #shutil.rmtree('sh')
        os.makedirs('sh')
    except:
        pass #Directory already exists, this is fine

    for i in filesToProcess:

        executable = workingpath + "/runMVA.py -e -f " + i + " -d " + inputDir
        
        if test:
            executable = executable + " -t"

            template = templateCONDOR
            template = template.replace('CMSSWRELEASE', cmssw)
            template = template.replace('EXENAME', executable) 
            template = template.replace('WORKINGPATH', workingpath) 
                
            f = open('sh/send_' + i.replace('.root', '') + '.sh', 'w')
            f.write(template)
            f.close()
            os.chmod('sh/send_' + i.replace('.root', '') + '.sh', 0755)     

    print(str(len(filesToProcess)) + " file(s) matching the requirements have been found.")
