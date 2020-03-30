import ROOT
from ROOT import TMVA, TFile, TTree, TCanvas, TCut, TChain, TMath, TH1F, TLorentzVector
from subprocess import call
from os.path import isfile
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.regularizers import l2
from keras.optimizers import SGD, RMSprop
from keras.utils import plot_model
import optparse
import os, fnmatch

# ===========================================
# Arguments to be updated
# ===========================================

#DESY variables
thetal0 = "TMath::Cos(2*TMath::ATan(exp(-Lepton_eta[0])))"
thetal1 = "TMath::Cos(2*TMath::ATan(exp(-Lepton_eta[1])))"
thetab = "TMath::Cos(2*TMath::ATan(exp(-CleanJet_eta[bJetsIdx[0]])))"
thetab2 = "TMath::Cos(2*TMath::ATan(exp(-CleanJet_eta[bJetsIdx[1]])))"
thetal0l1 = thetal0 + "*" + thetal1
thetal0b = thetal0 + "*" + thetab
thetal1b = thetal1 + "*" + thetab

#IFCA variables
totalET = "PuppiMET_sumEt + Lepton_pt[0] + Lepton_pt[1] + CleanJet_p[0]t + CleanJet_pt[1]"

variables = ["PuppiMET_pt", "mT2", "dphill", "dphillmet", "Lepton_pt[0]", "Lepton_pt[1]", "mll", "nJet", "nbJet", "mtw1", "mtw2", "mth", "Lepton_eta[0]-Lepton_eta[1]", "Lepton_phi[0]-Lepton_phi[1]", "thetal0l1 := "+thetal0l1, "thetal0b := "+thetal0b, "thetal1b := "+thetal1b, "totalET :="+totalET, "dark_pt", "overlapping_factor"]
#variables = ["PuppiMET_pt", "mT2", "dphill", "dphillmet", "Lepton0_pt", "Lepton1_pt", "mll", "njet", "nbjet", "mtw1", "mtw2", "mth", "Lepton0_eta-Lepton1_eta", "Lepton0_phi-Lepton1_phi", "thetal0l1 := "+thetal0l1, "thetal0b := "+thetal0b, "thetal1b := "+thetal1b, "totalET :="+totalET]

#baseDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer16_102X_nAODv4_Full2016v5/MCl1loose2016v5__MCCorr2016v5__l2loose__l2tightOR2016v5/"
baseDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"

# ===========================================
# Argument parser
# ===========================================
parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
parser.add_option('-s', '--signal', action='store', type=str, dest='signal', default='pseudoscalar_LO_Mchi_1_Mphi_100', help='Name of the signal file to be used')
parser.add_option('-b', '--background', action='store', type=str, dest='background', default='TTTo2L2Nu__part', help='Name of the background file samples can be found')
(opts, args) = parser.parse_args()

signal     = opts.signal
background = opts.background
    
# ===========================================
# Setup TMVA
# ===========================================
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()
#output = TFile.Open('TMVA_'+signal+'.root', 'RECREATE')
output = TFile.Open('TMVA.root', 'RECREATE')
factory = TMVA.Factory('TMVAClassification', output, '!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')

# ===========================================
# Load data
# ===========================================
dataloader = TMVA.DataLoader('dataset')
for variable in variables:
    dataloader.AddVariable(variable)

#We typically have several signal background files (*__part*), so let's read them in a loop
listOfFiles = os.listdir(baseDir)
signalPattern = "*"+signal+"*.root"
signalChain = TChain("Events")
backgroundPattern = "*"+background+"*.root"
backgroundChain = TChain("Events")
for index, entry in enumerate(listOfFiles):
    if fnmatch.fnmatch(entry, signalPattern):
        signalChain.AddFile(baseDir+entry)
    if fnmatch.fnmatch(entry, backgroundPattern):
        backgroundChain.AddFile(baseDir+entry)

canvas = TCanvas("canvas")
canvas.cd()

backgroundChain.Draw("Lepton_pt[1]")
signalTree = signalChain #We can actually feed directly a Tchain to TMVA, no need to get the tree
dataloader.AddSignalTree(signalTree)
backgroundTree = backgroundChain
dataloader.AddBackgroundTree(backgroundTree)

#Define the training and testing samples
nSignal = signalChain.GetEntries()
nBackground = backgroundChain.GetEntries()

nTrain_Signal = str(int(nSignal/100*10)) #10% for now
nTrain_Background = str(int(nBackground/100*10))
nTest_Signal = str(int(nSignal/100*5))
nTest_Background = str(int(nBackground/100*5))

dataloader.PrepareTrainingAndTestTree(TCut(''), 'nTrain_Signal='+nTrain_Signal+':nTrain_Background='+nTrain_Background+':nTest_Signal='+nTest_Signal+':nTest_Background='+nTest_Background+':SplitMode=Block:NormMode=NumEvents:!V')

# ===========================================
# Generate model
# ===========================================
model = Sequential()
model.add(Dense(20, activation='relu', input_dim=len(variables)))
model.add(Dropout(0.2))
model.add(Dense(20, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(20, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(20, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(2, activation='softmax'))

# Set loss and optimizer
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy', 'mse'])

#Move to the correct directory to save the model and its weights
outputDirectory = "training/"
try:
    os.stat(outputDirectory)
except:
    os.makedirs(outputDirectory)

# Store model
#plot_model(model, to_file=outputDirectory+'model.png')
model.save(outputDirectory+'model.h5')
model.summary() #Print the summary of the model compiled

# Book method
factory.BookMethod(dataloader, TMVA.Types.kBDT, 'BDT', 'NTrees=100:MaxDepth=10:AdaBoostBeta=0.5:!H:!V')
factory.BookMethod(dataloader, TMVA.Types.kFisher, 'Fisher', '!H:!V:Fisher')
factory.BookMethod(dataloader, TMVA.Types.kPyKeras, 'PyKeras', 'H:!V:FilenameModel='+outputDirectory+'model.h5:NumEpochs=30:BatchSize=64:TriesEarlyStopping=5')
factory.BookMethod(dataloader, TMVA.Types.kLikelihood, 'LikelihoodD', '!H:!V:!TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmooth=5:NAvEvtPerBin=50')

# ===========================================
# Run training, test and evaluation
# ===========================================

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
