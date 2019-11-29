#Code used to read the input files for dnn.py and create additional variables we use for the discrimination
from ROOT import TFile, TTree
from array import array
import optparse
import os, sys

#Progress bar
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar                                                                                            
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done!\r\n"
    block = int(round(barLength*progress))
    text = "\rProgress: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

def createTree(filename):
    print("Now starting up and getting everything ready... This might take a while.")
    inputFile = TFile.Open(filename)
    inputTree = inputFile.Get("Events")

    #Create a directory to keep the files if it does not already exist
    outputDirectory = "rootfiles"
    try:
        os.stat(outputDirectory)
    except:
        os.mkdir(outputDirectory)
    os.chdir(outputDirectory)

    outputFile = TFile.Open(filename[:-5] + "_dnn.root", "recreate")
    outputTree = TTree("Events", "New events tree")

    #Set the variables we want to keep
    Lepton_pt = array("f", [0.])
    Lepton_eta = array("f", [0.])

    #Set the branches
    outputTree.Branch("Lepton_pt", Lepton_pt, "Lepton_pt/F")
    outputTree.Branch("Lepton_eta", Lepton_eta, "Lepton_eta/F")

    nEvents = 0
    for ev in inputFile.Events:
        nEvents += 1

    print("Let's start with the loop")

    for index, ev in enumerate(inputFile.Events):
        if index % 10 == 0: #Update the loading bar every 10 events                                                                                              
            update_progress(index/float(nEvents))

        if ev.njet == 0:
            continue
        if ev.Lepton_pt[0] < 20. or ev.Lepton_pt[1] < 20.:
            continue
    
        Lepton_pt = ev.Lepton_pt
        Lepton_eta = ev.Lepton_eta
    
        outputTree.Fill()

    outputTree.Write()
    inputFile.Close()
    outputFile.Close()

if __name__ == "__main__":
    # =========================================== 
    # Argument parser                            
    # ===========================================
    
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-f', '--filename', action='store', type=str, dest='filename', default='', help='Name of the file to be read')
    (opts, args) = parser.parse_args()

    filename = opts.filename

    if filename is not "":
        createTree(filename)
    else:
        print "The filename option has to be used"
