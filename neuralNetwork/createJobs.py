import os, sys, stat, fnmatch, shutil
import ROOT as r
from array import array
import optparse

templateCONDOR = """#!/bin/bash
pushd CMSSWRELEASE/src
eval `scramv1 runtime -sh`
pushd
python EXENAME INPUTFILE MODEL WORKINGPATH 
"""

########################## Main program #####################################
if __name__ == "__main__":
    
    # ===========================================                                                        
    # Argument parser                                                                                    
    # ===========================================                                                        
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-y', '--year', action='store', type=int, dest='year', default=2018)
    parser.add_option('-c', '--cmssw', action='store', type=str, dest='cmssw', default="/afs/cern.ch/user/c/cprieels/work/public/TopPlusDMRunIILegacy/CMSSW_10_4_0/") #Cmssw release
    parser.add_option('-s', '--signal', action='store_true', dest='signal', default=False) #Process the signal or background files?
    parser.add_option('-d', '--data', action='store_true', dest='data', default=False) #Process the data?
    parser.add_option('-a', '--allFiles', action='store_true', dest='allFiles', default=False) #Process all the files or just one?
    parser.add_option('-t', '--searchTerm', action='store', type=str, dest='searchTerm', default="*") #String to be matched when searching for the files
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    year = opts.year
    cmssw = opts.cmssw
    signal = opts.signal
    data = opts.data
    allFiles = opts.allFiles #Launch the processing of all the files found
    searchTerm = opts.searchTerm
    verbose = opts.verbose

    if signal:
        data = False

    print("=================================================")
    print("-> OPTIONS USED:")
    print("Year: " + str(year))
    print("CMSSW: " + str(cmssw))
    print("Signal: " + str(signal))
    print("Data: " + str(data))
    print("All files: " + str(allFiles))
    print("searchTerm: " + str(searchTerm))
    print("=================================================")

    workingpath = os.getcwd()
 
    if year == 2018:
        if signal:
            inputDir = "/eos/user/c/cprieels/work/SignalsPostProcessing/Pablo/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
        elif data:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/DATAl1loose2018v6__l2loose__l2tightOR2018v6/"
        else:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
    elif year == 2017:
        if signal:
            inputDir = "/eos/user/c/cprieels/work/SignalsPostProcessing/Pablo/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6/"
        elif data:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/DATAl1loose2017v6__l2loose__l2tightOR2017v6/"
        else:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6/"
    elif year == 2016:
        if signal:
            inputDir = "/eos/user/c/cprieels/work/SignalsPostProcessing/Pablo/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6/" 
        elif data:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/DATAl1loose2016v6__l2loose__l2tightOR2016v6/"
        else:
            inputDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6/"
    else:
        inputDir = ""
        print("The year option has to be used, and the year should be 2016, 2017 or 2018.")

    filesToProcess = []
    if inputDir != "":
        if signal:
            filesToProcess = fnmatch.filter(os.listdir(inputDir), 'nanoLatino*'+searchTerm+'*')
        else:
            filesToProcess = fnmatch.filter(os.listdir(inputDir), 'nanoLatino*'+searchTerm+'*')

    if not allFiles:
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

        executable = workingpath + "/getReady.py -f" + i + " -d" + inputDir
        if verbose:
            executable = executable + " -v"

        template = templateCONDOR
        template = template.replace('CMSSWRELEASE', cmssw)
        template = template.replace('EXENAME', executable) 
        template = template.replace('INPUTFILE', i) 
        template = template.replace('MODEL', i) 
        template = template.replace('WORKINGPATH', workingpath) 

        f = open('sh/send_' + i.replace('.root', '') + '.sh', 'w')
        f.write(template)
        f.close()
        os.chmod('sh/send_' + i.replace('.root', '') + '.sh', 0755)     
    













     

