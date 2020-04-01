#Code used to read the input files for dnn.py and create additional variables we use for the discrimination
import ROOT as r
from array import array
import optparse
import os, sys, fnmatch

#Class for the ttbar reconstruction
from eventKinematic import EventKinematic

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
    #===================================================
    #Global setup
    #===================================================

    print("\n\n --> Now considering file... " + filename)

    #First, let's open the mlb histogram we are going to need
    mlbFile = r.TFile("mlb.root", "r")
    mlbHist = mlbFile.Get("mlb")

    inputFile = r.TFile.Open(inputDir+filename, "r")
    inputTree = inputFile.Get("Events")

    #Create a directory to keep the files if it does not already exist
    outputDirectory = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/"
    outputDirectoryProduction = "/".join(inputDir.split('/')[-3:-1])+"/"
    outputDirectory = outputDirectory + outputDirectoryProduction #Add a final name to distinguish between 2016, 2017 and 2018 files
    try:
        os.stat(outputDirectory)
    except:
        os.makedirs(outputDirectory)

    outputFile = r.TFile.Open(outputDirectory + filename, "recreate")
    outputTree = inputTree.CloneTree(0)

    #===================================================
    #Select the branches we want to keep
    #===================================================

    outputTree.SetBranchStatus("*", 0);

    #Leptons
    outputTree.SetBranchStatus("nLepton", 1);
    outputTree.SetBranchStatus("Lepton_pt", 1);
    outputTree.SetBranchStatus("Lepton_eta", 1);
    outputTree.SetBranchStatus("Lepton_phi", 1);
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
    outputTree.SetBranchStatus("MET_significance", 1);
    outputTree.SetBranchStatus("mT2", 1); #mT2 computed by Latino
    outputTree.SetBranchStatus("dphill", 1);
    outputTree.SetBranchStatus("dphillmet", 1);
    outputTree.SetBranchStatus("mll", 1);
    outputTree.SetBranchStatus("mtw1", 1);
    outputTree.SetBranchStatus("mtw2", 1);
    outputTree.SetBranchStatus("mth", 1);
    outputTree.SetBranchStatus("PV_npvsGood", 1);
    outputTree.SetBranchStatus("ptll", 1);

    #Additional variables needed for latino
    outputTree.SetBranchStatus("event", 1);
    outputTree.SetBranchStatus("Gen_ZGstar_mass", 1);
    outputTree.SetBranchStatus("LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW", 1);
    outputTree.SetBranchStatus("fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW*", 1);
    outputTree.SetBranchStatus("GenPart_pdgId", 1);
    outputTree.SetBranchStatus("GenPart_statusFlags", 1);
    outputTree.SetBranchStatus("topGenPt", 1);
    outputTree.SetBranchStatus("antitopGenPt", 1);
    outputTree.SetBranchStatus("Jet_btagSF_shape_*", 1);
    outputTree.SetBranchStatus("SFweight2l", 1);
    outputTree.SetBranchStatus("LepSF2l__ele_mvaFall17V1Iso_WP90*", 1);
    outputTree.SetBranchStatus("LepSF2l__mu_cut_Tight_HWWW*", 1);
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
    outputTree.Branch("bJetsIdx", bJetsIdx, "bJetsIdx[nbJet]/I")

    mt2ll = array("f", [0.])
    outputTree.Branch("mt2ll", mt2ll, "mt2ll/F")
    mt2bl = array("f", [0.])
    outputTree.Branch("mt2bl", mt2bl, "mt2bl/F")

    reco_weight = array("f", [0.])
    outputTree.Branch("reco_weight", reco_weight, "reco_weight/F")
    dark_pt = array("f", [0.])
    outputTree.Branch("dark_pt", dark_pt, "dark_pt/F")
    overlapping_factor = array("f", [0.])
    outputTree.Branch("overlapping_factor", overlapping_factor, "overlapping_factor/F")

    thetall = array("f", [0.])
    outputTree.Branch("thetall", thetall, "thetall/F")
    thetal1b1 = array("f", [0.])
    outputTree.Branch("thetal1b1", thetal1b1, "thetal1b1/F")
    thetal2b2 = array("f", [0.])
    outputTree.Branch("thetal2b2", thetal2b2, "thetal2b2/F")
    cosphill = array("f", [0.])
    outputTree.Branch("cosphill", cosphill, "cosphill/F")

    nEvents = inputFile.Events.GetEntries()
    nAttempts, nWorked = 0, 0

    #Compile the code for the mt2 calculation
    r.gROOT.ProcessLine('.L '+os.getcwd()+'/mt2Calculation/lester_mt2_bisect.h+')

    for index, ev in enumerate(inputFile.Events):
        if index % 100 == 0: #Update the loading bar every 100 events
            updateProgress(round(index/float(nEvents), 2))
    
        #===================================================
        #Skimming and preselection
        #===================================================

        try: #The third lepton is not always defined
            pt3 = ev.Lepton_pt[2]
        except:
            pt3 = 0.

        if ev.Lepton_pt[0] < 25. or ev.Lepton_pt[1] < 20. or pt3 > 10.: #Exactly two leptons
            continue
        if ev.Lepton_pdgId[0]*ev.Lepton_pdgId[1] >= 0: #Opposite sign leptons only
            continue

        if ev.mll < 20.:
            continue

        #The jet does not always exist, so let's check if it does exist
        try:
            jetpt1 = ev.CleanJet_pt[0]
        except:
            jetpt1 = 0.

        try:
            jetpt2 = ev.CleanJet_pt[1]
        except:
            jetpt2 = 0.

        if jetpt1 < 30. or jetpt2 < 30.: #At least two jets with pt > 30 GeV
            continue
        
        #Additional cut removing events having less than one b-jet performed later, once the b-jets have been computed

        #===================================================
        #b-jets collection creation
        #===================================================
        jetIndexes = []
        bJetIndexes = [] #Instead of keeping all the b-jets in a new collection, let's just keep in the trees their indexes to save memory

        ibjet = 0
        for j, jet in enumerate(ev.CleanJet_pt): #TOCHECK: For now, we only consider b-jets from the clean jets collection
            jetIndexes.append(j)
            if ev.Jet_btagDeepB[ev.CleanJet_jetIdx[j]] > 0.2217: #TOCHECK: Loose WP for now
                bJetIndexes.append(j) #Variable to use for the ttbar reco
                bJetsIdx[ibjet] = j #Variable to keep in the tree
                ibjet = ibjet + 1

        nbJet[0] = len(bJetIndexes)

        if len(bJetIndexes) == 0: #We don't consider events having less than 1 b-jet
            continue 

        #===================================================
        #Kinematics definition
        #===================================================

        Tlep1 = r.TLorentzVector()
        Tlep2 = r.TLorentzVector()
        Tb1 = r.TLorentzVector()
        Tb2 = r.TLorentzVector()
        Tnu1  = r.TLorentzVector()
        Tnu2  = r.TLorentzVector()
        TMET  = r.TLorentzVector()

        Tlep1.SetPtEtaPhiM(ev.Lepton_pt[0], ev.Lepton_eta[0], ev.Lepton_phi[0], 0.000511 if (abs(ev.Lepton_pdgId[0]) == 11) else 0.106)
        Tlep2.SetPtEtaPhiM(ev.Lepton_pt[1], ev.Lepton_eta[1], ev.Lepton_phi[1], 0.000511 if (abs(ev.Lepton_pdgId[1]) == 11) else 0.106)
        #Tnu1.SetPtEtaPhiM(-99.0, -99.0, -99.0, -99.0) #Not needed for the ttbar reconstruction and not available, we can pass default values
        #Tnu2.SetPtEtaPhiM(-99.0, -99.0, -99.0, -99.0)
        TMET.SetPtEtaPhiM(ev.MET_pt, 0.0, ev.MET_phi, 0.0) #TOCHECK: use the MET or PUPPIMET?

        #===================================================
        #Ttbar reconstruction
        #===================================================

        bJetCandidateIndexes = []
        if len(bJetIndexes) > 1:
            bJetCandidateIndexes = bJetIndexes
        else: #If we have exactly one -bjet, then we keep it as the first element while the rest of the list will be made out of usual jets for which we will try to apply the ttbar reconstruction, to try and recover some efficiency of the b-tagging
            bJetCandidateIndexes = bJetIndexes + jetIndexes

        #Remove the duplicates to avoid counting the same jet twice
        bJetCandidateIndexes = list(set(bJetCandidateIndexes))

        maxWeight = -99.0 #Criteria to know which b-jet/lepton combination to keep
        bestReconstructedKinematic = None
        inverseOrder = False #Keep track of the b-jet/lepton combination used

        for i, jet in enumerate(bJetCandidateIndexes):
            if i == 0:
                #By construction, we know that the first element of bJetCandidateIndexes is a b-jet
                Tb1.SetPtEtaPhiM(ev.CleanJet_pt[jet], ev.CleanJet_eta[jet], ev.CleanJet_phi[jet], ev.Jet_mass[ev.CleanJet_jetIdx[jet]])
            else:
                Tb2.SetPtEtaPhiM(ev.CleanJet_pt[jet], ev.CleanJet_eta[jet], ev.CleanJet_phi[jet], ev.Jet_mass[ev.CleanJet_jetIdx[jet]])

                eventKinematic1 = EventKinematic(Tlep1, Tlep2, Tb1, Tb2, Tnu1, Tnu2, TMET)
                eventKinematic2 = EventKinematic(Tlep2, Tlep1, Tb1, Tb2, Tnu1, Tnu2, TMET)

                #Perform first of all the reco without smearing
                eventKinematic1.runReco()
                eventKinematic1.findBestSolution(mlbHist)
                if eventKinematic1.weight > maxWeight:
                    bestReconstructedKinematic = eventKinematic1
                    inverseOrder = False
                    maxWeight = eventKinematic1.weight

                eventKinematic2.runReco()
                eventKinematic2.findBestSolution(mlbHist)
                if eventKinematic2.weight > maxWeight:
                    bestReconstructedKinematic = eventKinematic2
                    inverseOrder = True
                    maxWeight = eventKinematic2.weight

                #Run the smearing 100 times
                for i in range(100): 

                    smearedEventKinematic = eventKinematic1.runSmearingOnce(mlbHist)
                    #Keep the solution that has the higher weight
                    if smearedEventKinematic.weight > maxWeight:
                        bestReconstructedKinematic = smearedEventKinematic
                        inverseOrder = False
                        maxWeight = smearedEventKinematic.weight
                        
                    #Do the same by reversing the leptons
                    smearedEventKinematic = eventKinematic2.runSmearingOnce(mlbHist)
                    #Keep the solution that has the higher weight
                    if smearedEventKinematic.weight > maxWeight:
                        bestReconstructedKinematic = smearedEventKinematic
                        inverseOrder = True
                        maxWeight = smearedEventKinematic.weight

        recoWorked = False
        nAttempts = nAttempts + 1 #Count the number of event for which the reco worked
        if bestReconstructedKinematic is not None:
            if bestReconstructedKinematic.weight != -99.0:
                recoWorked = True
                nWorked = nWorked + 1

        if inverseOrder:
            eventKinematic = eventKinematic2
        else: 
            eventKinematic = eventKinematic1

        #===================================================
        #Dark pt and overlapping factor
        #===================================================

        if recoWorked:
            reco_weight[0] = bestReconstructedKinematic.weight
            dark_pt[0] = bestReconstructedKinematic.dark_pt
            overlapping_factor[0] = bestReconstructedKinematic.overlapping_factor
        else:
            reco_weight[0] = -99.0
            dark_pt[0] = -99.0
            overlapping_factor[0] = -99.0

        #===================================================
        #MT2 computation
        #===================================================

        mt2ll[0] = computeMT2(eventKinematic.Tlep1, eventKinematic.Tlep2, eventKinematic.TMET, 0) 
        if recoWorked:
            try:
                mt2bl[0] = computeMT2(eventKinematic.Tlep1 + bestReconstructedKinematic.Tb1, event.Tlep2 + bestReconstructedKinematic.Tb2, eventKinematic.TMET, 0) 
            except:
                mt2bl[0] = -9.0
        else:
            mt2bl[0] = -99.0

        #===================================================
        #Additional variables computation
        #===================================================
        """
        #Variables bases on DESY's AN2016-240-v10

        #cos(theta_i)*cos(theta_j), where (i,j) = (l+l-, l-b, l+bbar)
        thetall[0] = math.cos(2*math.atan(math.exp(-Tlep1.Eta()))) * math.cos(2*math.atan(math.exp(-Tlep2.Eta())))
        if recoWorked:
            thetal1b1[0] = math.cos(2*math.atan(math.exp(-Tlep1.Eta()))) * math.cos(2*math.atan(math.exp(-Tb1Updated.Eta())))
            thetal2b2[0] = math.cos(2*math.atan(math.exp(-Tlep2.Eta()))) * math.cos(2*math.atan(math.exp(-Tb2Updated.Eta())))
        else:
            thetal1b1[0] = -999.0
            thetal2b2[0] = -999.0

        #cos(phi) for the same (i,j) but in the rest frame
        if recoWorked:
            Tmom1 = Tlep1 + Tnu1Updated #TLorentzVector of the W boson associated to the lepton 1 
            Tmom2 = Tlep2 + Tnu2Updated

            boostvector = Tmom1.BoostVector()
            Tlep1RestFrame = Tlep1.Boost(boostvector)
            boostvector = Tmom2.BoostVector()
            Tlep2RestFrame = Tlep2.Boost(boostvector)

            #cosphill[0] = math.cos(Tlep2RestFrame.Phi() - Tlep1RestFrame.Phi())
        else:
            cosphill[0] = -999.0
        """
        outputTree.Fill()

    print '\nThe ttbar reconstruction worked for ' + str(round((nWorked/float(nAttempts))*100, 2)) + '% of the events considered'

    outputFile.cd()
    outputTree.Write()
    inputFile.Close()
    outputFile.Close()
    mlbFile.Close()

def computeMT2(VisibleA, VisibleB, Invisible, MT2Type = 0, MT2Precision = 0) :

    mVisA = abs(VisibleA.M())  # Mass of visible object on side A. Must be >= 0
    mVisB = abs(VisibleB.M())  # Mass of visible object on side B. Must be >= 0

    chiA = 0.  # Hypothesized mass of invisible on side A. Must be >= 0
    chiB = 0.  # Hypothesized mass of invisible on side B. Must be >= 0
  
    if MT2Type== 1 : # This is for mt2 with b jets

        mVisA =  5.
        mVisB =  5.
        chiA  = 80.
        chiB  = 80.
            
    pxA = VisibleA.Px()  # x momentum of visible object on side A
    pyA = VisibleA.Py()  # y momentum of visible object on side A
    
    pxB = VisibleB.Px()  # x momentum of visible object on side B
    pyB = VisibleB.Py()  # y momentum of visible object on side B
        
    pxMiss = Invisible.Px()  # x component of missing transverse momentum
    pyMiss = Invisible.Py()  # y component of missing transverse momentum
        
    # Must be >= 0
    # If = 0 algorithm aims for machine precision
    # If > 0 MT2 computed to supplied absolute precision
    desiredPrecisionOnMt2 = MT2Precision
    
    mT2 = r.asymm_mt2_lester_bisect().get_mT2(mVisA, pxA, pyA,
                                                 mVisB, pxB, pyB,
                                                 pxMiss, pyMiss,
                                                 chiA, chiB,
                                                 desiredPrecisionOnMt2)
    
    return mT2


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
    
