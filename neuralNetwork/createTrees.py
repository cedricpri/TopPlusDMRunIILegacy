#Code used to read the input files for dnn.py and create additional variables we use for the discrimination
from ROOT import TFile, TTree, TLorentzVector
from array import array
import optparse
import os, sys, fnmatch

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
def createTree(inputDir, filename):
    print("\n\n --> Now considering file... " + filename)

    inputFile = TFile.Open(inputDir+filename)
    inputTree = inputFile.Get("Events")

    #Create a directory to keep the files if it does not already exist
    outputDirectory = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/"
    outputDirectoryProduction = "/".join(inputDir.split('/')[-3:-1])+"/"
    outputDirectory = outputDirectory + outputDirectoryProduction #Add a final name to distinguish between 2016, 2017 and 2018 files
    try:
        os.stat(outputDirectory)
    except:
        os.makedirs(outputDirectory)

    outputFile = TFile.Open(outputDirectory + filename, "recreate")
    outputTree = inputTree.CloneTree(0)

    #Select the branches we want to keep
    outputTree.SetBranchStatus("*", 0);

    #Leptons
    outputTree.SetBranchStatus("nLepton", 1);
    outputTree.SetBranchStatus("Lepton_pt", 1);
    outputTree.SetBranchStatus("Lepton_eta", 1);
    outputTree.SetBranchStatus("Lepton_pdgId", 1);
    outputTree.SetBranchStatus("Lepton_promptgenmatched", 1);
    
    #Jets
    outputTree.SetBranchStatus("nJet", 1);
    outputTree.SetBranchStatus("Jet_btagDeepB", 1);
    outputTree.SetBranchStatus("Jet_btagSF_shape", 1);

    #Clean jets
    outputTree.SetBranchStatus("nCleanJet", 1);
    outputTree.SetBranchStatus("CleanJet_pt", 1);
    outputTree.SetBranchStatus("CleanJet_eta", 1);
    outputTree.SetBranchStatus("CleanJet_phi", 1);
    outputTree.SetBranchStatus("CleanJet_jetIdx", 1);

    #Additional discriminating variables
    outputTree.SetBranchStatus("PuppiMET_pt", 1);
    outputTree.SetBranchStatus("PuppiMET_phi", 1);
    outputTree.SetBranchStatus("PuppiMET_sumEt", 1);
    outputTree.SetBranchStatus("MET_pt", 1);
    outputTree.SetBranchStatus("TkMET_pt", 1);
    outputTree.SetBranchStatus("mT2", 1);
    outputTree.SetBranchStatus("dphill", 1);
    outputTree.SetBranchStatus("dphillmet", 1);
    outputTree.SetBranchStatus("mll", 1);
    outputTree.SetBranchStatus("mtw1", 1);
    outputTree.SetBranchStatus("mtw2", 1);
    outputTree.SetBranchStatus("mth", 1);
    outputTree.SetBranchStatus("PV_npvsGood", 1);
    outputTree.SetBranchStatus("ptll", 1);

    #Additional variables needed for latino
    outputTree.SetBranchStatus("Gen_ZGstar_mass", 1);
    outputTree.SetBranchStatus("LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW", 1);
    outputTree.SetBranchStatus("fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW*", 1);
    outputTree.SetBranchStatus("GenPart_pdgId", 1);
    outputTree.SetBranchStatus("GenPart_statusFlags", 1);
    outputTree.SetBranchStatus("topGenPt", 1);
    outputTree.SetBranchStatus("antitopGenPt", 1);
    outputTree.SetBranchStatus("Jet_btagSF_shape_*", 1);
    outputTree.SetBranchStatus("SFweight2l", 1);
    outputTree.SetBranchStatus("LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW", 1);
    outputTree.SetBranchStatus("LepWPCut", 1);
    outputTree.SetBranchStatus("btagSF", 1);
    outputTree.SetBranchStatus("SFweight*", 1);
    outputTree.SetBranchStatus("TriggerEffWeight_2l*", 1);
    outputTree.SetBranchStatus("baseW", 1);
    outputTree.SetBranchStatus("puWeight*", 1);
    outputTree.SetBranchStatus("LHEScaleWeight", 1);
    outputTree.SetBranchStatus("nllW", 1);
    outputTree.SetBranchStatus("Trigger_*", 1);
    outputTree.SetBranchStatus("XSWeight", 1);
    outputTree.SetBranchStatus("METFilter_*", 1);
    outputTree.SetBranchStatus("gen_ptll", 1);
    outputTree.SetBranchStatus("PhotonGen_isPrompt", 1);
    outputTree.SetBranchStatus("PhotonGen_pt", 1);
    outputTree.SetBranchStatus("PhotonGen_eta", 1);

    #New variables
    nbJet = array("i", [0])
    outputTree.Branch("nbJet", nbJet, "nbJet/I")
    bJetsIdx = array("i", 10*[0])
    outputTree.Branch("bJetsIdx", bJetsIdx, "bJetsIdx[nbJet]/F")

    dark_pt = array("f", [0.])
    outputTree.Branch("dark_pt", dark_pt, "dark_pt/F")
    overlapping_factor = array("f", [0.])
    outputTree.Branch("overlapping_factor", overlapping_factor, "overlapping_factor/F")

    nEvents = inputFile.Events.GetEntries()
    recoAttempts = 0
    recoWorked = 0

    for index, ev in enumerate(inputFile.Events):
        if index % 100 == 0: #Update the loading bar every 100 events
            updateProgress(round(index/float(nEvents), 2))
    
        #Skimming and preselection
        if ev.nLepton < 2:
                continue
        if ev.Lepton_pt[0] < 25. or ev.Lepton_pt[1] < 20.:
            continue
        if ev.Lepton_pdgId[0]*ev.Lepton_pdgId[1] >= 0:
            continue

        if ev.mll < 20.:
            continue

        if ev.nCleanJet < 2:
            continue

        #if index > 1000: #For testing only
        #    continue

        #Creation of new variables
        #bjets collection
        jetIndexes = []
        bJetIndexes = []
        for j in range(ev.nCleanJet):
            jetIndexes.append(j)
            if ev.Jet_btagDeepB[ev.CleanJet_jetIdx[j]] > 0.2217: #Loose WP for now
                bJetIndexes.append(j)

        jetsIdx = jetIndexes
        bJetsIdx = bJetIndexes
        nbJet[0] = len(bJetIndexes)

        #===================================================
        #Ttbar reconstruction
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
        if len(bJetIndexes) == 0:
            continue #We don't consider events having less than 1 bjet
        elif len(bJetIndexes) > 1:
            listOfBJetsCandidates = bJetIndexes
        else: #If we have exactly one bjet, then we keep it as the first element of listOfBJetsCandidates.append while the rest of the list will be made out of usual jets for which we will try to apply the ttbar reconstruction, to try and recover some efficiency of the b-tagging
            listOfBJetsCandidates = bJetIndexes + jetIndexes

        #We have different combinations to perform the reconstruction: we consider the association of the bjets with the two leptons, and we consider all the different bjets candidates
        successfullCombinations = [] #List used to keep the lepton/b-jet indexes for which the reconstruction is working and all the new ttbar inv mass

        Tlep1.SetPtEtaPhiM(ev.Lepton_pt[0], ev.Lepton_eta[0], ev.Lepton_phi[0], 0.000511 if (abs(ev.Lepton_pdgId[0]) == 11) else 0.106)
        Tlep2.SetPtEtaPhiM(ev.Lepton_pt[1], ev.Lepton_eta[1], ev.Lepton_phi[1], 0.000511 if (abs(ev.Lepton_pdgId[1]) == 11) else 0.106)
                        
        for i, jet in enumerate(listOfBJetsCandidates):
            if i == 0:
                Tb1.SetPtEtaPhiM(ev.Jet_pt[jet], ev.Jet_eta[jet], ev.Jet_phi[jet], ev.Jet_mass[jet]) #By construction, we know that the first element of listOfBJetsCandidates is a bjet
            else:
                Tb2.SetPtEtaPhiM(ev.Jet_pt[jet], ev.Jet_eta[jet], ev.Jet_phi[jet], ev.Jet_mass[jet])
                Tnu1.SetPtEtaPhiM(-99.0, -99.0, -99.0, -99.0) #Not needed for the ttbar reconstruction and not available, we can pass default values
                Tnu2.SetPtEtaPhiM(-99.0, -99.0, -99.0, -99.0)
                TMET.SetPtEtaPhiM(ev.PuppiMET_pt, -99.0, ev.PuppiMET_phi, -99.0)

                mW1 = 80.38 #Mass of the W
                mW2 = 80.38
                mt1 = 173.0 #Mass of the top
                mt2 = 173.0

                if verbose:
                    print("Tb1: " + str(Tb1.Print()))
                    print("Tb2: " + str(Tb2.Print()))
                    print("Lep1: " + str(Tlep1.Print()))
                    print("Lep2: " + str(Tlep2.Print()))
                    print("MET: " + str(TMET.Print()))
                
                try:
                    nuSol=ttbar.solveNeutrino(Tb1, Tb2, Tlep1, Tlep2, Tnu1, Tnu2, TMET, mW1, mW2, mt1, mt2)
                    successfullCombinations.append([[0, listOfBJetsCandidates[0], 1, jet], (Tnu1+Tlep1+Tb1).M() + (Tnu2+Tlep2+Tb2).M(), nuSol]) 
                except :
                    if verbose: 
                        print('There is no solution for the ttbar reconstruction for event number '+ str(index))
                    
                #Now we do the same by switching the two leptons since we do not know which lepton corresponds to which b-jet
                try:
                    nuSol=ttbar.solveNeutrino(Tb1, Tb2, Tlep2, Tlep1, Tnu1, Tnu2, TMET, mW1, mW2, mt1, mt2)
                    successfullCombinations.append([[0, jet, 1, listOfBJetsCandidates[0]], (Tnu1+Tlep1+Tb1).M() + (Tnu2+Tlep2+Tb2).M(), nuSol])             
                except :
                    if verbose:
                        print('There is no solution for the ttbar reconstruction for event number '+ str(index))
        
        recoAttempts = recoAttempts + 1
        if verbose: 
            print 'Number of solutions', len(successfullCombinations) 

        if len(successfullCombinations) == 0:
            #The ttbar reco did not work so we fill the ttbar reco with with default values
            dark_pt[0] = -99.0
            overlapping_factor[0] = -99.0
        else:
            recoWorked = recoWorked + 1 #Count the number of times the reco worked

            #Keep the combination having the lowest ttbar invariant mass
            indexLowestInvMass = -1
            lowestInvMass = 100000
            for i, combination in enumerate(successfullCombinations):
                invMass = combination[1]
                if invMass < lowestInvMass:
                    indexLowestInvMass = i
                    lowestInvMass = invMass

            #Compute the dark pt and all the needed variables from this particular combination
            bestNuSol = successfullCombinations[indexLowestInvMass][2]
            overlapping_factor[0] = bestNuSol.overlapingFactor(bestNuSol.N,bestNuSol.n_)
            if bestNuSol.overlapingFactor(bestNuSol.N,bestNuSol.n_) < 0.2: #0.2 to be tweaked?
                dark_pt[0] = bestNuSol.darkPt('DarkPt')
            else:
                dark_pt[0] = -99.0

        outputTree.Fill()

    outputTree.Write()
    inputFile.Close()
    outputFile.Close()

if __name__ == "__main__":
    # =========================================== 
    # Argument parser                            
    # ===========================================
    
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-f', '--filename', action='store', type=str, dest='filename', default="")
    parser.add_option('-d', '--inputDir', action='store', type=str, dest='inputDir', default="")
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    filename = opts.filename
    inputDir = opts.inputDir
    verbose = opts.verbose
    createTree(inputDir, filename)
    
