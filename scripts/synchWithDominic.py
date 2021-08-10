import glob
import ROOT as r

ECALRegion0 = "(abs(Lepton_pdgId[0]) != 11 || (Lepton_eta[0] < -1.566 || (Lepton_eta[0] > -1.444 && Lepton_eta[0] < 1.444) || Lepton_eta[0] > 1.566))"
ECALRegion1 = "(abs(Lepton_pdgId[1]) != 11 || (Lepton_eta[1] < -1.566 || (Lepton_eta[1] > -1.444 && Lepton_eta[1] < 1.444) || Lepton_eta[1] > 1.566))"
METFilters = "Flag_goodVertices*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter"

#Main parameters
#query = "DMscalar_Dilepton_top_tWChan_Mchi1_Mphi100_"
query = "TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_100_"
category = "signal2016"
baseCuts = "Lepton_pt[0] > 25. && Lepton_pt[1] > 20. && mll > 20. && abs(Lepton_eta[0]) < 2.4 && abs(Lepton_eta[1]) < 2.4 && Lepton_pdgId[0] * Lepton_pdgId[1] < 0"
cuts = ["1", ECALRegion0 + " && " + ECALRegion1, "Sum$(CleanJet_pt >= 20. && abs(CleanJet_eta) < 2.4) >= 1", METFilters, ECALRegion0 + " && " + ECALRegion1 + " && ((Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) || (mll < 76 || mll > 106)) && Sum$(CleanJet_pt >= 20. && abs(CleanJet_eta) < 2.4) >= 1 && nbJet >= 1 && mt2ll > 80."]#, ECALRegion0 + " && " + ECALRegion1 + " && Sum$(CleanJet_pt >= 20. && abs(CleanJet_eta) < 2.4) >= 1 && mt2ll > 80. && nbJet >= 1 && ((Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) || (mll < 76 || mll > 106))"]
channels = ["ll", "ee", "df", "mm"]
weights = ["1"]
myTrees = True
applyTriggers = False

if applyTriggers:
    for index, cut in enumerate(cuts):
        cuts[index] = cut + " && (Trigger_ElMu || Trigger_dblMu || Trigger_sngMu || Trigger_dblEl || Trigger_sngEl)"

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

    for cut in cuts:
        print("For cut " + cut.replace("Sum$(CleanJet_pt >= 20. && abs(CleanJet_eta) < 2.4)", "nJet").replace("(Trigger_ElMu || Trigger_dblMu || Trigger_sngMu || Trigger_dblEl || Trigger_sngEl)", "Triggers").replace("(abs(Lepton_pdgId[0]) != 11 || (Lepton_eta[0] < -1.566 || (Lepton_eta[0] > -1.444 && Lepton_eta[0] < 1.444) || Lepton_eta[0] > 1.566))", "ECALRegion0").replace("(abs(Lepton_pdgId[1]) != 11 || (Lepton_eta[1] < -1.566 || (Lepton_eta[1] > -1.444 && Lepton_eta[1] < 1.444) || Lepton_eta[1] > 1.566))", "EcalRegion1").replace("Flag_goodVertices*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter", "METFilters") + ", " + str(chain.GetEntries(baseCutsWithChannel + " && " + cut)) + " entries have been found.")

# ========================================
# Write to file

maxEntries = 1000
luminosityBlocks = []
events = []
mt2ll = []
index = 0
for ev in chain:
    if ev.Lepton_pt[0] < 25. or ev.Lepton_pt[1] < 20. or abs(ev.Lepton_eta[0]) > 2.4 or abs(ev.Lepton_eta[1]) > 2.4 or ev.mll < 20. or (ev.Lepton_pdgId[0] * ev.Lepton_pdgId[1]) > 0:# or ev.Lepton_pdgId[0]*ev.Lepton_pdgId[1] != -121 or ev.Lepton_isTightElectron_cutBasedMediumPOG[0] < 0.5 or ev.Lepton_isTightElectron_cutBasedMediumPOG[1] < 0.5:
        continue
    if abs(ev.Lepton_pdgId[0]) == 11 and ev.Lepton_isTightElectron_cutBasedMediumPOG[0] < 0.5:
        continue
    if abs(ev.Lepton_pdgId[0]) == 13 and ev.Lepton_isTightMuon_mediumRelIsoTight[0] < 0.5:
        continue
    if abs(ev.Lepton_pdgId[1]) == 11 and ev.Lepton_isTightElectron_cutBasedMediumPOG[1] < 0.5:
        continue
    if abs(ev.Lepton_pdgId[1]) == 13 and ev.Lepton_isTightMuon_mediumRelIsoTight[1] < 0.5:
        continue

    index += 1
    if index > maxEntries and maxEntries > 0:
        break

    luminosityBlocks.append(str(ev.luminosityBlock).replace("L", ""))
    events.append(str(ev.event).replace("L", ""))
    mt2ll.append(str(ev.mt2ll).replace("L", ""))

with open('luminosityBlocks.txt', 'w') as f:
    for luminosityBlock in luminosityBlocks:
        f.write("%s\n" % luminosityBlock)

with open('events.txt', 'w') as f:
    for event in events:
        f.write("%s\n" % event)

with open('mt2ll.txt', 'w') as f:
    for mt2 in mt2ll:
        f.write("%s\n" % mt2)

"""
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
