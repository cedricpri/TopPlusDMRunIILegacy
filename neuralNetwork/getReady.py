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
    try:
        os.stat(outputDirectory)
    except:
        os.mkdir(outputDirectory)
    #os.chdir(outputDirectory)

    outputFile = TFile.Open(outputDirectory + filename[:-5] + "_dnn.root", "recreate")
    outputTree = TTree("Events", "New events tree")

    #Set the variables we want to keep
    #Leptons
    Lepton_pt = array("f", [0.])
    outputTree.Branch("Lepton_pt", Lepton_pt, "Lepton_pt/F")
    Lepton_eta = array("f", [0.])
    outputTree.Branch("Lepton_eta", Lepton_eta, "Lepton_eta/F")
    Lepton_phi = array("f", [0.])
    outputTree.Branch("Lepton_phi", Lepton_phi, "Lepton_phi/F")
    Lepton_pdgId = array("f", [0.])
    outputTree.Branch("Lepton_pdgId", Lepton_pdgId, "Lepton_pdgId/F")
    Lepton_promptgenmatched = array("f", [0.])
    outputTree.Branch("Lepton_promptgenmatched", Lepton_promptgenmatched, "Lepton_promptgenmatched/F")

    #Jets
    CleanJet_pt = array("f", [0.])
    outputTree.Branch("CleanJet_pt", CleanJet_pt, "CleanJet_pt/F")
    CleanJet_eta = array("f", [0.])
    outputTree.Branch("CleanJet_eta", CleanJet_eta, "CleanJet_eta/F")
    CleanJet_phi = array("f", [0.])
    outputTree.Branch("CleanJet_phi", CleanJet_phi, "CleanJet_phi/F")
    CleanJet_jetIdx = array("f", [0.])
    outputTree.Branch("CleanJet_jetIdx", CleanJet_jetIdx, "CleanJet_jetIdx/F")
    njet = array("i", [0])
    outputTree.Branch("njet", njet, "njet/I")

    CleanbJet_pt = array("f", [0.])
    outputTree.Branch("CleanbJet_pt", CleanbJet_pt, "CleanbJet_pt/F")
    CleanbJet_eta = array("f", [0.])
    outputTree.Branch("CleanbJet_eta", CleanbJet_eta, "CleanbJet_eta/F")
    CleanbJet_phi = array("f", [0.])
    outputTree.Branch("CleanbJet_phi", CleanbJet_phi, "CleanbJet_phi/F")
    Jet_btagDeepB = array("f", [0.])
    outputTree.Branch("Jet_btagDeepB", Jet_btagDeepB, "Jet_btagDeepB/F")
    Jet_btagSF_shape = array("f", [0.])
    outputTree.Branch("Jet_btagSF_shape", Jet_btagSF_shape, "Jet_btagSF_shape/F")
    nbjet = array("i", [0])
    outputTree.Branch("nbjet", nbjet, "nbjet/I")

    #Additional variables for the dnn
    PuppiMET_pt    = array("f", [0.])
    outputTree.Branch("PuppiMET_pt", PuppiMET_pt, "PuppiMET_pt/F")
    PuppiMET_phi   = array("f", [0.])
    outputTree.Branch("PuppiMET_phi", PuppiMET_phi, "PuppiMET_phi/F")
    PuppiMET_sumEt = array("f", [0.])
    outputTree.Branch("PuppiMET_sumEt", PuppiMET_sumEt, "PuppiMET_sumEt/F")
    MET_pt         = array("f", [0.])
    outputTree.Branch("MET_pt", MET_pt, "MET_pt/F")
    TkMET_pt       = array("f", [0.])
    outputTree.Branch("TkMET_pt", TkMET_pt, "TkMET_pt/F")
    mT2            = array("f", [0.])
    outputTree.Branch("mT2", mT2, "mT2/F")
    dphill         = array("f", [0.])
    outputTree.Branch("dphill", dphill, "dphill/F")
    dphillmet      = array("f", [0.])
    outputTree.Branch("dphillmet", dphillmet, "dphillmet/F")
    mll            = array("f", [0.])
    outputTree.Branch("mll", mll, "mll/F")
    mtw1           = array("f", [0.])
    outputTree.Branch("mtw1", mtw1, "mtw1/F")
    mtw2           = array("f", [0.])
    outputTree.Branch("mtw2", mtw2, "mtw2/F")
    mth            = array("f", [0.])
    outputTree.Branch("mth", mth, "mth/F")
    nvtx            = array("f", [0.])
    outputTree.Branch("nvtx", nvtx, "nvtx/F")
    ptll            = array("f", [0.])
    outputTree.Branch("ptll", ptll, "ptll/F")

    #Our own discriminating variables
    dark_pt = array("f", [0.])
    outputTree.Branch("dark_pt", dark_pt, "dark_pt/F")
    overlapping_factor = array("f", [0.])
    outputTree.Branch("overlapping_factor", overlapping_factor, "overlapping_factor/F")

    #Additional latino variables needed for plotting and datacards
    Gen_ZGstar_mass = array("f", [0.])
    outputTree.Branch("Gen_ZGstar_mass", Gen_ZGstar_mass, "Gen_ZGstar_mass/F")
    LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW = array("f", [0.])
    outputTree.Branch("LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW", LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW, "LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW/F")
    fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW = array("f", [0.])
    outputTree.Branch("fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW", fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW, "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW/F")
    fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_EleUp = array("f", [0.])
    outputTree.Branch("fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_EleUp", fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_EleUp, "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_EleUp/F")
    fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_EleDown = array("f", [0.])
    outputTree.Branch("fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_EleDown", fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_EleDown, "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_EleDown/F")
    fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_MuUp = array("f", [0.])
    outputTree.Branch("fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_MuUp", fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_MuUp, "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_MuUp/F")
    fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_MuDown = array("f", [0.])
    outputTree.Branch("fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_MuDown", fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_MuDown, "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW_MuDown/F")
    fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statEleUp = array("f", [0.])
    outputTree.Branch("fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statEleUp", fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statEleUp, "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statEleUp/F")
    fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statEleDown = array("f", [0.])
    outputTree.Branch("fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statEleDown", fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statEleDown, "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statEleDown/F")
    fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statMuUp = array("f", [0.])
    outputTree.Branch("fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statMuUp", fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statMuUp, "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statMuUp/F")
    fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statMuDown = array("f", [0.])
    outputTree.Branch("fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statMuDown", fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statMuDown, "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW__statMuDown/F")

    GenPart_pdgId = array("f", [0.])
    outputTree.Branch("GenPart_pdgId", GenPart_pdgId, "GenPart_pdgId/F")
    GenPart_statusFlags = array("f", [0.])
    outputTree.Branch("GenPart_statusFlags", GenPart_statusFlags, "GenPart_statusFlags/F")
    topGenPt = array("f", [0.])
    outputTree.Branch("topGenPt", topGenPt, "topGenPt/F")
    antitopGenPt= array("f", [0.])
    outputTree.Branch("antitopGenPt", antitopGenPt, "antitopGenPt/F")

    btagSF_shape_up_jes = array("f", [0.])
    outputTree.Branch("btagSF_shape_up_jes", btagSF_shape_up_jes, "btagSF_shape_up_jes/F")
    btagSF_shape_up_lf = array("f", [0.])
    outputTree.Branch("btagSF_shape_up_lf", btagSF_shape_up_lf, "btagSF_shape_up_lf/F")
    btagSF_shape_up_hf = array("f", [0.])
    outputTree.Branch("btagSF_shape_up_hf", btagSF_shape_up_hf, "btagSF_shape_up_hf/F")
    btagSF_shape_up_lfstats1 = array("f", [0.])
    outputTree.Branch("btagSF_shape_up_lfstats1", btagSF_shape_up_lfstats1, "btagSF_shape_up_lfstats1/F")
    btagSF_shape_up_lfstats2 = array("f", [0.])
    outputTree.Branch("btagSF_shape_up_lfstats2", btagSF_shape_up_lfstats2, "btagSF_shape_up_lfstats2/F")
    btagSF_shape_up_hfstats1 = array("f", [0.])
    outputTree.Branch("btagSF_shape_up_hfstats1", btagSF_shape_up_hfstats1, "btagSF_shape_up_hfstats1/F")
    btagSF_shape_up_hfstats2 = array("f", [0.])
    outputTree.Branch("btagSF_shape_up_hfstats2", btagSF_shape_up_hfstats2, "btagSF_shape_up_hfstats2/F")
    btagSF_shape_up_cferr1 = array("f", [0.])
    outputTree.Branch("btagSF_shape_up_cferr1", btagSF_shape_up_cferr1, "btagSF_shape_up_cferr1/F")
    btagSF_shape_up_cferr2 = array("f", [0.])
    outputTree.Branch("btagSF_shape_up_cferr2", btagSF_shape_up_cferr2, "btagSF_shape_up_cferr2/F")
    btagSF_shape_down_jes = array("f", [0.])
    outputTree.Branch("btagSF_shape_down_jes", btagSF_shape_down_jes, "btagSF_shape_down_jes/F")
    btagSF_shape_down_lf = array("f", [0.])
    outputTree.Branch("btagSF_shape_down_lf", btagSF_shape_down_lf, "btagSF_shape_down_lf/F")
    btagSF_shape_down_hf = array("f", [0.])
    outputTree.Branch("btagSF_shape_down_hf", btagSF_shape_down_hf, "btagSF_shape_down_hf/F")
    btagSF_shape_down_lfstats1 = array("f", [0.])
    outputTree.Branch("btagSF_shape_down_lfstats1", btagSF_shape_down_lfstats1, "btagSF_shape_down_lfstats1/F")
    btagSF_shape_down_lfstats2 = array("f", [0.])
    outputTree.Branch("btagSF_shape_down_lfstats2", btagSF_shape_down_lfstats2, "btagSF_shape_down_lfstats2/F")
    btagSF_shape_down_hfstats1 = array("f", [0.])
    outputTree.Branch("btagSF_shape_down_hfstats1", btagSF_shape_down_hfstats1, "btagSF_shape_down_hfstats1/F")
    btagSF_shape_down_hfstats2 = array("f", [0.])
    outputTree.Branch("btagSF_shape_down_hfstats2", btagSF_shape_down_hfstats2, "btagSF_shape_down_hfstats2/F")
    btagSF_shape_down_cferr1 = array("f", [0.])
    outputTree.Branch("btagSF_shape_down_cferr1", btagSF_shape_down_cferr1, "btagSF_shape_down_cferr1/F")
    btagSF_shape_down_cferr2 = array("f", [0.])
    outputTree.Branch("btagSF_shape_down_cferr2", btagSF_shape_down_cferr2, "btagSF_shape_down_cferr2/F")

    SFweight2l = array("f", [0.])
    outputTree.Branch("SFweight2l", SFweight2l, "SFweight2l/F")
    LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW = array("f", [0.])
    outputTree.Branch("LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW", LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW, "LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW/F")
    LepWPCut = array("f", [0.])
    outputTree.Branch("LepWPCut", LepWPCut, "LepWPCut/F")
    btagSF = array("f", [0.])
    outputTree.Branch("btagSF", btagSF, "btagSF/F")
    SFweightEleUp = array("f", [0.])
    outputTree.Branch("SFweightEleUp", SFweightEleUp, "SFweightEleUp/F")
    SFweightEleDown = array("f", [0.])
    outputTree.Branch("SFweightEleDown", SFweightEleDown, "SFweightEleDown/F")
    SFweightMuUp = array("f", [0.])
    outputTree.Branch("SFweightMuUp", SFweightMuUp, "SFweightMuUp/F")
    SFweightMuDown = array("f", [0.])
    outputTree.Branch("SFweightMuDown", SFweightMuDown, "SFweightMuDown/F")

    TriggerEffWeight_2l = array("f", [0.])
    outputTree.Branch("TriggerEffWeight_2l", TriggerEffWeight_2l, "TriggerEffWeight_2l/F")
    TriggerEffWeight_2l_u = array("f", [0.])
    outputTree.Branch("TriggerEffWeight_2l_u", TriggerEffWeight_2l_u, "TriggerEffWeight_2l_u/F")
    TriggerEffWeight_2l_d = array("f", [0.])
    outputTree.Branch("TriggerEffWeight_2l_d", TriggerEffWeight_2l_d, "TriggerEffWeight_2l_d/F")
    baseW = array("f", [0.])
    outputTree.Branch("baseW", baseW, "baseW/F")
    puWeight = array("f", [0.])
    outputTree.Branch("puWeight", puWeight, "puWeight/F")
    puWeightUp = array("f", [0.])
    outputTree.Branch("puWeightUp", puWeightUp, "puWeightUp/F")
    puWeightDown = array("f", [0.])
    outputTree.Branch("puWeightDown", puWeightDown, "puWeightDown/F")
    nLHEScaleWeight = array("i", [0])
    outputTree.Branch("nLHEScaleWeight", nLHEScaleWeight, "nLHEScaleWeight/I")
    LHEScaleWeight = array("f", [0.])
    outputTree.Branch("LHEScaleWeight", LHEScaleWeight, "LHEScaleWeight/F")
    nllW = array("f", [0.])
    outputTree.Branch("nllW", nllW, "nllW/F")
    luminosityBlock = array("i", [0])
    outputTree.Branch("luminosityBlock", luminosityBlock, "luminosityBlock/I")

    Trigger_ElMu = array("i", [0])
    outputTree.Branch("Trigger_ElMu", Trigger_ElMu, "Trigger_ElMu/I")
    Trigger_dblMu = array("i", [0])
    outputTree.Branch("Trigger_dblMu", Trigger_dblMu, "Trigger_dblMu/I")
    Trigger_sngMu = array("i", [0])
    outputTree.Branch("Trigger_sngMu", Trigger_sngMu, "Trigger_sngMu/I")
    Trigger_sngEl = array("i", [0])
    outputTree.Branch("Trigger_sngEl", Trigger_sngEl, "Trigger_sngEl/I")
    Trigger_dblEl = array("i", [0])
    outputTree.Branch("Trigger_dblEl", Trigger_dblEl, "Trigger_dblEl/I")
    XSWeight = array("f", [0.])
    outputTree.Branch("XSWeight", XSWeight, "XSWeight/F")
    METFilter_MC = array("f", [0.])
    outputTree.Branch("METFilter_MC", METFilter_MC, "METFilter_MC/F")
    METFilter_DATA = array("f", [0.])
    outputTree.Branch("METFilter_DATA", METFilter_DATA, "METFilter_DATA/F")
    gen_ptll = array("f", [0.])
    outputTree.Branch("gen_ptll", gen_ptll, "gen_ptll/F")
    PhotonGen_isPrompt = array("f", [0.])
    outputTree.Branch("PhotonGen_isPrompt", PhotonGen_isPrompt, "PhotonGen_isPrompt/F")
    PhotonGen_pt = array("f", [0.])
    outputTree.Branch("PhotonGen_pt", PhotonGen_pt, "PhotonGen_pt/F")
    PhotonGen_eta = array("f", [0.])
    outputTree.Branch("PhotonGen_eta", PhotonGen_eta, "PhotonGen_eta/F")

    #Let's get started
    nEvents = inputFile.Events.GetEntries()
    recoAttempts = 0
    recoWorked = 0

    print("Let's start with the loop")
    
    for index, ev in enumerate(inputFile.Events):
        if index % 100 == 0: #Update the loading bar every 100 events                                                                                              
            updateProgress(round(index/float(nEvents), 2))

        #Skimming and preselection
        if ev.Lepton_pdgId[0]*ev.Lepton_pdgId[1] >= 0:
            continue
        if ev.Lepton_pt[0] < 25. or ev.Lepton_pt[1] < 20.:
            continue
        if mll < 20.:
            continue
        if ev.njet < 2:
            continue
        if index > 100:  #TODO: to be removed
            break

        #Leptons
        Lepton_pt = []
        for l, lepton in enumerate(ev.Lepton_pt):
            Lepton_pt.append(ev.Lepton_pt[l])
            Lepton_eta.append(ev.Lepton_eta[l])
            Lepton_phi.append(ev.Lepton_phi[l])
            Lepton_pdgId.append(ev.Lepton_pdgId[l])
            Lepton_promptgenmatched.append(ev.Lepton_promptgenmatched[l])
        print(Lepton_pt)
        
        #Jets
        for j, jet in enumerate(ev.CleanJet_jetIdx):
            CleanJet_pt.append(ev.CleanJet_pt[j])
            CleanJet_eta.append(ev.CleanJet_eta[j])
            CleanJet_eta.append(ev.CleanJet_eta[j])
            CleanJet_jetIdx.append(ev.CleanJet_jetIdx[j])
            Jet_btagDeepB.append(ev.Jet_btagDeepB[j])
            Jet_btagSF_shape.append(ev.Jet_btagSF_shape[j])
            njet[0] = njet[0] + 1

            #B-jets
            if ev.Jet_btagDeepB[j] > 0.2217: #Loose WP for now
                CleanbJet_pt.append(ev.CleanJet_pt[j])
                CleanbJet_eta.append(ev.CleanJet_eta[j])
                CleanbJet_phi.append(ev.CleanJet_phi[j])
                nbjet[0] = nbjet[0] + 1

        PuppiMET_pt[0] = ev.PuppiMET_pt;
        PuppiMET_phi[0] = ev.PuppiMET_phi;
        #PuppiMET_sumET[0] = ev.PuppiMET_sumET;

        """
        #Additional variables
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

        #We have different combinations to perform the reconstruction: we consider the association of the bjets with the two leptons, and we consider all the different bjets candidates
	successfullCombinations = [] #List used to keep the lepton/b-jet indexes for which the reconstruction is working and all the new ttbar inv mass

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
                except LinAlgError :
                    if verbose: 
                        print('There is no solution for the ttbar reconstruction for event number '+ str(index))
                    
                #Now we do the same by switching the two leptons since we do not know which lepton corresponds to which b-jet
                try:
                    nuSol=ttbar.solveNeutrino(Tb1, Tb2, Tlep2, Tlep1, Tnu1, Tnu2, TMET, mW1, mW2, mt1, mt2)
                    successfullCombinations.append([[0, jet, 1, listOfBJetsCandidates[0]], (Tnu1+Tlep1+Tb1).M() + (Tnu2+Tlep2+Tb2).M(), nuSol])             
                except LinAlgError :
                    if verbose:
                        print('There is no solution for the ttbar reconstruction for event number '+ str(index))
        
        recoAttempts = recoAttempts + 1
        if verbose: 
            print 'Number of solutions', len(successfullCombinations) 

        if len(successfullCombinations) == 0:
            #The ttbar reco did not work so we fill the ttbar reco with with default values
            ttbarLowestInvMass[0] = -99.0
            dark_pt[0] = -99.0
            overlappingFactor[0] = -99.0
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

            ttbarLowestInvMass[0] = lowestInvMass
            overlappingFactor[0] = bestNuSol.overlapingFactor(bestNuSol.N,bestNuSol.n_)
            if bestNuSol.overlapingFactor(bestNuSol.N,bestNuSol.n_) < 0.2: #0.2 to be tweaked?
                dark_pt[0] = bestNuSol.darkPt('DarkPt')
            else:
                dark_pt[0] = -99.0
        """
        outputTree.Fill()

    #print 'The ttbar reconstruction worked for ' + str(round((recoWorked/float(recoAttempts))*100, 2)) + '% of the events considered'
    
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
    
