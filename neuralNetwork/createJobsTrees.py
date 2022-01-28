import os, sys, stat, fnmatch, shutil
import ROOT as r
from array import array
import optparse, re

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
    parser.add_option('-f', '--fakes', action='store_true', dest='fakes', default=False) #Process the fakes?
    parser.add_option('-y', '--year', action='store', type=int, dest='year', default=2018)
    parser.add_option('-o', '--outputDir', action='store', type=str, dest='outputDir', default="/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/") #Output directory where to keep the output files
    parser.add_option('-q', '--query', action='store', type=str, dest='query', default="*") #String to be matched when searching for the files (without the nanoLatino prefix)
    parser.add_option('-p', '--split', action='store', type=int, dest='split', default=1) #Do we want to divide the input file to speed up the process?
    parser.add_option('-e', '--systematic', action='store', type=str, dest='systematic', default="") #Systematic suffix

    parser.add_option('-t', '--test', action='store_true', dest='test') #Only process a few files and a few events, for testing purposes
    parser.add_option('-r', '--resubmit', action='store_true', dest='resubmit') #Resubmit only files that failed based on the log files and missing Tree events
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    cmssw = opts.cmssw
    signal = opts.signal
    data = opts.data
    fakes = opts.fakes
    year = opts.year
    outputDir = opts.outputDir
    query = opts.query
    split = opts.split
    systematic = opts.systematic

    test = opts.test
    resubmit = opts.resubmit
    verbose = opts.verbose

    if signal:
        data = False
        fakes = False
    if fakes:
        data = False
        signal = False

    if verbose:
        print("=================================================")
        print("OPTIONS USED:")
        print("CMSSW release: " + str(cmssw))
        print("Signal: " + str(signal))
        print("Data: " + str(data))
        print("Fakes: " + str(fakes))
        print("Year: " + str(year))
        print("Output directory: " + str(outputDir))
        print("Test: " + str(test))
        print("Query: " + str(query))
        print("Split: " + str(split))
        print("Resubmit: " + str(resubmit))
        print("=================================================")

    #Three different directories are used: the inputDir, where the original latino files are, the outputDir, where to keep the output, and baseDir, the current path where the distributions.root file is.
    baseDir = os.getcwd() + "/"
    trailer = "/"
    nomin = "Smear"

    if year == 2018:
        if signal:
            baseInputDir = "/eos/user/c/cprieels/work/JonatanEOS/Autumn18_102X_nAODv7_Full2018v7/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyNomin2018v6loose__susyMT2recoNomin"
            if systematic != "":
                inputDir = baseInputDir + "__susyMT2reco" + systematic + "/"
            else:
                inputDir = baseInputDir + trailer
        elif data:
            inputDir = "/eos/user/s/scodella/SUSY/Nano/Run2018_102X_nAODv6_Full2018v6loose/DATASusy2018v6__hadd__susyMT2recoNomin/"
        elif fakes:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2018_102X_nAODv7_Full2018v7/DATAl1loose2018v7__l2loose__fakeW/"
        else:
            if systematic == "JESDo":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Autumn18_102X_nAODv6_Full2018v6loose/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyJESDo2018v6loose__susyMT2recoJESDo/"
            elif systematic == "JESUp":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Autumn18_102X_nAODv6_Full2018v6loose/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyJESUp2018v6loose__susyMT2recoJESUp/"
            elif systematic == "METDo":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Autumn18_102X_nAODv6_Full2018v6loose/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyNomin2018v6loose__susyMT2recoMETDo/"
            elif systematic == "METUp":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Autumn18_102X_nAODv6_Full2018v6loose/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyNomin2018v6loose__susyMT2recoMETUp/"
            else:
                inputDir = "/eos/user/s/scodella/SUSY/Nano/Autumn18_102X_nAODv6_Full2018v6loose/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyNomin2018v6loose__susyMT2reco" + nomin + trailer

    elif year == 2017:
        if signal:
            baseInputDir = "/eos/user/c/cprieels/work/JonatanEOS/Fall2017_102X_nAODv7_Full2017v7/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyNomin2017v6loose__susyMT2recoNomin"
            if systematic != "":
                inputDir = baseInputDir + "__susyMT2reco" + systematic + "/"
            else:
                inputDir = baseInputDir + trailer
        elif data:
            inputDir = "/eos/cms/store/caf/user/scodella/BTV/Nano/Run2017_102X_nAODv6_Full2017v6loose/DATASusy2017v6__hadd__susyMT2recoNomin/"
        elif fakes:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2017_102X_nAODv7_Full2017v7/DATAl1loose2017v7__l2loose__fakeW/"
        else:
            if systematic == "JESDo":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Fall2017_102X_nAODv6_Full2017v6loose/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyJESDo2017v6loose__susyMT2recoJESDo/"
            elif systematic == "JESUp":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Fall2017_102X_nAODv6_Full2017v6loose/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyJESUp2017v6loose__susyMT2recoJESUp/"
            elif systematic == "METDo":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Fall2017_102X_nAODv6_Full2017v6loose/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyNomin2017v6loose__susyMT2recoMETDo/"
            elif systematic == "METUp":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Fall2017_102X_nAODv6_Full2017v6loose/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyNomin2017v6loose__susyMT2recoMETUp/"
            else:
                inputDir = "/eos/cms/store/caf/user/scodella/BTV/Nano/Fall2017_102X_nAODv6_Full2017v6loose/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyNomin2017v6loose__susyMT2reco" + nomin + trailer

    elif year == 2016:
        if signal:
            baseInputDir = "/eos/user/c/cprieels/work/JonatanEOS/Summer16_102X_nAODv7_Full2016v7loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyNomin2016v6loose__susyMT2recoNomin"
            if systematic != "":
                inputDir = baseInputDir + "__susyMT2reco" + systematic + "/"
            else:
                inputDir = baseInputDir + trailer
        elif data:
            inputDir = "/eos/cms/store/user/scodella/SUSY/Nano/Run2016_102X_nAODv6_Full2016v6loose/DATASusy2016v6__hadd__susyMT2recoNomin/"
        elif fakes:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2016_102X_nAODv7_Full2016v7/DATAl1loose2016v7__l2loose__fakeW/"
        else:
            if systematic == "JESDo":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Summer16_102X_nAODv6_Full2016v6loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyJESDo2016v6loose__susyMT2recoJESDo/"
            elif systematic == "JESUp":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Summer16_102X_nAODv6_Full2016v6loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyJESUp2016v6loose__susyMT2recoJESUp/"
            elif systematic == "METDo":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Summer16_102X_nAODv6_Full2016v6loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyNomin2016v6loose__susyMT2recoMETDo/"
            elif systematic == "METUp":
                inputDir = "/eos/user/c/cprieels/work/TreesWithSystematics/Summer16_102X_nAODv6_Full2016v6loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyNomin2016v6loose__susyMT2recoMETUp/"
            else:
                inputDir = "/eos/cms/store/user/scodella/SUSY/Nano/Summer16_102X_nAODv6_Full2016v6loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyNomin2016v6loose__susyMT2reco" + nomin + trailer

    else:
        inputDir = ""
        print("The year option has to be used, and the year should be 2016, 2017 or 2018.")

    productionName = "/".join(inputDir.split('/')[-3:])

    try:
        os.makedirs('sh')
        os.makedirs('log')
    except:
        pass #Directories already exists, this is fine

    #Move all the files in folder to the global directory
    outputDirWithSubfolders = outputDir + "/" + productionName

    #Remove all the ".root" in folder names
    if resubmit:
        stringstoremove = [".root"]
        try:
            for folder in next(os.walk(outputDirWithSubfolders))[1]:
                newFolder = folder
                for stringtoremove in stringstoremove :
                    newFolder = newFolder.replace( stringtoremove, '')
            
                if folder != newFolder :  # don't rename if it's the same
                    os.rename( outputDirWithSubfolders + folder, outputDirWithSubfolders + newFolder )
        except:
            print("No folders found")

    for root, dirs, files in os.walk(outputDirWithSubfolders):
        for subdir in dirs:
            oldSubdir = subdir
            #subdir = subdir.replace(".root", "")
            #os.rename(outputDirWithSubfolders + "/" + oldSubdir, outputDirWithSubfolders + "/" + subdir)
            filesInSubdir = fnmatch.filter(os.listdir(root + subdir), 'nanoLatino*' + query + '*')

            for fileInSubdir in filesInSubdir:
                try:
                    os.remove(outputDirWithSubfolders + fileInSubdir)
                    pass
                except Exception as e:
                    pass

                try:
                    shutil.move(os.path.join(outputDirWithSubfolders + subdir, fileInSubdir), outputDirWithSubfolders)
                except Exception as e:
                    pass

    #Find the files to process based on the arguments given
    filesToProcess = []

    if inputDir != "":
        matchingFilesFound = fnmatch.filter(os.listdir(inputDir), 'nanoLatino*' + query + '*')
        for matchingFileFound in matchingFilesFound:

            if split != 1:
                f = r.TFile.Open(inputDir + "/" + matchingFileFound)
                nEvents = f.Get("Events").GetEntries()/split

                for splitNumber in range(split):
                    firstEvent = (splitNumber * nEvents) + 1
                    lastEvent = (splitNumber+1) * nEvents
                    fileToProcess = {
                        "inputName": matchingFileFound,
                        "outputName": matchingFileFound.replace('.root', '') + "_" + str(splitNumber) + '.root',
                        "firstEvent": firstEvent,
                        "lastEvent": lastEvent,
                        "splitNumber": splitNumber
                    }
                    filesToProcess.append(fileToProcess)
            else:
                fileToProcess = {
                        "inputName": matchingFileFound,
                        "outputName": matchingFileFound,
                        "firstEvent": -1,
                        "lastEvent": -1,
                        "splitNumber": -1
                    }
                filesToProcess.append(fileToProcess)
   
    #Resubmit only the files that ran into an error previously
    if resubmit:
        filesToResubmit = []

        print("The resubmit process might take a while in order to open each output file and check that the tree Events is present.")
        for fileToProcess in filesToProcess:

            #Check if the file is missing in the output directory
            fileToCheck = outputDir + "/" + productionName + fileToProcess['outputName']
            print(fileToCheck)
            if not os.path.exists(fileToCheck):
                #if data or fakes or signal or query != "*":
                filesToResubmit.append(fileToProcess)
                #pass
            else: #If the file exists, check if the tree Events has been created successfully
                print("  --> Opening " + fileToProcess['outputName'] + " to check for the presence of the Events tree.")
                try:
                    f = r.TFile.Open(fileToCheck)
                    tree = f.Get("Events")
                    if not f.GetListOfKeys().Contains("Events"):
                        filesToResubmit.append(fileToProcess)
                        os.remove(fileToCheck)
                except:
                    filesToResubmit.append(fileToProcess)
                    try:
                        os.remove(fileToCheck)
                        pass
                    except Exception as e:
                        pass
    
        filesToProcess = filesToResubmit

    #If the test option is used, then only process a single file
    if test:
        try:
            filesToProcess = [filesToProcess[0]]
        except:
            print("No file matching the requirements has been found.")

    #Now, delete all the folders we don't need any more
    try:
        foldersFound = fnmatch.filter(os.listdir(outputDirWithSubfolders), 'nanoLatino*')
        for folderFound in foldersFound:
            #print(outputDir + folderFound, os.path.isdir(outputDir + folderFound))
            if os.path.isdir(outputDirWithSubfolders + folderFound):
                shutil.rmtree(outputDirWithSubfolders + folderFound)
    except Exception as e:
        pass

    #Write the executable needed for each file to process
    for fileToProcess in filesToProcess:

        executable = baseDir + "/createTrees.py -f " + fileToProcess['inputName'] + " -i " + inputDir + " -o " + outputDir + " -b " + baseDir + " -y " + str(year)
        executable = executable + " --splitNumber " + str(fileToProcess['splitNumber']) + " --firstEvent " + str(fileToProcess['firstEvent']) + " --lastEvent " + str(fileToProcess['lastEvent'])

        if verbose:
            executable = executable + " -v"

        template = templateCONDOR
        template = template.replace('EXENAME', executable) 
        template = template.replace('CMSSWRELEASE', cmssw)

        if fakes:
            f = open('sh/send_' + fileToProcess['outputName'].replace('.root', '') + '_fakes.sh', 'w')
        else:
            f = open('sh/send_' + fileToProcess['outputName'].replace('.root', '') + systematic + '.sh', 'w')
        f.write(template)
        f.close()

        if fakes:
            os.chmod('sh/send_' + fileToProcess['outputName'].replace('.root', '') + '_fakes.sh', 0755)     
        else:
            os.chmod('sh/send_' + fileToProcess['outputName'].replace('.root', '') + systematic + '.sh', 0755)     

    print(str(len(filesToProcess)) + " file(s) matching the requirements have been found.")

