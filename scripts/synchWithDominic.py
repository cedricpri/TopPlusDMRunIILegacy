import glob
import ROOT as r

ECALRegion0 = "(abs(Lepton_pdgId[0]) != 11 || ((Lepton_eta[0] + Electron_deltaEtaSC[Lepton_electronIdx[0]]) < -1.566 || ((Lepton_eta[0] + Electron_deltaEtaSC[Lepton_electronIdx[0]]) > -1.444 && (Lepton_eta[0] + Electron_deltaEtaSC[Lepton_electronIdx[0]]) < 1.444) || (Lepton_eta[0] + Electron_deltaEtaSC[Lepton_electronIdx[0]]) > 1.566))"
ECALRegion1 = "(abs(Lepton_pdgId[1]) != 11 || ((Lepton_eta[1] + Electron_deltaEtaSC[Lepton_electronIdx[1]]) < -1.566 || ((Lepton_eta[1] + Electron_deltaEtaSC[Lepton_electronIdx[1]]) > -1.444 && (Lepton_eta[1] + Electron_deltaEtaSC[Lepton_electronIdx[1]]) < 1.444) || (Lepton_eta[1] + Electron_deltaEtaSC[Lepton_electronIdx[1]]) > 1.566))"
METFilters = "Flag_goodVertices*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter"

#Main parameters
#query = "DMscalar_Dilepton_top_tWChan_Mchi1_Mphi100_"
#query = "TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_100_"
#query="DoubleEG_Run2016D"
query="ST_tW_top"

category = "MC2016"
baseCuts = "Sum$((Lepton_isTightElectron_cutBasedMediumPOG+Lepton_isTightMuon_mediumRelIsoTight)==1)==2 && Lepton_pt[0] > 25. && Lepton_pt[1] > 20. && mll > 20. && (Lepton_pdgId[0] * Lepton_pdgId[1]) < 0 && " + ECALRegion0 + " && " + ECALRegion1
cuts = ["1", 
        "((Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) || (mll < 76 || mll > 106))",
        "((Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) || (mll < 76 || mll > 106)) && Sum$(CleanJet_pt >= 20. && abs(CleanJet_eta) < 2.4) >= 1",
        "((Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) || (mll < 76 || mll > 106)) && Sum$(CleanJet_pt >= 20. && abs(CleanJet_eta) < 2.4) >= 1 && nbJet >= 1",
        "((Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) || (mll < 76 || mll > 106)) && Sum$(CleanJet_pt >= 20. && abs(CleanJet_eta) < 2.4) >= 1 && nbJet >= 1 && mt2ll < 80."]
channels = ["ll"]#, "ee", "df", "mm"]
myTrees = True
applyTriggers = True


#weight = '35.9 * 1.007 * baseW*genWeight*puWeight*customTriggerSF*((abs(Lepton_pdgId[0])==13)+(Lepton_RecoSF[0]*(abs(Lepton_pdgId[0])==11)))*((abs(Lepton_pdgId[1])==13)+(Lepton_RecoSF[1]*(abs(Lepton_pdgId[1])==11)))*Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[0]*Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[1]*Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[0]*Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[1]*(((nbJet == 0) * (1.-btagWeight_1tag_btagDeepBM_1c)) + ((nbJet > 0) * btagWeight_1tag_btagDeepBM_1c))*PrefireWeight*Flag_goodVertices*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter*Flag_globalSuperTightHalo2016Filter'
#weight='35.9 * 1.007 * baseW*puWeight*customTriggerSF*Flag_goodVertices*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter*Flag_globalSuperTightHalo2016Filter*Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[0]*Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[1]*Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[0]*Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[1]*((abs(Lepton_pdgId[0])==13)+(Lepton_RecoSF[0]*(abs(Lepton_pdgId[0])==11)))*((abs(Lepton_pdgId[1])==13)+(Lepton_RecoSF[1]*(abs(Lepton_pdgId[1])==11)))'
"""
weight = "35.9 * 1.007 * baseW*puWeight*customTriggerSF * \
Flag_goodVertices*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter*Flag_globalSuperTightHalo2016Filter * \
Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[0] * Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[1] * \
Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[0] * Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[1] * \
((abs(Lepton_pdgId[0])==13)+(Lepton_RecoSF[0]*(abs(Lepton_pdgId[0])==11)))*((abs(Lepton_pdgId[1])==13)+(Lepton_RecoSF[1]*(abs(Lepton_pdgId[1])==11))) * \
(((nbJet == 0) * (1.-btagWeight_1tag_btagDeepBM_1c)) + ((nbJet > 0) * btagWeight_1tag_btagDeepBM_1c))"
"""
weight = "35.9 * 1.007 * baseW*genWeight*puWeight*customTriggerSF*((abs(Lepton_pdgId[0])==13)+(Lepton_RecoSF[0]*(abs(Lepton_pdgId[0])==11)))*((abs(Lepton_pdgId[1])==13)+(Lepton_RecoSF[1]*(abs(Lepton_pdgId[1])==11)))*Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[0]*Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[1]*Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[0]*Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[1]*(((nbJet == 0) * (1.-btagWeight_1tag_btagDeepBM_1c)) + ((nbJet > 0) * btagWeight_1tag_btagDeepBM_1c))*PrefireWeight*Flag_goodVertices*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter*Flag_globalSuperTightHalo2016Filter"

if applyTriggers:
    for index, cut in enumerate(cuts):
        cuts[index] = cut + " && (Trigger_ElMu || Trigger_dblMu || Trigger_sngMu || Trigger_dblEl || Trigger_sngEl)"
        #cuts[index] = cut + " && (Trigger_dblEl)"

#Open the files needed
if myTrees:
    print("Be careful! My trees with the skimming have been selected.")
    baseDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/"

    inputDir = {}
    inputDir["data2016"] = baseDir + "Run2016_102X_nAODv6_Full2016v6loose/DATASusy2016v6__hadd__susyMT2recoNomin/" 
    inputDir["data2017"] = baseDir + "Run2017_102X_nAODv6_Full2017v6loose/DATASusy2017v6__hadd__susyMT2recoNomin/" 
    inputDir["data2018"] = baseDir + "Run2018_102X_nAODv6_Full2018v6loose/DATASusy2018v6__hadd__susyMT2recoNomin/" 
    inputDir["MC2016"] = baseDir + "Summer16_102X_nAODv6_Full2016v6loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyNomin2016v6loose__susyMT2recoNomin/" 
    inputDir["MC2017"] = baseDir + "Fall2017_102X_nAODv6_Full2017v6loose/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyNomin2017v6loose__susyMT2recoNomin/"
    inputDir["MC2018"] = baseDir + "Autumn18_102X_nAODv6_Full2018v6loose/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyNomin2018v6loose__susyMT2recoNomin/"
    inputDir["signal2016"] = baseDir + "Summer16_102X_nAODv7_Full2016v7loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyNomin2016v6loose__susyMT2recoNomin/"
    inputDir["signal2017"] = baseDir + "Fall2017_102X_nAODv7_Full2017v7/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyNomin2017v6loose__susyMT2recoNomin/"
    inputDir["signal2018"] = baseDir + "Autumn18_102X_nAODv7_Full2018v7/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyNomin2018v6loose__susyMT2recoNomin/"

else:
    print("The trees without the skimming have been selected.")

    inputDir = {}
    inputDir["data2016"] = "/eos/cms/store/user/scodella/SUSY/Nano/Run2016_102X_nAODv6_Full2016v6loose/DATASusy2016v6__hadd__susyMT2recoNomin/"
    inputDir["data2017"] = "/eos/cms/store/caf/user/scodella/BTV/Nano/Run2017_102X_nAODv6_Full2017v6loose/DATASusy2017v6__hadd__susyMT2recoNomin/" 
    inputDir["data2018"] = "/eos/user/s/scodella/SUSY/Nano/Run2018_102X_nAODv6_Full2018v6loose/DATASusy2018v6__hadd__susyMT2recoNomin/"
    inputDir["MC2016"] = "/eos/cms/store/user/scodella/SUSY/Nano/Summer16_102X_nAODv6_Full2016v6loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyNomin2016v6loose__susyMT2recoNomin/"
    inputDir["MC2017"] = "/eos/cms/store/caf/user/scodella/BTV/Nano/Fall2017_102X_nAODv6_Full2017v6loose/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyNomin2017v6loose__susyMT2recoNomin/"
    inputDir["MC2018"] = "/eos/user/s/scodella/SUSY/Nano/Autumn18_102X_nAODv6_Full2018v6loose/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyNomin2018v6loose__susyMT2recoNomin/"
    inputDir["signal2016"] = "/eos/user/c/cprieels/work/JonatanEOS/Summer16_102X_nAODv7_Full2016v7loose/MCSusy2016v6loose__MCSusyCorr2016v6loose__MCSusyNomin2016v6loose__susyMT2recoNomin/"
    inputDir["signal2017"] = "/eos/user/c/cprieels/work/JonatanEOS/Fall2017_102X_nAODv7_Full2017v7/MCSusy2017v6loose__MCSusyCorr2017v6loose__MCSusyNomin2017v6loose__susyMT2recoNomin/"
    inputDir["signal2018"] = "/eos/user/c/cprieels/work/JonatanEOS/Autumn18_102X_nAODv7_Full2018v7/MCSusy2018v6loose__MCSusyCorr2018v6loose__MCSusyNomin2018v6loose__susyMT2recoNomin/"

chain = r.TChain("Events")
filesToProcess = glob.glob(inputDir[category] + "nanoLatino_*" + query + "*.root")
if len(filesToProcess) == 0:
    print("No files found.")
    exit()
else:
    print(str(len(filesToProcess)) + " file(s) matching the query have been found.")

for fileToProcess in filesToProcess:
    #print(fileToProcess)
    chain.AddFile(fileToProcess)

#Compute the number of entries
for channel in channels:
    print("\n============================= CHANNEL " + channel + " =============================\n")
    if channel == "ee":
        baseCutsWithChannel = baseCuts + " && Lepton_pdgId[0]*Lepton_pdgId[1] == -121 && Lepton_isTightElectron_cutBasedMediumPOG[0] > 0.5 && Lepton_isTightElectron_cutBasedMediumPOG[1] > 0.5"
    elif channel == "df":
        baseCutsWithChannel = baseCuts + " && Lepton_pdgId[0]*Lepton_pdgId[1] == -143 && ((Lepton_isTightElectron_cutBasedMediumPOG[0] > 0.5 && Lepton_isTightMuon_mediumRelIsoTight[1] > 0.5) || (Lepton_isTightMuon_mediumRelIsoTight[0] > 0.5 && Lepton_isTightElectron_cutBasedMediumPOG[1] > 0.5))"
    elif channel == "mm":
        baseCutsWithChannel = baseCuts + " && Lepton_pdgId[0]*Lepton_pdgId[1] == -169 && Lepton_isTightMuon_mediumRelIsoTight[0] > 0.5 && Lepton_isTightMuon_mediumRelIsoTight[1] > 0.5"
    elif channel == "ll":
        baseCutsWithChannel = baseCuts + " && ((Lepton_isTightElectron_cutBasedMediumPOG[0] > 0.5 && Lepton_isTightElectron_cutBasedMediumPOG[1] > 0.5) || (Lepton_isTightMuon_mediumRelIsoTight[0] > 0.5 && Lepton_isTightMuon_mediumRelIsoTight[1] > 0.5) || (Lepton_isTightElectron_cutBasedMediumPOG[0] > 0.5 && Lepton_isTightMuon_mediumRelIsoTight[1] > 0.5) || (Lepton_isTightMuon_mediumRelIsoTight[0] > 0.5 && Lepton_isTightElectron_cutBasedMediumPOG[1] > 0.5))"
    else:
        print("Channel not found.")
        exit()

    for c, cut in enumerate(cuts):
        print("For cut " + cut.replace("Sum$(CleanJet_pt >= 20. && abs(CleanJet_eta) < 2.4)", "nJet").replace("(Trigger_ElMu || Trigger_dblMu || Trigger_sngMu || Trigger_dblEl || Trigger_sngEl)", "Triggers").replace(ECALRegion0, "ECALRegion0").replace(ECALRegion1, "EcalRegion1").replace("Flag_goodVertices*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter", "METFilters") + ", " + str(chain.GetEntries(baseCutsWithChannel + " && " + cut)) + " entries have been found.")

        #if(weight != "1" and weight != "1."):
        hist = r.TH1F("hist_" + str(c), "", 1, -10000, 1000000)
        print("("  + cut + ") * (" + weight + ")")
        chain.Draw("mt2ll >> " + "hist_" + str(c), "(" + baseCutsWithChannel + " && " + cut + ") * (" + weight + ")")
        print(str(hist.Integral(-1, -1)) + " weighted entries have been observed.\n")

"""
# ========================================
# Write to file
maxEntries = 1000
luminosityBlocks = []
events = []
index = 0
for ev in chain:
    if ev.Lepton_pt[0] < 25. or ev.Lepton_pt[1] < 20. or ev.mll < 20. or (ev.Lepton_pdgId[0] * ev.Lepton_pdgId[1]) > 0:# or ev.Lepton_pdgId[0]*ev.Lepton_pdgId[1] != -121 or ev.Lepton_isTightElectron_cutBasedMediumPOG[0] < 0.5 or ev.Lepton_isTightElectron_cutBasedMediumPOG[1] < 0.5:
        continue
    if abs(ev.Lepton_pdgId[0]) == 11 and ev.Lepton_isTightElectron_cutBasedMediumPOG[0] < 0.5:
        continue
    if abs(ev.Lepton_pdgId[0]) == 13 and ev.Lepton_isTightMuon_mediumRelIsoTight[0] < 0.5:
        continue
    if abs(ev.Lepton_pdgId[1]) == 11 and ev.Lepton_isTightElectron_cutBasedMediumPOG[1] < 0.5:
        continue
    if abs(ev.Lepton_pdgId[1]) == 13 and ev.Lepton_isTightMuon_mediumRelIsoTight[1] < 0.5:
        continue

    #if not ev.Trigger_ElMu and not ev.Trigger_dblMu and not ev.Trigger_sngMu and not ev.Trigger_dblEl and not ev.Trigger_sngEl:
    #    continue

    #if not ev.Trigger_dblEl:
    if ev.Trigger_ElMu or ev.Trigger_dblMu or ev.Trigger_sngMu or not ev.Trigger_dblEl or ev.Trigger_sngEl:
        continue

    if ev.mll > 76 and ev.mll < 106:
        continue

    if ev.CleanJet_pt[0] < 30. or abs(ev.CleanJet_eta[0]) > 2.4:
        continue

    if ev.nbJet < 1:
        continue

    #ECAL transition region
    if (abs(ev.Lepton_pdgId[0]) == 11):
        if (ev.Lepton_eta[0] + ev.Electron_deltaEtaSC[ev.Lepton_electronIdx[0]]) > -1.566 and (ev.Lepton_eta[0] + ev.Electron_deltaEtaSC[ev.Lepton_electronIdx[0]]) < -1.444:
            continue
        if (ev.Lepton_eta[0] + ev.Electron_deltaEtaSC[ev.Lepton_electronIdx[0]]) > 1.444 and (ev.Lepton_eta[0] + ev.Electron_deltaEtaSC[ev.Lepton_electronIdx[0]]) < 1.566:
            continue

    if (abs(ev.Lepton_pdgId[1]) == 11):
        if (ev.Lepton_eta[1] + ev.Electron_deltaEtaSC[ev.Lepton_electronIdx[1]]) > -1.566 and (ev.Lepton_eta[1] + ev.Electron_deltaEtaSC[ev.Lepton_electronIdx[1]]) < -1.444:
            continue
        if (ev.Lepton_eta[1] + ev.Electron_deltaEtaSC[ev.Lepton_electronIdx[1]]) > 1.444 and (ev.Lepton_eta[1] + ev.Electron_deltaEtaSC[ev.Lepton_electronIdx[1]]) < 1.566:
            continue

    if ev.mt2ll < 80.:
        continue
    if ev.nJet < 1:
        continue
    if ev.nbJet < 1:
        continue
    if ev.Lepton_pdgId[0] * ev.Lepton_pdgId[1] != -169 and ev.mll > 76 and ev.mll < 106:
        continue

    index += 1
    if index > maxEntries and maxEntries > 0:
        break

    luminosityBlocks.append(str(ev.luminosityBlock).replace("L", ""))
    events.append(str(ev.event).replace("L", ""))

with open('luminosityBlocks.txt', 'w') as f:
    for luminosityBlock in luminosityBlocks:
        f.write("%s\n" % luminosityBlock)

with open('events.txt', 'w') as f:
    for event in events:
        f.write("%s\n" % event)

# ========================================
# Read from file

f = open("dominic.txt", "r")
lines = f.readlines()
dominicEvents = []
for line in lines:
    try:
        line = line.replace("\n", "")
        dominicEvents.append(line)
    except Exception as e:
        print("Not an integer.\n")

print("\n\n===================================== MISSING EVENTS =====================================\n")
missingEvents = list(set(dominicEvents) - set(events))
print("Number of missing events: ", str(len(missingEvents)))
print("Missing events: ", missingEvents)
"""
