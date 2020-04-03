
import ROOT as r
import os,  sys, fnmatch
import math

"""
Code used to generate true simulation/reco distribution from Latino ttbar files used to perform the smearing
"""
#===============================================================================0
#PROGRESS BAR
#===============================================================================0

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

#===============================================================================0
#MAIN FUNCTION
#===============================================================================0

#Let's consider the ttbar files in a chain
#baseDir = os.getcwd()+"/"
baseDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
filesChain = r.TChain("Events")
listOfFiles = os.listdir(baseDir)
pattern = "*"+"TTTo2L2Nu__part"+"*.root"

for index, entry in enumerate(listOfFiles):
    if fnmatch.fnmatch(entry, pattern):
        filesChain.AddFile(baseDir+entry)

#Define the histograms
bwHist = t.TH1F("bw", "Breit-Wigner W boson distribution", 40, 60, 100)
mlbHistTrue = r.TH1F("mlbTrue", "Mlb generation distribution", 100, 0, 200)
jerHistTrue = r.TH1F("jerTrue", "JER generation distribution", 100, 0, 500) #Jet energy resolution
jerHistReco = r.TH1F("jerReco", "JER reco distribution", 100, 0, 500) 
jerHist = r.TH1F("jer", "Jet energy correction factor", 100, 0, 3)
lerHistTrue = r.TH1F("lerTrue", "LER generation distribution", 100, 0, 500)
lerHistReco = r.TH1F("lerReco", "LER reco distribution", 100, 0, 500)
lerHist = r.TH1F("ler", "Lepton energy correction factor", 100, 0.5, 1.5)

jphatHist = r.TH1F("jphat", "Jet angular distribution", 200, 0, 0.3)
lphatHist = r.TH1F("lphat", "Lepton angular distribution", 200, 0, 0.02)

#Start the loop
#nEvents = filesChain.GetEntries()
nEvents = 4000000
for index, ev in enumerate(filesChain):
    if index % 100 == 0: #Update the loading bar every 100 events                                                                                                                                              
            updateProgress(round(index/float(nEvents), 2))

    if index == 4000000: #For testing only
        break

    #===================================================
    #First, get the simulation information
    #===================================================

    #First of all, select events having exactly two leptons coming from W bosons
    leptons = []
    for l, lepton in enumerate(ev.LeptonGen_pt):
        if abs(ev.LeptonGen_pdgId[l]) == 11 or abs(ev.LeptonGen_pdgId[l]) == 13:
            if(ev.LeptonGen_isPrompt[l] == 1): #Select only prompt leptons (coming from the top)
                lepton = r.TLorentzVector()
                lepton.SetPtEtaPhiM(ev.LeptonGen_pt[l], ev.LeptonGen_eta[l], ev.LeptonGen_phi[l], ev.LeptonGen_mass[l])
                leptons.append([lepton, ev.LeptonGen_pdgId[l]])
                
    #Then, do the same for the b jets
    bjets = []
    for j, jet in enumerate(ev.GenJet_pt):
        if abs(ev.GenJet_partonFlavour[j]) == 5:
            bjet = r.TLorentzVector()
            bjet.SetPtEtaPhiM(ev.GenJet_pt[j], ev.GenJet_eta[j], ev.GenJet_phi[j], ev.GenJet_mass[j])
            bjets.append([bjet, ev.GenJet_partonFlavour[j]])

    if len(leptons) == 2 and len(bjets) == 2:
        for i in range(2):
            try:
                if leptons[i][1] * bjets[i][1] < 0:
                    #Fill the true histograms
                    mlbHistTrue.Fill((leptons[i][0] + bjets[i][0]).M())
                    jerHistTrue.Fill(bjets[i][0].E())
                    lerHistTrue.Fill(leptons[i][0].E())
            except:
                pass

    #===================================================
    #Then, get the reco information
    #===================================================

    recoLeptons = []

    if len(ev.Lepton_pt) != 2:
        continue

    for l, lepton in enumerate(ev.Lepton_pt):
        Tlep = r.TLorentzVector()
        Tlep.SetPtEtaPhiM(ev.Lepton_pt[l], ev.Lepton_eta[l], ev.Lepton_phi[l], 0.000511 if (abs(ev.Lepton_pdgId[l]) == 11) else 0.106)
        recoLeptons.append(Tlep)

    recoJetIndexes = []
    recobJetIndexes = [] #Instead of keeping all the b-jets in a new collection, let's just keep in the trees their indexes to save memory

    for j, jet in enumerate(ev.CleanJet_pt): #TOCHECK: For now, we only consider b-jets from the clean jets collection
        recoJetIndexes.append(j)
        if ev.Jet_btagDeepB[ev.CleanJet_jetIdx[j]] > 0.2217: #TOCHECK: Loose WP for now
            recobJetIndexes.append(j)

    recobjets = []
    for j, jet in enumerate(recobJetIndexes):
        Tb = r.TLorentzVector()
        Tb.SetPtEtaPhiM(ev.CleanJet_pt[jet], ev.CleanJet_eta[jet], ev.CleanJet_phi[jet], ev.Jet_mass[ev.CleanJet_jetIdx[jet]])
        recobjets.append(Tb)

    if len(recobjets) != 2:
        continue

    #Now, let's find the best lepton/b-jet combination based on the invariant mass of the system    
    combinations = []
    for l, lepton in enumerate(recoLeptons):
        for b, bjet in enumerate(recobjets):
            invMass = (lepton + bjet).M()
            if invMass - 173.0 < 2.:
                combinations.append([lepton, bjet])

    for combination in combinations:
        try:
            #Fill the reco histograms
            jerHistReco.Fill(combination[1].E())
            lerHistReco.Fill(combination[0].E())
        except:
            pass

    #Finally, fill the ratio histograms
    if len(combinations) != 2:
        continue

    for i in range(2):
        try:
            jerHist.Fill(bjets[i][0].E()/combinations[i][1].E())
            lerHist.Fill(leptons[i][0].E()/combinations[i][0].E())

            jvectorTrue = [math.cos(bjets[i][0].Phi()) * math.sin(bjets[i][0].Theta()), math.sin(bjets[i][0].Phi()) * math.sin(bjets[i][0].Theta()), math.cos(bjets[i][0].Theta())]
            jvectorReco = [math.cos(combinations[i][1].Phi()) * math.sin(combinations[i][1].Theta()), math.sin(combinations[i][1].Phi()) * math.sin(combinations[i][1].Theta()), math.cos(combinations[i][1].Theta())]
            jalpha = math.acos(sum([x*y for x,y in zip(jvectorTrue, jvectorReco)]))
            jphatHist.Fill(jalpha)

            lvectorTrue = [math.cos(leptons[i][0].Phi()) * math.sin(leptons[i][0].Theta()), math.sin(leptons[i][0].Phi()) * math.sin(leptons[i][0].Theta()), math.cos(leptons[i][0].Theta())]
            lvectorReco = [math.cos(combinations[i][0].Phi()) * math.sin(combinations[i][0].Theta()), math.sin(combinations[i][0].Phi()) * math.sin(combinations[i][0].Theta()), math.cos(combinations[i][0].Theta())]
            lalpha = math.acos(sum([x*y for x,y in zip(lvectorTrue, lvectorReco)]))
            lphatHist.Fill(lalpha)

        except:
            pass

mlbHistTrue.Scale(1.0/mlbhist.Integral())
mlbHistTrue.SetTitle("Generation mlb distribution")
mlbHistTrue.GetXaxis().SetTitle("mlb [GeV]")

jerHistTrue.SetTitle("Jet energy response true distribution")
jerHistTrue.GetXaxis().SetTitle("E [GeV]")
lerHistTrue.SetTitle("Lepton energy response true distribution")
lerHistTrue.GetXaxis().SetTitle("E [GeV]")
jerHistReco.SetTitle("Jet energy response reco distribution")
jerHistReco.GetXaxis().SetTitle("E [GeV]")
lerHistReco.SetTitle("Lepton energy response reco distribution")
lerHistReco.GetXaxis().SetTitle("E [GeV]")

jerHistReco.SetTitle("Jet energy response correction")
jerHistReco.GetXaxis().SetTitle("Etrue/Ereco [GeV]")
lerHistReco.SetTitle("Lepton energy response correction")
lerHistReco.GetXaxis().SetTitle("Etrue/Ereco [GeV]")

jerHist.SetTitle("Jet energy correction factor")
jerHist.GetXaxis().SetTitle("Etrue/Ereco")
lerHist.SetTitle("Lepton energy correction factor")
lerHist.GetXaxis().SetTitle("Etrue/Ereco")

jphatHist.SetTitle("Angular correction for b-jets")
jphatHist.GetXaxis().SetTitle("#alpha [rad]")
lphatHist.SetTitle("Angular correction for leptons")
lphatHist.GetXaxis().SetTitle("#alpha [rad]")

rand = r.TRandom3()
for i in range(100000):
    value = rand.BreitWigner(80.379, 2.085)
    bwhist.Fill(value)

bwHist.Scale(1.0/bwhist.Integral())
bwHist.SetTitle("Breit-Wigner W boson distribution")
bwHist.GetXaxis().SetTitle("W mass [GeV]")

#Keep the histograms in a new file
outputFile = r.TFile.Open("distributions.root", "recreate")

mlbHistTrue.Write()
jerHistTrue.Write()
lerHistTrue.Write()
jerHistReco.Write()
lerHistReco.Write()

jerHist.Write()
lerHist.Write()

jphatHist.Write()
lphatHist.Write()

bwHist.Write()

outputFile.Close()
