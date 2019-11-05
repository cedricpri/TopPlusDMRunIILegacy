from ROOT import TMVA, TFile, TTree, TCut
from subprocess import call
from os.path import isfile
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.regularizers import l2
from keras.optimizers import SGD, RMSprop
import optparse

# ===========================================
# Arguments to be updated
# ===========================================

variables = ["PuppiMET_pt", "MET_pt", "TkMET_pt", "mT2", "dphill", "dphillmet", "Lepton_pt[0]", "Lepton_pt[1]", "Lepton_eta[0]", "Lepton_eta[1]", "Lepton_phi[0]", "Lepton_phi[1]", "mll", "njet", "mtw1", "mtw2"]

# ===========================================
# Argument parser
# ===========================================
parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
parser.add_option('-s', '--signal', action='store', type=str, dest='signal', default='nanoLatino_DMScalar_ttbar01j_Mchi1_Mphi100_Private2019.root', help='Name of the signal file to be used')
parser.add_option('-b', '--background', action='store', type=str, dest='background', default='nanoLatino_TTTo2L2Nu__part0.root', help='Name of the background file samples can be found')
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
                       '!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=Classification')

# ===========================================
# Load data
# ===========================================
if not isfile(background) or not isfile(signal):
    print("At least one of the input file has not been found!")
    exit()

signalFile = TFile.Open(signal)
signalTree = signalFile.Get('Events')
backgroundFile = TFile.Open(background)
backgroundTree = backgroundFile.Get('Events')

dataloader = TMVA.DataLoader('dataset')

for variable in variables:
    dataloader.AddVariable(variable)

dataloader.AddSignalTree(signalTree, 1.0)
dataloader.AddBackgroundTree(backgroundTree, 1.0)
dataloader.PrepareTrainingAndTestTree(TCut(''),
                                      'nTrain_Signal=1000:nTrain_Background=100000:SplitMode=Random:NormMode=NumEvents:!V')

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

# Book methods
factory.BookMethod(dataloader, TMVA.Types.kFisher, 'Fisher',
                   '!H:!V:Fisher:VarTransform=D,G')
factory.BookMethod(dataloader, TMVA.Types.kPyKeras, 'PyKeras',
                   'H:!V:VarTransform=D,G:FilenameModel=model.h5:NumEpochs=20:BatchSize=32')
factory.BookMethod(dataloader, TMVA.Types.kLikelihood, 'LikelihoodD',
                     '!H:!V:!TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmooth=5:NAvEvtPerBin=50:VarTransform=Decorrelate')

# ===========================================
# Run training, test and evaluation
# ===========================================

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
