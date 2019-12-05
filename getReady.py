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
    #Leptons
    Lepton0_pt  = array("f", [0.])
    Lepton1_pt  = array("f", [0.])
    Lepton0_eta = array("f", [0.])
    Lepton1_eta = array("f", [0.])
    Lepton0_phi = array("f", [0.])
    Lepton1_phi = array("f", [0.])

    #Jets
    CleanJet0_pt  = array("f", [0.])
    CleanJet1_pt  = array("f", [0.])
    CleanJet0_eta = array("f", [0.])
    CleanJet1_eta = array("f", [0.])
    njet          = array("f", [0.])

    #bJets
    CleanbJet0_pt  = array("f", [0.])
    CleanbJet1_pt  = array("f", [0.])
    CleanbJet0_eta = array("f", [0.])
    CleanbJet1_eta = array("f", [0.])
    nbjet          = array("f", [0.])

    #Additional variables
    PuppiMET_pt = array("f", [0.])
    MET_pt      = array("f", [0.])
    TkMET_pt    = array("f", [0.])
    mT2         = array("f", [0.])
    dphill      = array("f", [0.])
    dphillmet   = array("f", [0.])
    mll         = array("f", [0.])
    mtw1        = array("f", [0.])
    mtw2        = array("f", [0.])
    mth         = array("f", [0.])

    #Set the branches
    outputTree.Branch("Lepton0_pt", Lepton0_pt, "Lepton0_pt/F")
    outputTree.Branch("Lepton1_pt", Lepton1_pt, "Lepton1_pt/F")
    outputTree.Branch("Lepton0_eta", Lepton0_eta, "Lepton0_eta/F")
    outputTree.Branch("Lepton1_eta", Lepton1_eta, "Lepton1_eta/F")
    outputTree.Branch("Lepton0_phi", Lepton0_phi, "Lepton0_phi/F")
    outputTree.Branch("Lepton1_phi", Lepton1_phi, "Lepton1_phi/F")

    outputTree.Branch("CleanJet0_pt", CleanJet0_pt, "CleanJet0_pt/F")
    outputTree.Branch("CleanJet1_pt", CleanJet1_pt, "CleanJet1_pt/F")
    outputTree.Branch("CleanJet0_eta", CleanJet0_eta, "CleanJet0_eta/F")
    outputTree.Branch("CleanJet1_eta", CleanJet1_eta, "CleanJet1_eta/F")
    outputTree.Branch("njet", njet, "njet/F")

    outputTree.Branch("CleanbJet0_pt", CleanbJet0_pt, "CleanbJet0_pt/F")
    outputTree.Branch("CleanbJet1_pt", CleanbJet1_pt, "CleanbJet1_pt/F")
    outputTree.Branch("CleanbJet0_eta", CleanbJet0_eta, "CleanbJet0_eta/F")
    outputTree.Branch("CleanbJet1_eta", CleanbJet1_eta, "CleanbJet1_eta/F")
    outputTree.Branch("nbjet", nbjet, "nbjet/F")

    outputTree.Branch("PuppiMET_pt", PuppiMET_pt, "PuppiMET_pt/F")
    outputTree.Branch("MET_pt", MET_pt, "MET_pt/F")
    outputTree.Branch("TkMET_pt", TkMET_pt, "TkMET_pt/F")
    outputTree.Branch("mT2", mT2, "mT2/F")
    outputTree.Branch("dphill", dphill, "dphill/F")
    outputTree.Branch("dphillmet", dphillmet, "dphillmet/F")
    outputTree.Branch("mll", mll, "mll/F")
    outputTree.Branch("mtw1", mtw1, "mtw1/F")
    outputTree.Branch("mtw2", mtw2, "mtw2/F")
    outputTree.Branch("mth", mth, "mth/F")

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
    
        #Leptons
        Lepton0_pt[0] = ev.Lepton_pt[0]
        if(len(ev.Lepton_pt) > 1):
            Lepton1_pt[0] = ev.Lepton_pt[1]

        Lepton0_eta[0] = ev.Lepton_eta[0]
        if(len(ev.Lepton_eta) > 1):
            Lepton1_eta[0] = ev.Lepton_eta[1]

        Lepton0_phi[0] = ev.Lepton_phi[0]
        if(len(ev.Lepton_phi) > 1):
            Lepton1_phi[0] = ev.Lepton_phi[1]

        #Jets
        nJets = 0
        for jet in ev.CleanJet_jetIdx:
            if nJets < 2:
                if nJets == 0:
                    nJets = 1
                    CleanJet0_pt[0] = ev.Jet_pt[jet]
                    CleanJet0_eta[0] = ev.Jet_eta[jet]
                if nJets == 1:
                    nJets = 2
                    CleanJet1_pt[0] = ev.Jet_pt[jet]
                    CleanJet1_eta[0] = ev.Jet_eta[jet]

        njet = ev.njet;

        #bJets
        nBjets = 0
        for jet in ev.CleanJet_jetIdx:
            if nBjets < 2:
                if ev.Jet_btagDeepB[jet] > 0.2217 and nBjets == 0:
                    nBjets = 1
                    CleanbJet0_pt[0] = ev.Jet_pt[jet]
                    CleanbJet0_eta[0] = ev.Jet_eta[jet]
                if ev.Jet_btagDeepB[jet] > 0.2217 and nBjets == 1:
                    nBjets = 2
                    CleanbJet1_pt[0] = ev.Jet_pt[jet]
                    CleanbJet1_eta[0] = ev.Jet_eta[jet]
                elif ev.Jet_btagDeepB[jet] > 0.2217:
                    nBjets = nBjets + 1

        nbjet = nBjets

        #Additional variables
        PuppiMET_pt[0] = ev.PuppiMET_pt;
        MET_pt[0] = ev.MET_pt;
        TkMET_pt[0] = ev.TkMET_pt;
        mT2[0] = ev.mT2;
        dphill[0] = ev.dphill;
        dphillmet[0] = ev.dphillmet;
        mll[0] = ev.mll;
        mtw1[0] = ev.mtw1;
        mtw2[0] = ev.mtw2;
        mth[0] = ev.mth;

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
