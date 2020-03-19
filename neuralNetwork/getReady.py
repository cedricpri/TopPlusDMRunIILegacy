#Code used to read the input files for dnn.py and create additional variables we use for the discrimination
from ROOT import TFile, TTree, TLorentzVector
from array import array
import optparse
import os, sys

import numpy as np
LinAlgError = np.linalg.linalg.LinAlgError
import ttbar #ttbar reconstruction

#=========================================================================================================
# HELPERS
#=========================================================================================================
#Progress bar
def updateProgress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
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

#=========================================================================================================
# TREE CREATION
#=========================================================================================================
def createTree(filename):
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
    Lepton0_pdgId = array("f", [0.])
    Lepton1_pdgId = array("f", [0.])
    Lepton0_mass = array("f", [0.])
    Lepton1_mass = array("f", [0.])

    #Jets
    Jet0_pt  = array("f", [0.])
    Jet1_pt  = array("f", [0.])
    Jet0_eta = array("f", [0.])
    Jet1_eta = array("f", [0.])
    Jet0_phi = array("f", [0.])
    Jet1_phi = array("f", [0.])
    njet          = array("i", [0])

    #bJets
    bJet0_pt  = array("f", [0.])
    bJet1_pt  = array("f", [0.])
    bJet0_eta = array("f", [0.])
    bJet1_eta = array("f", [0.])
    bJet0_phi = array("f", [0.])
    bJet1_phi = array("f", [0.])
    nbjet          = array("i", [0])

    #Additional variables
    PuppiMET_pt = array("f", [0.])
    PuppiMET_phi = array("f", [0.])
    PuppiMET_sumEt = array("f", [0.])
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
    outputTree.Branch("Lepton0_pdgId", Lepton0_pdgId, "Lepton0_pdgId/F")
    outputTree.Branch("Lepton1_pdgId", Lepton1_pdgId, "Lepton1_pdgId/F")
    outputTree.Branch("Lepton0_mass", Lepton0_mass, "Lepton0_mass/F")
    outputTree.Branch("Lepton1_mass", Lepton1_mass, "Lepton1_mass/F")

    outputTree.Branch("Jet0_pt", Jet0_pt, "Jet0_pt/F")
    outputTree.Branch("Jet1_pt", Jet1_pt, "Jet1_pt/F")
    outputTree.Branch("Jet0_eta", Jet0_eta, "Jet0_eta/F")
    outputTree.Branch("Jet1_eta", Jet1_eta, "Jet1_eta/F")
    outputTree.Branch("Jet0_phi", Jet0_eta, "Jet0_phi/F")
    outputTree.Branch("Jet1_phi", Jet1_eta, "Jet1_phi/F")
    outputTree.Branch("njet", njet, "njet/I")

    outputTree.Branch("bJet0_pt", bJet0_pt, "bJet0_pt/F")
    outputTree.Branch("bJet1_pt", bJet1_pt, "bJet1_pt/F")
    outputTree.Branch("bJet0_eta", bJet0_eta, "bJet0_eta/F")
    outputTree.Branch("bJet1_eta", bJet1_eta, "bJet1_eta/F")
    outputTree.Branch("bJet0_phi", bJet0_phi, "bJet0_phi/F")
    outputTree.Branch("bJet1_phi", bJet1_phi, "bJet1_phi/F")
    outputTree.Branch("nbjet", nbjet, "nbjet/I")

    outputTree.Branch("PuppiMET_pt", PuppiMET_pt, "PuppiMET_pt/F")
    outputTree.Branch("PuppiMET_phi", PuppiMET_phi, "PuppiMET_phi/F")
    outputTree.Branch("PuppiMET_sumEt", PuppiMET_sumEt, "PuppiMET_sumEt/F")
    outputTree.Branch("MET_pt", MET_pt, "MET_pt/F")
    outputTree.Branch("TkMET_pt", TkMET_pt, "TkMET_pt/F")
    outputTree.Branch("mT2", mT2, "mT2/F")
    outputTree.Branch("dphill", dphill, "dphill/F")
    outputTree.Branch("dphillmet", dphillmet, "dphillmet/F")
    outputTree.Branch("mll", mll, "mll/F")
    outputTree.Branch("mtw1", mtw1, "mtw1/F")
    outputTree.Branch("mtw2", mtw2, "mtw2/F")
    outputTree.Branch("mth", mth, "mth/F")

    nEvents = inputFile.Events.GetEntries()
    recoAttempts = 0
    recoWorked = 0

    print("Let's start with the loop")

    for index, ev in enumerate(inputFile.Events):
        if index % 200 == 0: #Update the loading bar every 100 events                                                                                              
            updateProgress(round(index/float(nEvents), 2))

        #Skimming and preselection
        if ev.njet < 2:
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

        Lepton0_pdgId[0] = ev.Lepton_pdgId[0]
        Lepton0_mass[0] = 0.000511 if (abs(Lepton0_pdgId[0]) == 11) else 0.106; #Mass in GeV needed for ttbar reconstruction
        if(len(ev.Lepton_pdgId) > 1):
            Lepton1_pdgId[0] = ev.Lepton_pdgId[1]
            Lepton1_mass[0] = 0.000511 if (abs(Lepton1_pdgId[0]) == 11) else 0.106;

        #Jets
        nJets = 0
        for jet in ev.CleanJet_jetIdx:
            nJets = nJets + 1
            if nJets < 2:
                if nJets == 0:
                    Jet0_pt[0] = ev.Jet_pt[jet]
                    Jet0_eta[0] = ev.Jet_eta[jet]
                    Jet0_phi[0] = ev.Jet_phi[jet]
                elif nJets == 1:
                    Jet1_pt[0] = ev.Jet_pt[jet]
                    Jet1_eta[0] = ev.Jet_eta[jet]
                    Jet1_phi[0] = ev.Jet_phi[jet]
                 
        njet[0] = nJets

        #bJets
        nBjets = 0
	bJetIndex = [] #First of all, we are going to keep in an array the jet indices corresponding to the bjets in the jet collection

        for jet in ev.CleanJet_jetIdx:
            if ev.Jet_btagDeepB[jet] > 0.2217: #For now, we use the loose WP for the b-tag
                bJetIndex.append(jet)
 		if ev.Jet_btagDeepB[jet] > 0.2217 and nBjets == 0:
                    nBjets = 1
                    bJet0_pt[0] = ev.Jet_pt[jet]
                    bJet0_eta[0] = ev.Jet_eta[jet]
                    bJet0_phi[0] = ev.Jet_phi[jet]
		elif ev.Jet_btagDeepB[jet] > 0.2217 and nBjets == 1:
                    nBjets = 2
                    bJet1_pt[0] = ev.Jet_pt[jet]
                    bJet1_eta[0] = ev.Jet_eta[jet]
                    bJet1_phi[0] = ev.Jet_phi[jet]
            	elif ev.Jet_btagDeepB[jet] > 0.2217:
                    nBjets = nBjets + 1
   
	nbjet[0] = nBjets

        #Additional variables
        PuppiMET_pt[0] = ev.PuppiMET_pt;
        PuppiMET_phi[0] = ev.PuppiMET_phi;
        PuppiMET_sumEt[0] = ev.PuppiMET_sumEt;
        MET_pt[0] = ev.MET_pt;
        TkMET_pt[0] = ev.TkMET_pt;
        mT2[0] = ev.mT2;
        dphill[0] = ev.dphill;
        dphillmet[0] = ev.dphillmet;
        mll[0] = ev.mll;
        mtw1[0] = ev.mtw1;
        mtw2[0] = ev.mtw2;
        mth[0] = ev.mth;

        #===================================================
        #ttbar reconstruction
        #===================================================
        
        if verbose:
            print("===================================\n")

        Tb1   = TLorentzVector()
        Tb2   = TLorentzVector()
        Tlep1 = TLorentzVector()
        Tlep2 = TLorentzVector()
        Tnu1  = TLorentzVector()
        Tnu2  = TLorentzVector()
        TMET  = TLorentzVector()
        
        listOfBJetsCandidates = []
        if len(bJetIndex) == 0:
            continue #We don't consider events having less than 1 bjet
        elif len(bJetIndex) > 1:
            listOfBJetsCandidates = bJetIndex 
        else: #If we have exactly one bjet, then we keep it as the first element of listOfBJetsCandidates.append while the rest of the list will be made out of usual jets for which we will try to apply the ttbar reconstruction, to try and recover some efficiency of the b-tagging
            listOfBJetsCandidates.append(bJetIndex[0])
            for jet in ev.CleanJet_jetIdx:
                if jet == bJetIndex[0]:
                    continue
                else:
                    listOfBJetsCandidates.append(jet)

        #We have different combinations to perform the reconstruction: we consider the association of the bjets with the two leptons, and we consider all the different bjets
	successfullCombinations = [] #List used to keep the lepton/b-jet indexes for which the reconstruction is working

        Tlep1.SetPtEtaPhiM(Lepton0_pt[0], Lepton0_eta[0], Lepton0_phi[0], Lepton0_mass[0])
        Tlep2.SetPtEtaPhiM(Lepton1_pt[0], Lepton1_eta[0], Lepton1_phi[0], Lepton1_mass[0])
                        
        for i, jet in enumerate(listOfBJetsCandidates):
            if i == 0:
                Tb1.SetPtEtaPhiM(ev.Jet_pt[jet], ev.Jet_eta[jet], ev.Jet_phi[jet], ev.Jet_mass[jet]) #By construction, we know that the first element of listOfBJetsCandidates is a bjet
            else:
                Tb2.SetPtEtaPhiM(ev.Jet_pt[jet], ev.Jet_eta[jet], ev.Jet_phi[jet], ev.Jet_mass[jet])
                Tnu1.SetPtEtaPhiM(-99.0, -99.0, -99.0, -99.0) #Not needed for the ttbar reconstruction and not available, we can pass default values
                Tnu2.SetPtEtaPhiM(-99.0, -99.0, -99.0, -99.0)
                TMET.SetPtEtaPhiM(PuppiMET_pt[0], -99.0, PuppiMET_phi[0], -99.0)

                mW1 = 82-0
                mW2 = 82.0
                mt1 = 173.0
                mt2 = 173.0

                if verbose:
                    print("Tb1: " + str(Tb1.Print()))
                    print("Tb2: " + str(Tb2.Print()))
                    print("Lep1: " + str(Tlep1.Print()))
                    print("Lep2: " + str(Tlep2.Print()))
                    print("MET: " + str(TMET.Print()))
                
                try:
                    nuSol=ttbar.solveNeutrino(Tb1, Tb2, Tlep1, Tlep2, Tnu1, Tnu2, TMET, mW1, mW2, mt1, mt2)
                    successfullCombinations.append([0, listOfBJetsCandidates[0], 1, jet])             
                except LinAlgError :
                    if verbose: 
                        print('There is no solution for the ttbar reconstruction for event number '+ str(index))
                    
                #Now we do the same by switching the two leptons
                try:
                    nuSol=ttbar.solveNeutrino(Tb1, Tb2, Tlep2, Tlep1, Tnu1, Tnu2, TMET, mW1, mW2, mt1, mt2)
                    successfullCombinations.append([0, jet, 1, listOfBJetsCandidates[0]])             
                except LinAlgError :
                    if verbose:
                        print('There is no solution for the ttbar reconstruction for event number '+ str(index))
        
        recoAttempts = recoAttempts + 1
        if verbose: 
            print 'Number of solutions', len(successfullCombinations) 

        #Count the number of times the reco worked
        if len(successfullCombinations) != 0:
            recoWorked = recoWorked + 1

        outputTree.Fill()

    print 'The ttbar reconstruction worked for ' + str(round((recoWorked/float(recoAttempts))*100, 2)) + '% of the events considered'
    
    outputTree.Write()
    inputFile.Close()
    outputFile.Close()

if __name__ == "__main__":
    # =========================================== 
    # Argument parser                            
    # ===========================================
    
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-f', '--filename', action='store', type=str, dest='filename', default='', help='Name of the file to be read')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    filename = opts.filename
    verbose = opts.verbose

    if filename is not "":
        createTree(filename)
    else:
        print "The filename option has to be used"
