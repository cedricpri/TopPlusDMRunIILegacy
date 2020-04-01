#Code used to read the input files for dnn.py and create additional variables we use for the discrimination
import ROOT
from ROOT import TFile, TTree, TLorentzVector
from array import array
import optparse
import os, sys, fnmatch

import math
import matplotlib.pyplot as plt
import numpy as np
from ttbarReco import ttbar #ttbar reconstruction
LinAlgError = np.linalg.linalg.LinAlgError

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

    inputFile = TFile.Open(inputDir+filename, "r")
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
    ROOT.gROOT.ProcessLine('.L '+os.getcwd()+'/mt2Calculation/lester_mt2_bisect.h+')

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

        Tlep1 = TLorentzVector()
        Tlep2 = TLorentzVector()
        Tnu1  = TLorentzVector()
        Tnu2  = TLorentzVector()
        TMET  = TLorentzVector()

        Tlep1.SetPtEtaPhiM(ev.Lepton_pt[0], ev.Lepton_eta[0], ev.Lepton_phi[0], 0.000511 if (abs(ev.Lepton_pdgId[0]) == 11) else 0.106)
        Tlep2.SetPtEtaPhiM(ev.Lepton_pt[1], ev.Lepton_eta[1], ev.Lepton_phi[1], 0.000511 if (abs(ev.Lepton_pdgId[1]) == 11) else 0.106)
        Tnu1.SetPtEtaPhiM(-99.0, -99.0, -99.0, -99.0) #Not needed for the ttbar reconstruction and not available, we can pass default values
        Tnu2.SetPtEtaPhiM(-99.0, -99.0, -99.0, -99.0)
        TMET.SetPtEtaPhiM(ev.MET_pt, 0.0, ev.MET_phi, 0.0) #TOCHECK: use the MET or PUPPIMET?

        #===================================================
        #Ttbar reconstruction
        #===================================================
        
        bJetCandidateIndexes = []
        if len(bJetIndexes) > 1:
            bJetCandidateIndexes = bJetIndexes
        else: #If we have exactly one -bjet, then we keep it as the first element while the rest of the list will be made out of usual jets for which we will try to apply the ttbar reconstruction, to try and recover some efficiency of the b-tagging
            bJetCandidateIndexes = bJetIndexes + jetIndexes

        recoOutput = runReco(ev, Tlep1, Tlep2, Tnu1, Tnu2, TMET, bJetCandidateIndexes)
        Tb1Updated = recoOutput[0][0]
        Tb2Updated = recoOutput[0][1]
        Tnu1Updated = recoOutput[1][0]
        Tnu2Updated = recoOutput[1][1]
        nuSol = recoOutput[2] #Optimal nuSol object

        recoWorked = False
        nAttempts = nAttempts + 1 #Count the number of times the reco worked
        if Tb1Updated is not None and Tb2Updated is not None:
            if Tnu1Updated is not None and Tnu2Updated is not None: #The reconstruction worked
                recoWorked = True
                nWorked = nWorked + 1

        #===================================================
        #Dark pt and overlapping factor
        #===================================================

        if recoWorked: 
            #Compute the dark pt and all the needed variables from this particular combination
            try:
                overlapping_factor[0] = nuSol.overlapingFactor(nuSol.N, nuSol.n_)
                #if nuSol.overlapingFactor(nuSol.N, nuSol.n_) < 0.2: #TOCHECK: put back this cut and tweak it?
                dark_pt[0] = nuSol.darkPt('DarkPt')
                
                """
                #Plot the ellipses if needed
                m,b=nuSol.ellipseSeparation(nuSol.N,nuSol.n_,'LineParameters')
                x=np.r_[-600:600]
                plt.plot(x,m*x+b);
                plt.show()
                nuSol.darkPt('ttbarEllipse')
                nuSol.plotEllipse(nuSol.N,'black')
                nuSol.plotEllipse(nuSol.n_,'red')
                
                plt.savefig('ElipsesDARKPT/Elipse'+str(index)+'.png')
                plt.clf()
                """

            except:
                overlapping_factor[0] = -99.0
                dark_pt[0] = -99.0
        else: #Some variables have to be set the non-physical default values if the reconstruction did not work
            overlapping_factor[0] = -999.0 #-999 is the default value if the reconstruction did not work
            dark_pt[0] = -999.0

        #===================================================
        #MT2 computation
        #===================================================

        mt2ll[0] = computeMT2(Tlep1, Tlep2, TMET, 0) 
        if recoWorked:
            try:
                mt2bl[0] = computeMT2(Tlep1 + Tb1Updated, Tlep2 + Tb2Updated, TMET, 0) 
            except:
                mt2bl[0] = -99.0
        else:
            mt2bl[0] = -999.0

        #===================================================
        #Additional variables computation
        #===================================================

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

        outputTree.Fill()

    print '\nThe ttbar reconstruction worked for ' + str(round((nWorked/float(nAttempts))*100, 2)) + '% of the events considered'

    outputTree.Write()
    inputFile.Close()
    outputFile.Close()


def runReco(ev, Tlep1, Tlep2, Tnu1, Tnu2, TMET, bJetCandidateIndexes): 
    """
    Function performing the ttbar reconstruction and the smearing of the jets.
    Returns a list with the two optimal b-jets and corresponding neutrinos TLorentzVector found. 
    """

    Tb1   = TLorentzVector()
    Tb2   = TLorentzVector()

    rand = ROOT.TRandom3() #For the smearing

    minInvMass = 9999999. #The best jet will be the one minimizing this value
    Tnu1Optimal, Tnu2Optimal = None, None #Best is considered over the possible solution, optimal is additionally the best solution and the best jet
    Tb2Optimal = None
    nuSolOptimal = None #Return the nuSOl object as well

    for i, jet in enumerate(bJetCandidateIndexes):
        if i == 0:
            Tb1.SetPtEtaPhiM(ev.CleanJet_pt[jet], ev.CleanJet_eta[jet], ev.CleanJet_phi[jet], ev.Jet_mass[ev.CleanJet_jetIdx[jet]]) #By construction, we know that the first element of bJetCandidateIndexes is a b-jet
        else:
            Tb2.SetPtEtaPhiM(ev.CleanJet_pt[jet], ev.CleanJet_eta[jet], ev.CleanJet_phi[jet], ev.Jet_mass[ev.CleanJet_jetIdx[jet]])
            
            mW1, mW2 = 80.379, 80.379
            mt1, mt2 = 173.0, 173.0 #TOCHECK: use a Breit-Wigner as well?

            neutrinos = findBestSolution(Tb1, Tb2, Tlep1, Tlep2, Tnu1, Tnu2, TMET, mW1, mW2, mt1, mt2) #Find the best solution for the jet considered
            Tnu1Best, Tnu2Best = neutrinos[0][0], neutrinos[0][1]
            nuSol = neutrinos[1]

            if Tnu1Best is not None and Tnu2Best is not None and nuSol is not None:
                invMass = (Tnu1Best + Tlep1 + Tb1).M() + (Tnu2Best + Tlep2 + Tb2).M()
                if invMass < minInvMass:
                    minInvMass = minInvMass
                    Tnu1Optimal, Tnu2Optimal = Tnu1Best, Tnu2Best
                    Tb2Optimal = Tb2
                    nuSolOptimal = nuSol

        #We now have to access to the optimal b-jets and the optimal neutrino solution for these jets, so let's do the smearing
        #runSmearing(Tb1, Tb2Optimal, Tlep1, Tlep2, Tnu1Optimal, Tnu2Optimal, TMET, mt1, mt2)

    return [[Tnu1Optimal, Tnu2Optimal], [Tb1, Tb2Optimal], nuSolOptimal]


def findBestSolution(Tb1, Tb2, Tlep1, Tlep2, Tnu1, Tnu2, TMET, mW1, mW2, mt1, mt2):
    """
    Function that actually performs the reconstruction and returns the best possible solution found.
    """

    try:
        nuSol = ttbar.solveNeutrino(Tb1, Tb2, Tlep1, Tlep2, Tnu1, Tnu2, TMET, mW1, mW2, mt1, mt2)
    except:
        nuSol = None

    Tnu1 = TLorentzVector()
    Tnu2 = TLorentzVector()

    Tnu1Best = None #Keep the best neutrinos to return them
    Tnu2Best = None

    minInvMass = 9999999.

    if nuSol is not None:
        for s, possibleSolution in enumerate(nuSol.solution): #The reconstruction can give either 0, 2 or 4 solutions
            
            Tnu1.SetPxPyPzE(possibleSolution[0][0], possibleSolution[0][1], possibleSolution[0][2], math.sqrt(possibleSolution[0][0]**2 + possibleSolution[0][1]**2 + possibleSolution[0][2]**2)) #TOCHECK: value of the total momentum (=energy) of a neutrino
            Tnu2.SetPxPyPzE(possibleSolution[1][0], possibleSolution[1][1], possibleSolution[1][2], math.sqrt(possibleSolution[1][0]**2 + possibleSolution[1][1]**2 + possibleSolution[1][2]**2)) #possibleSolution[0] is the neutrino, possibleSolution[0][0] its momentum along the x-axis
                            
            if (((Tnu1 + Tlep1 + Tb1).M() - mt1) > 2.): #TOCHECK: tweak this value?
                kk = Tlep1 #Invert the lepton1 and the lepton2 is we see this gives better results
                Tlep1 = Tlep2
                Tlep2 = kk
                print("Lepton switch performed")

            invMass = (Tnu1+Tlep1+Tb1).M() + (Tnu2+Tlep2+Tb2).M()
            if invMass < minInvMass:
                minInvMass = minInvMass
                Tnu1Best, Tnu2Best = Tnu1, Tnu2

    return [[Tnu1Best, Tnu2Best], nuSol]


def runSmearing(Tb1, Tb2Optimal, Tlep1, Tlep2, Tnu1Optimal, Tnu2Optimal, TMET, mt1, mt2):
    """
    Run the reco multiple times by changing the input parameters.
    """
    Tb1Updated = TLorentzVector()
    Tb2Updated = TLorentzVector()

    for n in range(0, 100):
        #Update the W mass
        mW1 = rand.BreitWigner(80.379, 2.085)
        mW2 = rand.BreitWigner(80.379, 2.085)

        #Update the leptons?

        #Update the jets
        Tb1Uncertainty = rand.Gaus(0, 0.3) * Tb1.E() 
        Tb2Uncertainty = rand.Gaus(0, 0.3) * Tb2Optimal.E() 
        ptCorrection1 = math.sqrt((Tb1.E() + Tb1Uncertainty)**2 - tb1.M()**2)/Tb1.P()
        ptCorrection2 = math.sqrt((Tb2.E() + Tb2Uncertainty)**2 - tb2.M()**2)/Tb2.P()
        
        Tb1Updated.SetPtEtaPhi(Tb1.Pt()*ptCorrection1, Tb1.Eta(), Tb1.Phi(), Tb1.M())
        Tb2Updated.SetPtEtaPhi(Tb2.Pt()*ptCorrection2, Tb2.Eta(), Tb2.Phi(), Tb2.M())
            
        #Update the MET
        TVector2 deltaP1(Tb1Updated.Px() - Tb1.Px(), Tb1Updated.Py() - Tb1.Py())
        TVector2 deltaP2(Tb2Updated.Px() - Tb2.Px(), Tb2Updated.Py() - Tb2.Py())
        TMETUpdated = TMET + DeltaP1 + DeltaP2
        
        #Solve with the new parameters
        findBestSolution(Tb1, Tb2, Tlep1, Tlep2, Tnu1, Tnu2, TMET, mW1, mW2, mt1, mt2)

        #Get the weights
        #getWeight(lep1, lep2, newJet1, newJet2, nu1, nu2, localTop1, localTop2, localW)

    return solution


def getWeight(params):
    pass


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
    
    mT2 = ROOT.asymm_mt2_lester_bisect().get_mT2(mVisA, pxA, pyA,
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
    
