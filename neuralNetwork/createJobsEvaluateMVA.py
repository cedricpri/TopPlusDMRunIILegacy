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

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

########################## Main program #####################################
if __name__ == "__main__":
    
    # ===========================================                                                        
    # Argument parser                                                                                    
    # ===========================================                                                        
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0', add_help_option=False)
    parser.add_option('-c', '--cmssw', action='store', type=str, dest='cmssw', default="/afs/cern.ch/user/c/cprieels/work/public/TopPlusDMRunIILegacy/CMSSW_10_4_0/") #CMSSW release
    parser.add_option('-w', '--weightsDir', action='store', type=str, dest='weightsDir', default="scalar_LO_Mchi_1_Mphi_100_default") #Directory(ies) where the weights are stored and waiting for application, without the year, as a comma separated string
    parser.add_option('-y', '--year', action='store', type=int, dest='year', default=2018)
    parser.add_option('-d', '--data', action='store_true', dest='data') #Process a data file or background/signal?
    parser.add_option('-f', '--fakes', action='store_true', dest='fakes') #Process a fakes file?
    parser.add_option('-q', '--query', action='store', type=str, dest='query', default="*") #String to be matched when searching for the files (do not use the nanoLatino prefix!)
    parser.add_option('-h', '--threshold', action='store', type=float, dest='threshold', default=-1.0) #Threshold for background assignment
    parser.add_option('-g', '--groupJobs', action='store', type=int, dest='groupJobs', default=4) #Group jobs before sending them to the queue

    parser.add_option('-r', '--resubmit', action='store_true', dest='resubmit') #Resubmit only files that failed based on the log files and missing Tree events
    parser.add_option('-t', '--test', action='store_true', dest='test') #Only process a few files and a few events, for testing purposes
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    cmssw = opts.cmssw
    weightsDir = opts.weightsDir
    year = opts.year
    data = opts.data
    fakes = opts.fakes
    query = opts.query
    threshold = opts.threshold
    groupJobs = opts.groupJobs

    test = opts.test
    resubmit = opts.resubmit
    verbose = opts.verbose

    if verbose:
        print("=================================================")
        print("-> OPTIONS USED:")
        print("CMSSW: " + str(cmssw))
        print("Data: " + str(data))
        print("Fakes: " + str(fakes))
        print("Weights directory: " + str(weightsDir))
        print("Year: " + str(year))
        print("Query: " + str(query))
        print("Threshold: " + str(threshold))
        print("Test: " + str(test))
        print("Resubmit: " + str(resubmit))
        print("=================================================")

    baseDir = os.getcwd() + "/"
 
    if year == 2018:
        if data:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2018_102X_nAODv7_Full2018v7/DATAl1loose2018v7__l2loose__l2tightOR2018v7/"
        elif fakes:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2018_102X_nAODv7_Full2018v7/DATAl1loose2018v7__l2loose__fakeW/"
        else:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7__MCCorr2018v7__l2loose__l2tightOR2018v7/"
                    
    elif year == 2017:
        if data:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2017_102X_nAODv7_Full2017v7/DATAl1loose2017v7__l2loose__l2tightOR2017v7/"
        elif fakes:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2017_102X_nAODv7_Full2017v7/DATAl1loose2017v7__l2loose__fakeW/"
        else:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Fall2017_102X_nAODv7_Full2017v7/MCl1loose2017v7__MCCorr2017v7__l2loose__l2tightOR2017v7/"

    elif year == 2016:
        if data:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2016_102X_nAODv7_Full2016v7/DATAl1loose2016v7__l2loose__l2tightOR2016v7/"
        elif fakes:
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Run2016_102X_nAODv7_Full2016v7/DATAl1loose2016v7__l2loose__fakeW/"
        else:            
            inputDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Summer16_102X_nAODv7_Full2016v7/MCl1loose2016v7__MCCorr2016v7__l2loose__l2tightOR2016v7/" 

    else:
        inputDir = ""
        print("The year option has to be used, and the year should be 2016, 2017 or 2018.")
    outputDir = inputDir[:-1] + "_weighted/"

    #Move all the files in folder to the global directory
    for root, dirs, files in os.walk(outputDir):
        for subdir in dirs: 
            filesInSubdir = fnmatch.filter(os.listdir(root + subdir), 'nanoLatino*' + query + '*')
            for fileInSubdir in filesInSubdir:
                try:
                    os.remove(outputDir + fileInSubdir)
                except Exception as e:
                    pass

                shutil.move(os.path.join(root + subdir, fileInSubdir), outputDir)

    exit
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
                    else:
                        
                        resubmitThis = False
                        for weight in weightsDir.split(","):
                            if threshold == -1.0 and (not tree.GetBranch("TTbar_DNN_output_signal_" + weight) or not tree.GetBranch("ST_DNN_output_signal_" + weight)):
                                resubmitThis = True
                            elif threshold > -1.0 and (not tree.GetBranch("TTbar_DNN_output_signal_" + weight + "_threshold_" + str(threshold)) or not tree.GetBranch("ST_DNN_output_signal_" + weight + "_threshold_" + str(threshold))):
                                resubmitThis = True

                        if resubmitThis:        
                            filesToResubmit.append(fileToProcess)
                except Exception as e:
                    print(e)
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

    chunckedProcesses = list(chunks(filesToProcess, groupJobs))
    for index, i in enumerate(chunckedProcesses):
        
        executable = baseDir + "/runMVA.py -e -f " + ','.join(i) + " -i " + inputDir + " -d " + baseDir + " -w " + weightsDir + " -y " + str(year) + " --threshold " + str(threshold)
        
        if test:
            executable = executable + " -t"

        template = templateCONDOR
        template = template.replace('CMSSWRELEASE', cmssw)
        template = template.replace('EXENAME', executable) 
            
        if fakes:
            f = open('sh/send_' + i[0].replace('.root', '') + '_fakes_' + str(year) + '.sh', 'w')
        else:
            f = open('sh/send_' + i[0].replace('.root', '') + '_' + str(year) + '.sh', 'w')
        f.write(template)
        f.close()

        if fakes:
            os.chmod('sh/send_' + i[0].replace('.root', '') + '_fakes_' + str(year) + '.sh', 0755)     
        else:
            os.chmod('sh/send_' + i[0].replace('.root', '') + '_' + str(year) + '.sh', 0755)     

    print(str(len(filesToProcess)) + " file(s) matching the requirements have been found.")
