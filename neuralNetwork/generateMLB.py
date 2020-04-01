
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
mlbhist = r.TH1F("mlb", "Mlb generation distribution", 20, 0, 200)
nEvents = filesChain.GetEntries()

for index, ev in enumerate(filesChain):
    if index % 100 == 0: #Update the loading bar every 100 events                                                                                                                                              
            updateProgress(round(index/float(nEvents), 2))

    leptons = []
    Ws = []
    bjets = []

    for p, particle in enumerate(ev.GenPart_pdgId):
        
        #Fill the leptons
        try:
            lepton = r.TLorentzVector()
            W = r.TLorentzVector()

            if abs(ev.GenPart_pdgId[p]) == 11 or abs(ev.GenPart_pdgId[p]) == 13:

                #Let's check if the mother of this lepton is a W
                if abs(ev.GenPart_pdgId[ev.GenPart_genPartIdxMother[p]]) == 24:

                    #Let's check if they have the same sign
                    if ev.GenPart_pdgId[p] * ev.GenPart_pdgId[ev.GenPart_genPartIdxMother[p]] < 0:

                        #Let's check if the lepton grandmother is a top quark
                        if abs(ev.GenPart_pdgId[ev.GenPart_genPartIdxMother[ev.GenPart_genPartIdxMother[p]]]) == 6:
                            leptons.append(lepton.SetPtEtaPhiM(ev.GenPart_pt[p], ev.GenPart_eta[p], ev.GenPart_phi[p], ev.GenPart_mass[p]))
                            Ws.append(W.SetPtEtaPhiM(ev.GenPart_pt[ev.GenPart_genPartIdxMother[p]], ev.GenPart_eta[ev.GenPart_genPartIdxMother[p]], ev.GenPart_phi[ev.GenPart_genPartIdxMother[p]], 80.38))

        except: #The lepton probably does not have a mother and a grandmother
            print("Error in creation of lepton/W TLorentzVector")

        #Fill the jets
        try:
            bjet = r.TLorentzVector()
            if abs(ev.GenPart_pdgId[p]) == 5:
                if abs(ev.GenPart_pdgId[ev.GenPart_genPartIdxMother[p]]) == 6:
                    bjets.append(bjet.SetPtEtaPhiM(ev.GenPart_pt[p], ev.GenPart_eta[p], ev.GenPart_phi[p], ev.GenPart_mass[p]))
        except:
            print("Error in creation of bjet TLorentzVector")

    #print(len(leptons), len(Ws), len(bjets))
    if len(leptons) < 2 or len(Ws) < 2 or len(bjets) < 2:
        continue

    #Now, let's match the leptons and the b-jets by comparing the invariant mass of the system with the top
    combinations = []
    for l, lepton in enumerate(leptons):
        for b, bjet in enumerate(bjets):
            invMass = (lepton + Ws[l] + bjet).M() - 173.0
            print(invMass)
            if abs(invMass) < 2.: #One correct combination found
                combinations.append([l, b])
                
                #Remove the lepton and the bjet just considered
                #leptons.remove(lepton)
                #bjets.remove(bjet)

    #if len(combinations) == 2:
    print(combinations)
            


    """
    l1 = r.TLorentzVector()
    l2 = r.TLorentzVector()
    j1 = r.TLorentzVector()    
    j2 = r.TLorentzVector()

    l1.SetPtEtaPhiM(ev.LeptonGen_pt[0], ev.LeptonGen_eta[0], ev.LeptonGen_phi[0], 0.000511 if (abs(ev.LeptonGen_pdgId[0]) == 11) else 0.106)
    l2.SetPtEtaPhiM(ev.LeptonGen_pt[1], ev.LeptonGen_eta[1], ev.LeptonGen_phi[1], 0.000511 if (abs(ev.LeptonGen_pdgId[0]) == 11) else 0.106)

    #Get the mothers of these two lepton gen
    moth1 = ev.LeptonGen_MotherPID[0]
    moth2 = ev.LeptonGen_MotherPID[1]
    """
    

