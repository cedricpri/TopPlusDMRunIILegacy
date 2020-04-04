import ROOT
from subprocess import call
from os.path import isfile
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.regularizers import l2
from keras.optimizers import SGD, RMSprop
from keras.utils import plot_model
import optparse, os, fnmatch, sys
from array import array

# ===========================================
# Arguments to be updated
# ===========================================

#Training variables
variables = ["PuppiMET_pt", "mt2ll", "mt2bl", "totalET", "dphill", "dphillmet", "Lepton_pt[0]", "Lepton_pt[1]", "mll", "nJet", "nbJet", "mtw1", "mtw2", "mth", "Lepton_eta[0]", "Lepton_eta[1]", "Lepton_phi[0]", "Lepton_phi[1]", "thetall", "thetal1b1", "thetal2b2", "dark_pt", "overlapping_factor", "reco_weight"]

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
# TRAINING
#=========================================================================================================
def trainMVA(inputDir, signalFiles, backgroundFiles):
    """
    Function used to train the MVA based on the signal given
    """

    #output = TFile.Open('TMVA_'+signal+'.root', 'RECREATE')
    output = ROOT.TFile.Open('TMVA.root', 'RECREATE')

    # ===========================================
    # Setup TMVA
    # ===========================================
    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()
    factory = ROOT.TMVA.Factory('TMVAClassification', output, '!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')

    # ===========================================
    # Load data
    # ===========================================
    dataloader = ROOT.TMVA.DataLoader('dataset')
    for variable in variables:
        dataloader.AddVariable(variable)
        
    #We passa as arguments the lists containing all the files to process, let's put them in a chain
    signalChain = ROOT.TChain("Events")
    for signalFile in signalFiles:
        signalChain.AddFile(inputDir+signalFile)

    backgroundChain = ROOT.TChain("Events")
    for backgroundFile in backgroundFiles:
        backgroundChain.AddFile(inputDir+backgroundFile)

    canvas = ROOT.TCanvas("canvas")
    canvas.cd()
                
    #backgroundChain.Draw("Lepton_pt[1]")
    dataloader.AddSignalTree(signalChain)
    dataloader.AddBackgroundTree(backgroundChain)

    #Define the training and testing samples
    nSignal = signalChain.GetEntries()
    nBackground = backgroundChain.GetEntries()

    nTrain_Signal = str(int(nSignal/100*10)) #10% for now
    nTrain_Background = str(int(nBackground/100*10))
    nTest_Signal = str(int(nSignal/100*5))
    nTest_Background = str(int(nBackground/100*5))

    dataloader.PrepareTrainingAndTestTree(ROOT.TCut(''), 'nTrain_Signal='+nTrain_Signal+':nTrain_Background='+nTrain_Background+':nTest_Signal='+nTest_Signal+':nTest_Background='+nTest_Background+':SplitMode=Block:NormMode=NumEvents:!V')

    # ===========================================
    # Generate keras model
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
    factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, 'BDT', 'NTrees=100:MaxDepth=10:AdaBoostBeta=0.5:!H:!V')
    factory.BookMethod(dataloader, ROOT.TMVA.Types.kFisher, 'Fisher', '!H:!V:Fisher')
    factory.BookMethod(dataloader, ROOT.TMVA.Types.kPyKeras, 'PyKeras', 'H:!V:FilenameModel='+outputDirectory+'model.h5:NumEpochs=30:BatchSize=64:TriesEarlyStopping=5')
    factory.BookMethod(dataloader, ROOT.TMVA.Types.kLikelihood, 'LikelihoodD', '!H:!V:!TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmooth=5:NAvEvtPerBin=50')

    # ===========================================
    # Run training, test and evaluation
    # ===========================================
    
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

#=========================================================================================================
# APPLICATION
#=========================================================================================================
def evaluateMVA(inputDir, filename, test):
    """
    Function used to evaluate the MVA after being trained
    """

    # ===========================================
    # Setup TMVA
    # ===========================================
    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()

    reader = ROOT.TMVA.Reader("Color:!Silent")
    for variable in variables:
        reader.AddVariable(variable, array('f',[0.]))

    reader.BookMVA("BDT", "dataset/weights/TMVAClassification_BDT.weights.xml")
    reader.BookMVA("Fisher", "dataset/weights/TMVAClassification_Fisher.weights.xml")
    reader.BookMVA("PyKeras", "dataset/weights/TMVAClassification_PyKeras.weights.xml")
    reader.BookMVA("LikelihoodD", "dataset/weights/TMVAClassification_LikelihoodD.weights.xml")

    #Write the new branches in the tree
    rootfile = ROOT.TFile.Open(inputDir+filename, "UPDATE")
    inputTree = rootfile.Get("Events")

    BDT_output = array("f", [0.])
    inputTree.Branch("BDT_output", BDT_output, "BDT_output/F")
    Fisher_output = array("f", [0.])
    inputTree.Branch("Fisher_output", Fisher_output, "Fisher_output/F")
    PyKeras_output = array("f", [0.])
    inputTree.Branch("PyKeras_output", PyKeras_output, "PyKeras_output/F")
    LikelihoodD_output = array("f", [0.])
    inputTree.Branch("LikelihoodD_output", LikelihoodD_output, "LikelihoodD_output/F")

    nEvents = rootfile.Events.GetEntries()
    if test:
        nmEvents = 1000

    for index, ev in enumerate(rootfile.Events):
        
        if index % 100 == 0: #Update the loading bar every 100 events
            updateProgress(round(index/float(nEvents), 2))
    
        #For testing only
        if test and index == nEvents:
            break

        BDTValue = reader.EvaluateMVA("BDT")
        BDT_output[0] = BDTValue
        FisherValue = reader.EvaluateMVA("Fisher")
        Fisher_output[0] = FisherValue
        PyKerasValue = reader.EvaluateMVA("PyKeras")
        PyKeras_output[0] = PyKerasValue
        LikelihoodDValue = reader.EvaluateMVA("LikelihoodD")
        LikelihoodD_output[0] = LikelihoodDValue

        inputTree.Fill()

    inputTree.Write()
    rootfile.Close()
        
    
if __name__ == "__main__":

    # ===========================================
    # Argument parser
    # ===========================================
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-s', '--signalFiles', action='store', type=str, dest='signalFiles', default=[], help='Name of the signal files to be used to train the MVA')
    parser.add_option('-b', '--backgroundFiles', action='store', type=str, dest='backgroundFiles', default=[], help='Name of the background files samples to train the MVA')
    parser.add_option('-f', '--filename', action='store', type=str, dest='filename', default='', help='Name of the file to be evaluated')
    parser.add_option('-d', '--inputDir', action='store', type=str, dest='inputDir', default="")
    parser.add_option('-e', '--evaluate', action='store_true', dest='evaluate') #Evaluate the MVA or train it?
    parser.add_option('-t', '--test', action='store_true', dest='test') #Only run on a single file
    (opts, args) = parser.parse_args()
    
    signalFiles     = opts.signalFiles
    backgroundFiles = opts.backgroundFiles
    filename = opts.filename
    inputDir = opts.inputDir
    evaluate = opts.evaluate
    test = opts.test

    #To evaluate the MVA, we pass as argument one file name each time, to parallelize the jobs
    if(evaluate):
        evaluateMVA(inputDir, filename, test)
    else: #To train, we need to pass a list containing all the files at once
        #Split the comaseparated string for the files into lists
        signalFiles = [str(item) for item in signalFiles.split(',')]
        backgroundFiles = [str(item) for item in backgroundFiles.split(',')]
        
        trainMVA(inputDir, signalFiles, backgroundFiles)
