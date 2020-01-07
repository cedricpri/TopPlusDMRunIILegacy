import ROOT
from ROOT import TMVA, TFile, TTree, TCanvas, TCut, TChain, TMath, TH1F, TLorentzVector
from subprocess import call
from os.path import isfile
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.regularizers import l2
from keras.optimizers import SGD, RMSprop
import optparse
import os, fnmatch

# ===========================================
# Arguments to be updated
# ===========================================

#DESY variables
thetal0 = "TMath::Cos(2*TMath::ATan(exp(-Lepton0_eta)))"
thetal1 = "TMath::Cos(2*TMath::ATan(exp(-Lepton1_eta)))"
thetab = "TMath::Cos(2*TMath::ATan(exp(-CleanbJet0_eta)))"
thetab2 = "TMath::Cos(2*TMath::ATan(exp(-CleanbJet1_eta)))"
thetal0l1 = thetal0 + "*" + thetal1
thetal0b = thetal0 + "*" + thetab
thetal1b = thetal1 + "*" + thetab

#IFCA variables
totalET = "PuppiMET_sumEt + Lepton0_pt + Lepton1_pt + CleanJet0_pt + CleanJet1_pt"

variables = ["PuppiMET_pt", "mT2", "dphill", "dphillmet", "Lepton0_pt", "Lepton1_pt", "mll", "njet", "nbjet", "mtw1", "mtw2", "mth", "Lepton0_eta-Lepton1_eta", "Lepton0_phi-Lepton1_phi", "thetal0l1 := "+thetal0l1, "thetal0b := "+thetal0b, "thetal1b := "+thetal1b, "totalET :="+totalET]
#baseDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer16_102X_nAODv4_Full2016v5/MCl1loose2016v5__MCCorr2016v5__l2loose__l2tightOR2016v5/"
baseDir = os.getcwd() + "/rootfiles/"

# ===========================================
# Argument parser
# ===========================================
parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
parser.add_option('-s', '--signal', action='store', type=str, dest='signal', default=baseDir+'nanoLatino_DMScalar_ttbar01j_Mchi1_Mphi100_Private2019_dnn.root', help='Name of the signal file to be used')
parser.add_option('-b', '--background', action='store', type=str, dest='background', default=baseDir+'nanoLatino_TTTo2L2Nu__part0_dnn.root', help='Name of the background file samples can be found')
(opts, args) = parser.parse_args()

signal     = opts.signal
background = opts.background
    
# ===========================================
# Setup TMVA
# ===========================================
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()
output = TFile.Open('TMVA.root', 'RECREATE')

factory = TMVA.Factory('TMVAClassification', output,
                       '!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')

# ===========================================
# Load data
# ===========================================
if not isfile(background) or not isfile(signal):
    print("At least one of the input file has not been found!")
    exit()

dataloader = TMVA.DataLoader('dataset')
for variable in variables:
    dataloader.AddVariable(variable)

#For now, we assume there is only one signal file
signalFile = TFile.Open(signal)
signalTree = signalFile.Get('Events')
dataloader.AddSignalTree(signalTree, 1.0)

#However we have several background files, so let's read them in a loop
listOfFiles = os.listdir(baseDir)
pattern = "*TTTo2L2Nu*.root"
chain = TChain("Events")
for index, entry in enumerate(listOfFiles):
    if fnmatch.fnmatch(entry, pattern):
        chain.AddFile(baseDir+entry)

canvas = TCanvas("canvas")
canvas.cd()

chain.Draw("Lepton_pt[1]")
backgroundTree = chain.GetTree()
dataloader.AddBackgroundTree(backgroundTree, 1.0)

dataloader.PrepareTrainingAndTestTree(TCut(''),
                                      'nTrain_Signal=2000:nTrain_Background=2000:nTest_Signal=2000:nTest_Background=2000:SplitMode=Random:NormMode=NumEvents:!V')

# ===========================================
# Generate model
# ===========================================
model = Sequential()
model.add(Dense(10, activation='relu', input_dim=len(variables)))
model.add(Dense(10, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(2, activation='softmax'))

# Set loss and optimizer
model.compile(loss='categorical_crossentropy', 
              optimizer=RMSprop(), metrics=['accuracy', 'mse'])

# Store model to file
model.save('model.h5')
model.summary()

# Book method
factory.BookMethod(dataloader, TMVA.Types.kBDT, 'BDT',
                   '!H:!V')
#factory.BookMethod(dataloader, TMVA.Types.kFisher, 'Fisher',
#                   '!H:!V:Fisher')
factory.BookMethod(dataloader, TMVA.Types.kPyKeras, 'PyKeras',
                   'H:!V:FilenameModel=model.h5:NumEpochs=20:BatchSize=32')
factory.BookMethod(dataloader, TMVA.Types.kLikelihood, 'LikelihoodD',
                   '!H:!V:!TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmooth=5:NAvEvtPerBin=50')

# ===========================================
# Run training, test and evaluation
# ===========================================

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
