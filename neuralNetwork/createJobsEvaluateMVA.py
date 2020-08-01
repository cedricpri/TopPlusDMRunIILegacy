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
    parser.add_option('-m', '--massPoints', action='store', type=str, dest='massPoints', default="scalar_LO_Mchi_1_Mphi_100") #Mass points training to be read (comma separated string)
    parser.add_option('-y', '--year', action='store', type=int, dest='year', default=2018)
    parser.add_option('-d', '--data', action='store_true', dest='data') #Process a data file or background/signal?
    parser.add_option('-f', '--fakes', action='store_true', dest='fakes') #Process a fakes file?a
    parser.add_option('-q', '--query', action='store', type=str, dest='query', default="*") #String to be matched when searching for the files (do not use the nanoLatino prefix!)

    parser.add_option('-r', '--resubmit', action='store_true', dest='resubmit') #Resubmit only files that failed based on the log files and missing Tree events
    parser.add_option('-t', '--test', action='store_true', dest='test') #Only process a few files and a few events, for testing purposes
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    cmssw = opts.cmssw
    massPoints = opts.massPoints
    year = opts.year
    data = opts.data
    fakes = opts.fakes
    query = opts.query

    test = opts.test
    resubmit = opts.resubmit
    verbose = opts.verbose

    if verbose:
        print("=================================================")
        print("-> OPTIONS USED:")
        print("CMSSW: " + str(cmssw))
        print("Data: " + str(data))
        print("Fakes: " + str(fakes))
        print("Mass points: " + str(massPoints))
        print("Year: " + str(year))
        print("Query: " + str(query))
        print("Test: " + str(test))
        print("Resubmit: " + str(resubmit))
        print("=================================================")

    baseDir = os.getcwd() + "/"
 
    if year == 2018:
        if data:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2018_102X_nAODv6_Full2018v6/DATAl1loose2018v6__l2loose__l2tightOR2018v6/"
        elif fakes:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2018_102X_nAODv6_Full2018v6/DATAl1loose2018v6__l2loose__fakeW/"
        else:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
                    
    elif year == 2017:
        if data:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2017_102X_nAODv5_Full2017v6/DATAl1loose2017v6__l2loose__l2tightOR2017v6/"
        elif fakes:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2017_102X_nAODv5_Full2017v6/DATAl1loose2017v6__l2loose__fakeW/"
        else:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6/"

    elif year == 2016:
        if data:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2016_102X_nAODv5_Full2016v6/DATAl1loose2016v6__l2loose__l2tightOR2016v6/"
        elif fakes:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2016_102X_nAODv5_Full2016v6/DATAl1loose2016v6__l2loose__fakeW/"
        else:            
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6/" 

    else:
        inputDir = ""
        print("The year option has to be used, and the year should be 2016, 2017 or 2018.")
    outputDir = inputDir[:-1] + "_weighted/"

    filesToProcess = []
    if inputDir != "":
        filesToProcess = fnmatch.filter(os.listdir(inputDir), 'nanoLatino*' + query + '*')

    #Resubmit only the files that ran into an error previously
    if resubmit:
        filesToResubmit = []

        print("The resubmit process might take a while in order to open each output file and check that the tree Events is present.")
        for fileToProcess in filesToProcess:

            #Check if the file is missing in the output directory
            if not os.path.exists(outputDir + fileToProcess): 
                filesToResubmit.append(fileToProcess)
            else: #If the file exists, check if the tree Events has been created successfully
                print("  --> Opening " + fileToProcess + " to check for the presence of the Events tree.")
                try:
                    f = r.TFile.Open(outputDir + fileToProcess)
                    tree = f.Get("Events")
                    if not f.GetListOfKeys().Contains("Events"):
                        filesToResubmit.append(fileToProcess)
                except:
                    filesToResubmit.append(fileToProcess)

        filesToProcess = filesToResubmit

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

        executable = baseDir + "/runMVA.py -e -f " + i + " -i " + inputDir + " -d " + baseDir + " -m " + massPoints
        
        if test:
            executable = executable + " -t"

        template = templateCONDOR
        template = template.replace('CMSSWRELEASE', cmssw)
        template = template.replace('EXENAME', executable) 

        f = open('sh/send_' + i.replace('.root', '') + '.sh', 'w')
        f.write(template)
        f.close()
        os.chmod('sh/send_' + i.replace('.root', '') + '.sh', 0755)     

    print(str(len(filesToProcess)) + " file(s) matching the requirements have been found.")
