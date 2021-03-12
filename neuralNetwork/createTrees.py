#Code used to read the input files for dnn.py and create additional variables we use for the discrimination
import ROOT as r
from array import array
import optparse
import os, sys, fnmatch, math, time
from copy import deepcopy

#Class for the ttbar reconstruction
from ttbarReco.eventKinematic import EventKinematic

#Smearing parameters
runSmearing = True
runSmearingNumber = 100

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
def createTree(inputDir, outputDir, baseDir, filename, firstEvent, lastEvent, splitNumber, year):
    #===================================================
    #Global setup
    #===================================================

    print("Filename:"+filename)
    start_time = time.time()
    
    #First, let's open the mlb histogram we are going to need
    distFile = r.TFile(baseDir+"distributions.root", "r")
    distributions = {
        "mlb": distFile.Get("mlb"),
        "bw": distFile.Get("bw"),
        "jer": distFile.Get("jer"),
        "ler": distFile.Get("ler"),
        "jphat": distFile.Get("jphat"),
        "lphat": distFile.Get("lphat")
    }

    inputFile = r.TFile.Open(inputDir+filename, "r")

    #Create a directory to keep the files if it does not already exist
    outputDirProduction = "/".join(inputDir.split('/')[-3:-1])+"/"
    outputDir = outputDir + outputDirProduction #Add a final name to distinguish between 2016, 2017 and 2018 files
    try:
        os.stat(outputDir)
    except:
        os.makedirs(outputDir)

    if splitNumber != -1:
        outputFile = r.TFile.Open(outputDir + filename.replace('.root', '') + '_' + str(splitNumber) + ".root", "recreate")
    else:
        outputFile = r.TFile.Open(outputDir + filename, "recreate")

    inputTree = inputFile.Get("Events")
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
    outputTree.SetBranchStatus("Jet_*", 1);
    outputTree.SetBranchStatus("CleanJet_*", 1);

    #Clean jets
    outputTree.SetBranchStatus("nCleanJet", 1);
    outputTree.SetBranchStatus("CleanJet_pt", 1);
    outputTree.SetBranchStatus("CleanJet_eta", 1);
    outputTree.SetBranchStatus("CleanJet_phi", 1);
    outputTree.SetBranchStatus("CleanJet_jetIdx", 1);
    outputTree.SetBranchStatus("nCleanGenJet", 1);

    #Additional discriminating variables
    outputTree.SetBranchStatus("PuppiMET_pt", 1);
    outputTree.SetBranchStatus("PuppiMET_phi", 1);
    outputTree.SetBranchStatus("PuppiMET_sumEt", 1);
    outputTree.SetBranchStatus("MET_pt", 1);
    outputTree.SetBranchStatus("MET_phi", 1);
    outputTree.SetBranchStatus("METFixEE2017_pt", 1);
    outputTree.SetBranchStatus("METFixEE2017_phi", 1);
    outputTree.SetBranchStatus("METFixEE2017_significance", 1);
    outputTree.SetBranchStatus("METFixEE2017_sumEt", 1);
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
    outputTree.SetBranchStatus("LepCut2l*", 1);
    outputTree.SetBranchStatus("fakeW", 1);
    outputTree.SetBranchStatus("fakeW2l*", 1);
    outputTree.SetBranchStatus("GenPart_pt", 1);
    outputTree.SetBranchStatus("GenPart_pdgId", 1);
    outputTree.SetBranchStatus("GenPart_genPartIdxMother", 1);
    outputTree.SetBranchStatus("GenPart_statusFlags", 1);
    outputTree.SetBranchStatus("topGenPt", 1);
    outputTree.SetBranchStatus("antitopGenPt", 1);
    outputTree.SetBranchStatus("nGenPart", 1);
    outputTree.SetBranchStatus("LeptonGen_pt", 1);
    outputTree.SetBranchStatus("LeptonGen_pdgId", 1);
    outputTree.SetBranchStatus("LeptonGen_isPrompt", 1);
    outputTree.SetBranchStatus("Jet_btagSF_*shape_*", 1);
    outputTree.SetBranchStatus("Jet_PUIDSF_loose", 1);
    outputTree.SetBranchStatus("nllw", 1);
    outputTree.SetBranchStatus("LepSF2l*", 1);
    outputTree.SetBranchStatus("LepWPCut", 1);
    outputTree.SetBranchStatus("*btagSF*", 1);
    outputTree.SetBranchStatus("SFweight*", 1);
    outputTree.SetBranchStatus("*PSWeight*", 1);
    outputTree.SetBranchStatus("TriggerEffWeight_2l*", 1);
    outputTree.SetBranchStatus("baseW", 1);
    outputTree.SetBranchStatus("puWeight*", 1);
    outputTree.SetBranchStatus("LHEScaleWeight", 1);
    outputTree.SetBranchStatus("nllW*", 1);
    outputTree.SetBranchStatus("gen_mll", 1);
    outputTree.SetBranchStatus("Trigger_*", 1);
    outputTree.SetBranchStatus("XSWeight", 1);
    outputTree.SetBranchStatus("genWeight", 1);
    outputTree.SetBranchStatus("METFilter_*", 1);
    outputTree.SetBranchStatus("gen_ptll", 1);
    outputTree.SetBranchStatus("PhotonGen_isPrompt", 1);
    outputTree.SetBranchStatus("PhotonGen_pt", 1);
    outputTree.SetBranchStatus("PhotonGen_eta", 1);
    outputTree.SetBranchStatus("LHE_HT", 1);
    outputTree.SetBranchStatus("PrefireWeight", 1);
    outputTree.SetBranchStatus("*Up*", 1);
    outputTree.SetBranchStatus("*Down*", 1);
    outputTree.SetBranchStatus("*Top_pTrw*", 1);

    #New variables
    nbJet = array("i", [0])
    outputTree.Branch("nbJet", nbJet, "nbJet/I")
    bJetsIdx = array("i", 10*[0])
    outputTree.Branch("bJetsIdx", bJetsIdx, "bJetsIdx[nbJet]/I")

    METcorrected_pt = array("f", [0.])
    outputTree.Branch("METcorrected_pt", METcorrected_pt, "METcorrected_pt/F")
    METcorrected_phi = array("f", [0.])
    outputTree.Branch("METcorrected_phi", METcorrected_phi, "METcorrected_phi/F")

    mt2ll = array("f", [0.])
    outputTree.Branch("mt2ll", mt2ll, "mt2ll/F")
    mt2bl = array("f", [0.])
    outputTree.Branch("mt2bl", mt2bl, "mt2bl/F")
    mblt = array("f", [0.])
    outputTree.Branch("mblt", mblt, "mblt/F")

    reco_weight = array("f", [0.])
    outputTree.Branch("reco_weight", reco_weight, "reco_weight/F")
    dark_pt = array("f", [0.])
    outputTree.Branch("dark_pt", dark_pt, "dark_pt/F")
    overlapping_factor = array("f", [0.])
    outputTree.Branch("overlapping_factor", overlapping_factor, "overlapping_factor/F")

    totalET = array("f", [0.])
    outputTree.Branch("totalET", totalET, "totalET/F")
    massT = array("f", [0.]) #New variable by Pablo
    outputTree.Branch("massT", massT, "massT/F")
    costhetall = array("f", [0.])
    outputTree.Branch("costhetall", costhetall, "costhetall/F")
    costhetal1b1 = array("f", [0.])
    outputTree.Branch("costhetal1b1", costhetal1b1, "costhetal1b1/F")
    costhetal2b2 = array("f", [0.])
    outputTree.Branch("costhetal2b2", costhetal2b2, "costhetal2b2/F")
    cosphill = array("f", [0.])
    outputTree.Branch("cosphill", cosphill, "cosphill/F")
    
    r2l = array("f", [0.]) #ATLAS publication
    outputTree.Branch("r2l", r2l, "r2l/F")
    r2l4j = array("f", [0.])
    outputTree.Branch("r2l4j", r2l4j, "r2l4j/F")

    nEvents = inputFile.Events.GetEntries()
    if test:
        nEvents = 500
    if lastEvent != -1:
        nEvents = lastEvent - firstEvent

    nAttempts, nWorked = 0, 0

    #Compile the code for the mt2 calculation
    r.gROOT.ProcessLine('.L '+baseDir+'/met/XYMETCorrection.h+')
    r.gROOT.ProcessLine('.L '+baseDir+'/mt2Calculation/lester_mt2_bisect.h+')
    try:
        r.asymm_mt2_lester_bisect.disableCopyrightMessage()
    except:
        pass

    for index, ev in enumerate(inputFile.Events):

        #Only consider events between first and lastEvent
        if (index < firstEvent):
            continue

        if (lastEvent != -1 and index > lastEvent):
            break

        if (index % 10 == 0 and test) or (index % 1000 == 0 and not test): #Update the loading bar
            updateProgress(round(index/float(nEvents), 2))
            
        if test and index == nEvents:
            break #for testing only
        
        event_start_time = time.time()

        #===================================================
        #Skimming and preselection
        #===================================================

        try: #The third lepton is not always defined
            pt3 = ev.Lepton_pt[2]
        except:
            pt3 = 0.

        if ev.Lepton_pt[0] < 25. or ev.Lepton_pt[1] < 20.: #or pt3 > 10.: #Exactly two leptons, removed for the ttV CR
            continue
            
        #if ev.Lepton_pdgId[0]*ev.Lepton_pdgId[1] >= 0: #Opposite sign leptons only, removed for the fakes CR
        #    continue

        if ev.mll < 20.:
            continue

        #The jet does not always exist, so let's check if it does exist
        try:
            jetpt1 = ev.CleanJet_pt[0]
            jeteta1 = ev.CleanJet_eta[0]
        except:
            jetpt1 = 0.

        try:
            jetpt2 = ev.CleanJet_pt[1]
            jeteta2 = ev.CleanJet_eta[1]
        except:
            jetpt2 = 0.

        try:
            jetpt3 = ev.CleanJet_pt[2]
            jeteta3 = ev.CleanJet_eta[2]
        except:
            jetpt3 = 0.

        try:
            jetpt4 = ev.CleanJet_pt[3]
            jeteta4 = ev.CleanJet_eta[3]
        except:
            jetpt4 = 0.

        #We want at least one jet with pt > 30 and abs(eta) < 2.4
        passJet = False
        for j, jet in enumerate(ev.CleanJet_pt):
            if ev.CleanJet_pt[j] > 30. and abs(ev.CleanJet_eta[j]) < 2.4:
                passJet = True

        if not passJet:
            continue

        #Additional cut removing events having less than one b-jet performed later, once the b-jets have been computed

        #===================================================
        #b-jets collection creation
        #===================================================
        jetIndexes = []
        bJetIndexes = [] #Instead of keeping all the b-jets in a new collection, let's just keep in the trees their indexes to save memory

        mbltJets = []  #Keep jets needed to compute the mblt variable as in https://arxiv.org/pdf/1812.00694.pdf (6.1)
        lastmlbJet = None

        ibjet = 0
        for j, jet in enumerate(ev.CleanJet_pt): #TOCHECK: For now, we only consider b-jets from the clean jets collection
            maxBWeight = -10.0

            jetIndexes.append(j)
            if (year == 2016 and ev.Jet_btagDeepB[ev.CleanJet_jetIdx[j]] > 0.6321) or (year == 2017 and ev.Jet_btagDeepB[ev.CleanJet_jetIdx[j]] > 0.4941) or (year == 2018 and ev.Jet_btagDeepB[ev.CleanJet_jetIdx[j]] > 0.4184):
                bJetIndexes.append(j) #Variable to use for the ttbar reco
                try:
                    bJetsIdx[ibjet] = j #Variable to keep in the tree
                    ibjet = ibjet + 1
                except:
                    pass
                
                if len(mbltJets) < 3:
                    mbltJets.append(j)
            else: #If not a b-jet, we want to keep the highest scoring b-tag weight in the mbltJets list
                bWeight = ev.Jet_btagDeepB[ev.CleanJet_jetIdx[j]]
                if bWeight > maxBWeight:
                    lastmlbJet = j
            
        if(len(mbltJets) < 3 and lastmlbJet is not None): mbltJets.append(lastmlbJet)
        nbJet[0] = len(bJetIndexes)

        #Commented for now as we need to have access to the mt2ll variable for 0b-jets events for the DY Rin-otu method
        #if len(bJetIndexes) == 0: #We don't consider events having less than 1 b-jet
        #    continue 

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
        TMET.SetPtEtaPhiM(ev.MET_pt, 0.0, ev.MET_phi, 0.0)

        #===================================================
        #Ttbar reconstruction
        #===================================================

        #Only try to perform the top reconstruction if we have at least one b-jet
        if len(bJetIndexes) > 0:
            bJetCandidateIndexes = []
            if len(bJetIndexes) > 1:
                bJetCandidateIndexes = bJetIndexes
            else: #If we have exactly one -bjet, then we keep it as the first element while the rest of the list will be made out of usual jets for which we will try to apply the ttbar reconstruction, to try and recover some efficiency of the b-tagging
                bJetCandidateIndexes = bJetIndexes + jetIndexes

            #Remove the duplicates to avoid counting the same jet twice
            bJetCandidateIndexes = list(set(bJetCandidateIndexes))

            maxWeight = 0.0 #Criteria to know which b-jet/lepton combination to keep
            eventKinematic1 = None
            eventKinematic2 = None
            bestReconstructedKinematicWithoutSmearing = None
            bestReconstructedKinematic = None
            inverseOrder = False #Keep track of the b-jet/lepton combination used

            for j, jet in enumerate(bJetCandidateIndexes):

                if j == 0:
                    #By construction, we know that the first element of bJetCandidateIndexes is a b-jet
                    Tb1.SetPtEtaPhiM(ev.CleanJet_pt[jet], ev.CleanJet_eta[jet], ev.CleanJet_phi[jet], ev.Jet_mass[ev.CleanJet_jetIdx[jet]])
                else:
                    Tb2.SetPtEtaPhiM(ev.CleanJet_pt[jet], ev.CleanJet_eta[jet], ev.CleanJet_phi[jet], ev.Jet_mass[ev.CleanJet_jetIdx[jet]])

                    eventKinematic1 = EventKinematic(Tlep1, Tlep2, Tb1, Tb2, Tnu1, Tnu2, TMET)
                    eventKinematic1Original = deepcopy(eventKinematic1)
                    eventKinematic2 = EventKinematic(Tlep2, Tlep1, Tb1, Tb2, Tnu1, Tnu2, TMET)
                    eventKinematic2Original = deepcopy(eventKinematic2)

                    #Perform first of all the reco without smearing
                    eventKinematic1.runReco()
                    eventKinematic1.findBestSolution(distributions["mlb"])
                    if eventKinematic1.weight > maxWeight:
                        bestReconstructedKinematic = eventKinematic1
                        bestReconstructedKinematicWithoutSmearing = eventKinematic1
                        inverseOrder = False
                        maxWeight = eventKinematic1.weight
                    
                    eventKinematic2.runReco()
                    eventKinematic2.findBestSolution(distributions["mlb"])
                    if eventKinematic2.weight > maxWeight:
                        bestReconstructedKinematic = eventKinematic2
                        bestReconstructedKinematicWithoutSmearing = eventKinematic2
                        inverseOrder = True
                        maxWeight = eventKinematic2.weight

                    if bestReconstructedKinematic is None: #Try to perform the smearing until reaching a solution
                        if runSmearing:
                            for i in range(runSmearingNumber): 
                                smearedEventKinematic1 = deepcopy(eventKinematic1Original).runSmearingOnce(distributions) #Get a new object by copying the original one
                                #Keep the solution that has the higher weight
                                if smearedEventKinematic1 is not None and smearedEventKinematic1.weight > maxWeight:
                                    bestReconstructedKinematic = smearedEventKinematic1
                                    inverseOrder = False
                                    maxWeight = smearedEventKinematic1.weight
                                    break

                                #Do the same by reversing the leptons
                                smearedEventKinematic2 = deepcopy(eventKinematic2Original).runSmearingOnce(distributions)
                                #Keep the solution that has the higher weight
                                if smearedEventKinematic2 is not None and smearedEventKinematic2.weight > maxWeight:
                                    bestReconstructedKinematic = smearedEventKinematic2
                                    inverseOrder = True
                                    maxWeight = smearedEventKinematic2.weight
                                    break
        else:
            eventKinematic1 = None
            eventKinematic2 = None
            bestReconstructedKinematicWithoutSmearing = None
            bestReconstructedKinematic = None
            inverseOrder = False

        #Keep track of all the weights needed to computed the top quark pt later on
        weights = []
        top1Pts = [] #Top 1 pts given by the combination using the correct lepton/b-jet combination
        top2Pts = []

        #Run the smearing if needed
        if runSmearing and bestReconstructedKinematic is not None:
            for i in range(runSmearingNumber): 
                smearedEventKinematic = deepcopy(bestReconstructedKinematic).runSmearingOnce(distributions) #Get a new object by copying the original one
                #Keep the solution that has the higher weight
                if smearedEventKinematic is not None and smearedEventKinematic.weight > maxWeight:
                    bestReconstructedKinematic = smearedEventKinematic
                    inverseOrder = False
                    weights.append(smearedEventKinematic.weight)
                    top1Pts.append(smearedEventKinematic.Ttop1)
                    top2Pts.append(smearedEventKinematic.Ttop2)
                    maxWeight = smearedEventKinematic.weight

        recoWorked = False
        nAttempts = nAttempts + 1 #Count the number of event for which the reco worked
        if bestReconstructedKinematic is not None:
            if bestReconstructedKinematic.weight > 0:
                recoWorked = True
                nWorked = nWorked + 1

        if inverseOrder and eventKinematic2 is not None:
            eventKinematic = eventKinematic2
        elif eventKinematic1 is not None:
            eventKinematic = eventKinematic1
        else:
            eventKinematic = None

        #===================================================
        #Dark pt and overlapping factor
        #===================================================

        if recoWorked and eventKinematic is not None:
            reco_weight[0] = bestReconstructedKinematic.weight
            dark_pt[0] = bestReconstructedKinematic.dark_pt
            overlapping_factor[0] = bestReconstructedKinematic.overlapping_factor
        else:
            reco_weight[0] = -99.0
            dark_pt[0] = -99.0
            overlapping_factor[0] = -99.0

        #===================================================
        #MET XY Correction
        #===================================================

        if(year == 2017):
            METcorrected_pt_phi = r.METXYCorr_Met_MetPhi(ev.METFixEE2017_pt, ev.METFixEE2017_phi, ev.run, year, "Run" in filename, ev.PV_npvs)
        else:
            METcorrected_pt_phi = r.METXYCorr_Met_MetPhi(ev.MET_pt, ev.MET_phi, ev.run, year, "Run" in filename, ev.PV_npvs)

        METcorrected_pt[0] = METcorrected_pt_phi[0]
        METcorrected_phi[0] = METcorrected_pt_phi[1]
        TMET.SetPtEtaPhiM(METcorrected_pt_phi[0], 0.0, METcorrected_pt_phi[1], 0.0)

        #===================================================
        #MT2 computation
        #===================================================

        mt2ll[0] = computeMT2(Tlep1, Tlep2, TMET)
        #if eventKinematic is not None: --> Removed to synch our results with Dominic's
            #mt2ll[0] = computeMT2(eventKinematic.Tlep1, eventKinematic.Tlep2, eventKinematic.TMET) 

        if eventKinematic is not None:
            if bestReconstructedKinematicWithoutSmearing is not None and bestReconstructedKinematicWithoutSmearing.weight > 0:
                mt2bl[0] = computeMT2(bestReconstructedKinematicWithoutSmearing.Tlep1 + bestReconstructedKinematicWithoutSmearing.Tb1, bestReconstructedKinematicWithoutSmearing.Tlep2 + bestReconstructedKinematicWithoutSmearing.Tb2, bestReconstructedKinematicWithoutSmearing.TMET) 
            else: #TOCHECK: put default value instead?
                mt2bl[0] = computeMT2(eventKinematic.Tlep1 + eventKinematic.Tb1, eventKinematic.Tlep2 + eventKinematic.Tb2, eventKinematic.TMET) 
        
        else:
            mt2bl[0] = -99.0

        #===================================================
        #Additional variables computation
        #===================================================
       
        #Variables bases on DESY's AN2016-240-v10

        #massT is defined as the mass of the phi component (eta = 0) of the TLorentzVector of the event
        if eventKinematic is not None:
            TMETEta0 = deepcopy(eventKinematic.TMET)
            TMETEta0.SetPtEtaPhiM(TMETEta0.Pt(), 0, TMETEta0.Phi(), TMETEta0.M())
            Tb1Eta0 = deepcopy(eventKinematic.Tb1)
            Tb1Eta0.SetPtEtaPhiM(Tb1Eta0.Pt(), 0, Tb1Eta0.Phi(), Tb1Eta0.M())
            Tb2Eta0 = deepcopy(eventKinematic.Tb2)
            Tb2Eta0.SetPtEtaPhiM(Tb2Eta0.Pt(), 0, Tb2Eta0.Phi(), Tb2Eta0.M())
            Tlep1Eta0 = deepcopy(eventKinematic.Tlep1)
            Tlep1Eta0.SetPtEtaPhiM(Tlep1Eta0.Pt(), 0, Tlep1Eta0.Phi(), Tlep1Eta0.M())
            Tlep2Eta0 = deepcopy(eventKinematic.Tlep2)
            Tlep2Eta0.SetPtEtaPhiM(Tlep2Eta0.Pt(), 0, Tlep2Eta0.Phi(), Tlep2Eta0.M())
            massT[0] = (TMETEta0 + Tb1Eta0 + Tb2Eta0 + Tlep1Eta0 + Tlep2Eta0).M()

            r2l[0] = ev.MET_pt / (eventKinematic.Tlep1.Pt() + eventKinematic.Tlep2.Pt())
            r2l4j[0] = ev.MET_pt / (eventKinematic.Tlep1.Pt() + eventKinematic.Tlep2.Pt() + jetpt1 + jetpt2 + jetpt3 + jetpt4)

            if recoWorked:
                totalET[0] = ev.MET_sumEt + bestReconstructedKinematic.Tb1.Pt() + bestReconstructedKinematic.Tb2.Pt() + bestReconstructedKinematic.Tlep1.Pt() + bestReconstructedKinematic.Tlep2.Pt()
                
                costhetall[0] = bestReconstructedKinematic.Tlep1.CosTheta() * bestReconstructedKinematic.Tlep2.CosTheta()
                costhetal1b1[0] = bestReconstructedKinematic.Tlep1.CosTheta() * bestReconstructedKinematic.Tb1.CosTheta()
                costhetal2b2[0] = bestReconstructedKinematic.Tlep2.CosTheta() * bestReconstructedKinematic.Tb2.CosTheta()
                
                #cos(phi) in the parent rest frame
                try:
                    
                    Ttop1 = bestReconstructedKinematic.Ttop1
                    Ttop2 = bestReconstructedKinematic.Ttop2

                    num1 = [a * b for a, b in zip(top1Pts, weights)]
                    Tnum1 = r.TLorentzVector()
                    for vec in num1: #Unfortunately, in Pyroot the sum() function does not work
                        Tnum1 += vec
                        Ttop1 = Tnum1 * (1./sum(weights))

                    num2 = [a * b for a, b in zip(top2Pts, weights)]
                    Tnum2 = r.TLorentzVector()
                    for vec in num2: 
                        Tnum2 += vec
                        Ttop2 = Tnum2 * (1./sum(weights))
                
                    #First boost
                    boostvectorTT = (Ttop1 + Ttop2).BoostVector()
                    Ttop1.Boost(-boostvectorTT)
                    Ttop2.Boost(-boostvectorTT)

                    #Second boost
                    boostvector = Ttop1.BoostVector()
                    bestReconstructedKinematic.Tlep1.Boost(-boostvectorTT)
                    bestReconstructedKinematic.Tlep1.Boost(-boostvector)

                    boostvector = Ttop2.BoostVector()
                    bestReconstructedKinematic.Tlep2.Boost(-boostvectorTT)
                    bestReconstructedKinematic.Tlep2.Boost(-boostvector)

                    cosphill[0] = (bestReconstructedKinematic.Tlep1.Vect().Unit().Dot(bestReconstructedKinematic.Tlep2.Vect().Unit()))
                except Exception as e:
                    print(e)
                    cosphill[0] = -49.0

            else: #TOCHECK: put default value instead?
                totalET[0] = ev.MET_sumEt + eventKinematic.Tb1.Pt() + eventKinematic.Tb2.Pt() + eventKinematic.Tlep1.Pt() + eventKinematic.Tlep2.Pt()

                costhetall[0] = -99.0
                costhetal1b1[0] = -99.0
                costhetal2b2[0] = -99.0
    
                cosphill[0] = -99.0 #We need the nu information for this variable, so default value if reco failed
        else:
            totalET[0] = -99.0

            r2l[0] = ev.MET_pt / (ev.Lepton_pt[0] + ev.Lepton_pt[1])
            r2l4j[0] = ev.MET_pt / (ev.Lepton_pt[0] + ev.Lepton_pt[1] + jetpt1 + jetpt2 + jetpt3 + jetpt4)

            costhetall[0] = -99.0
            costhetal1b1[0] = -99.0
            costhetal2b2[0] = -99.0
        
            cosphill[0] = -99.0 #We need the nu information for this variable, so default value if reco failed

        #===================================================
        #Compute the mblt variable as in https://arxiv.org/pdf/1812.00694.pdf (6.1)
        #===================================================

        TmbltJet1 = r.TLorentzVector()
        TmbltJet2 = r.TLorentzVector()

        mbltPossibilities = []
        for jet1 in mbltJets:
            TmbltJet1.SetPtEtaPhiM(ev.CleanJet_pt[jet1], ev.CleanJet_eta[jet1], ev.CleanJet_phi[jet1], ev.Jet_mass[ev.CleanJet_jetIdx[jet1]])
                
            for jet2 in mbltJets:
                if jet2 != jet1:
                    TmbltJet2.SetPtEtaPhiM(ev.CleanJet_pt[jet2], ev.CleanJet_eta[jet2], ev.CleanJet_phi[jet2], ev.Jet_mass[ev.CleanJet_jetIdx[jet2]])
                    mbltPossibilities.append(max((Tlep1 + TmbltJet1).M(), (Tlep2 + TmbltJet2).M()))

        if len(mbltPossibilities) != 0:
            mblt[0] = min(mbltPossibilities)
        else:
            mblt[0] = -99.0

        outputTree.Fill()
        
    try:
        print '\nThe ttbar reconstruction worked for ' + str(round((nWorked/float(nAttempts))*100, 2)) + '% of the events considered'
        print 'Total execution time: ' + str(time.time() - start_time) + ' seconds'
        print 'Mean execution time: ' + str(round(((time.time() - start_time)/nEvents), 2)) + ' seconds/event'
    except:
        print 'Done!'

    outputFile.cd()
    outputTree.Write()
    inputFile.Close()
    outputFile.Close()
    distFile.Close()

def computeMT2(VisibleA, VisibleB, Invisible, MT2Type = 0, MT2Precision = 0) :

    mVisA = abs(VisibleA.M())  # Mass of visible object on side A. Must be >= 0
    mVisB = abs(VisibleB.M())  # Mass of visible object on side B. Must be >= 0

    chiA = 0.  # Hypothesized mass of invisible on side A. Must be >= 0
    chiB = 0.  # Hypothesized mass of invisible on side B. Must be >= 0
  
    if MT2Type == 1: # This is for mt2 with b jets

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


def fixOperations():
    """
    Needed for reasons explained in https://root-forum.cern.ch/t/cannot-perform-both-dot-product-and-scalar-multiplication-on-tvector2-in-pyroot/28207
    """

    #Addition                                                                                                                                                   
    r.TVector3(1, 1, 1) + r.TVector3(2, 2, 1)
    mvv = r.TVector3.__add__
    del r.TVector3.__add__
    #r.TVector3(1, 1, 1) + 5
    #mvs = r.TVector3.__add__

    def fixadd(self, other, mvv=mvv):
        if isinstance(other, self.__class__):
            return mvv(self, other)
            #return mvs(self, other)

    r.TVector3.__add__ = fixadd

    #Multiplication                                                                                                                                             
    r.TVector3(1, 1, 1) * r.TVector3(2, 2, 1)
    mvv = r.TVector3.__mul__
    del r.TVector3.__mul__
    r.TVector3(1, 1, 1) * 5
    mvs = r.TVector3.__mul__

    def fixmul(self, other, mvv=mvv, mvs=mvs):
        if isinstance(other, self.__class__):
            return mvv(self, other)
            return mvs(self, other)

    r.TVector3.__mul__ = fixmul


if __name__ == "__main__":

    # =========================================== 
    # Argument parser                            
    # ===========================================
    
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-f', '--filename', action='store', type=str, dest='filename', default="")
    parser.add_option('-i', '--inputDir', action='store', type=str, dest='inputDir', default="")
    parser.add_option('-o', '--outputDir', action='store', type=str, dest='outputDir', default="/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/")
    parser.add_option('-b', '--baseDir', action='store', type=str, dest='baseDir', default="/afs/cern.ch/user/c/cprieels/work/public/TopPlusDMRunIILegacy/CMSSW_10_4_0/src/neuralNetwork/")
    parser.add_option('-p', '--splitNumber', action='store', type=int, dest='splitNumber', default=-1)
    parser.add_option('-c', '--firstEvent', action='store', type=int, dest='firstEvent', default=0)
    parser.add_option('-d', '--lastEvent', action='store', type=int, dest='lastEvent', default=0)
    parser.add_option('-y', '--year', action='store', type=int, dest='year', default=2018) #Year, to know the value of the medium b-tag working point

    parser.add_option('-t', '--test', action='store_true', dest='test')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')
    (opts, args) = parser.parse_args()

    filename = opts.filename
    inputDir = opts.inputDir
    outputDir = opts.outputDir
    baseDir = opts.baseDir
    splitNumber = opts.splitNumber
    firstEvent = opts.firstEvent
    lastEvent = opts.lastEvent
    year = int(opts.year)
    test = opts.test
    verbose = opts.verbose

    if year not in [2016, 2017, 2018]:
        print("The year for the production does not seem to be valid")
        exit

    #Needed for reasons explained in https://root-forum.cern.ch/t/cannot-perform-both-dot-product-and-scalar-multiplication-on-tvector2-in-pyroot/28207
    fixOperations()
    createTree(inputDir, outputDir, baseDir, filename, firstEvent, lastEvent, splitNumber, year)
    
