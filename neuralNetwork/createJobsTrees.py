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
    parser.add_option('-s', '--signal', action='store_true', dest='signal', default=False) #Process the signal or background files?
    parser.add_option('-d', '--data', action='store_true', dest='data', default=False) #Process the data or background files?
    parser.add_option('-y', '--year', action='store', type=int, dest='year', default=2018)
    parser.add_option('-o', '--outputDir', action='store', type=str, dest='outputDir', default="/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/") #Output directory where to keep the files
    parser.add_option('-q', '--query', action='store', type=str, dest='query', default="*") #String to be matched when searching for the files (without the nanoLatino prefix)

    parser.add_option('-t', '--test', action='store_true', dest='test') #Only process a few files and a few events, for testing purposes
    parser.add_option('-r', '--resubmit', action='store_true', dest='resubmit') #Resubmit only files that failed
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    cmssw = opts.cmssw
    signal = opts.signal
    data = opts.data
    year = opts.year
    outputDir = opts.outputDir
    query = opts.query

    test = opts.test
    resubmit = opts.resubmit
    verbose = opts.verbose

    if signal:
        data = False

    if verbose:
        print("=================================================")
        print("OPTIONS USED:")
        print("CMSSW release: " + str(cmssw))
        print("Signal: " + str(signal))
        print("Data: " + str(data))
        print("Year: " + str(year))
        print("Output directory: " + str(outputDir))
        print("Test: " + str(test))
        print("Query: " + str(query))
        print("Resubmit: " + str(resubmit))
        print("=================================================")

    #Three different directories are used: the inputDir, where the original latino files are, the outputDir, where to keep the output, and baseDir, the current path where the distributions.root file is.
    baseDir = os.getcwd()
 
    if year == 2018:
        if signal:
            inputDir = "/eos/user/c/cprieels/work/SignalsPostProcessing/Pablo/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
        elif data:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2018_102X_nAODv6_Full2018v6/DATAl1loose2018v6__l2loose__l2tightOR2018v6/"
        else:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
    elif year == 2017:
        if signal:
            inputDir = "/eos/user/c/cprieels/work/SignalsPostProcessing/Pablo/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6/"
        elif data:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2017_102X_nAODv5_Full2017v6/DATAl1loose2017v6__l2loose__l2tightOR2017v6/"
        else:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6/"
    elif year == 2016:
        if signal:
            inputDir = "/eos/user/c/cprieels/work/SignalsPostProcessing/Pablo/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6/" 
        elif data:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2016_102X_nAODv5_Full2016v6/DATAl1loose2016v6__l2loose__l2tightOR2016v6/"
        else:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6/"
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

    #If the resubmit option is set, then remove from this list the files that are already found in the output directory
    if resubmit:
        outputDirProduction = "/".join(inputDir.split('/')[-3:-1])+"/"
        outputDirComplete = outputDir + outputDirProduction
        alreadyFound = os.listdir(outputDirComplete)

        filesToProcess = [x for x in filesToProcess if x not in alreadyFound] #Remove the files not needed

    for i in filesToProcess:

        executable = baseDir + "/createTrees.py -f " + i + " -i " + inputDir + " -o " + outputDir + " -b " + baseDir 
        if verbose:
            executable = executable + " -v"

        template = templateCONDOR
        template = template.replace('CMSSWRELEASE', cmssw)
        template = template.replace('EXENAME', executable) 

        f = open('sh/send_' + i.replace('.root', '') + '.sh', 'w')
        f.write(template)
        f.close()
        os.chmod('sh/send_' + i.replace('.root', '') + '.sh', 0755)     

    print(str(len(filesToProcess)) + " file(s) matching the requirements have been found.")
