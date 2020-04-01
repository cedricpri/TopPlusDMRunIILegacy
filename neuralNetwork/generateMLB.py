
import ROOT as r
import os,  sys, fnmatch
import math

"""
Code used to generate true mlb distribution from Latino ttbar files
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
baseDir = os.getcwd()+"/"
#baseDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
filesChain = r.TChain("Events")
listOfFiles = os.listdir(baseDir)
pattern = "*"+"TTTo2L2Nu__part"+"*.root"

for index, entry in enumerate(listOfFiles):
    if fnmatch.fnmatch(entry, pattern):
        filesChain.AddFile(baseDir+entry)

#Define the histogram
mlbhist = r.TH1F("mlb", "Mlb generation distribution", 100, 0, 200)
nEvents = filesChain.GetEntries()

for index, ev in enumerate(filesChain):
    if index % 100 == 0: #Update the loading bar every 100 events                                                                                                                                              
            updateProgress(round(index/float(nEvents), 2))

    #First of all, select events having exactly two leptons coming from W bosons
    leptons = []
    for l, lepton in enumerate(ev.LeptonGen_pt):
        if abs(ev.LeptonGen_pdgId[l]) == 11 or abs(ev.LeptonGen_pdgId[l]) == 13:
            if(ev.LeptonGen_isPrompt[l] == 1): #Select only prompt leptons (coming from the top)
                lepton = r.TLorentzVector()
                lepton.SetPtEtaPhiM(ev.LeptonGen_pt[l], ev.LeptonGen_eta[l], ev.LeptonGen_phi[l], ev.LeptonGen_mass[l])
                leptons.append([lepton, ev.LeptonGen_pdgId[l]])
                
    if len(leptons) != 2:
        continue

    #Then, do the same for the b jets
    bjets = []
    for j, jet in enumerate(ev.GenJet_pt):
        if abs(ev.GenJet_partonFlavour[j]) == 5:
            bjet = r.TLorentzVector()
            bjet.SetPtEtaPhiM(ev.GenJet_pt[j], ev.GenJet_eta[j], ev.GenJet_phi[j], ev.GenJet_mass[j])
            bjets.append([bjet, ev.GenJet_partonFlavour[j]])

    if len(bjets) != 2:
        continue

    #Now, let's match the leptons and the b-jets
    for i in range(2):
        try:
            if leptons[i][1] * bjets[i][1] < 0:
                mlbhist.Fill((leptons[i][0] + bjets[i][0]).M())
        except:
            continue
        
mlbhist.Scale(1.0/mlbhist.Integral())
mlbhist.SetTitle("Generation mlb distribution")
mlbhist.GetXaxis().SetTitle("mlb [GeV]")

#Keep the histogram in a new file
outputFile = r.TFile.Open("mlb.root", "recreate")
mlbhist.Write()
outputFile.Close()
