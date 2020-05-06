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
#variables = ["PuppiMET_pt", "mt2ll", "totalET", "dphill", "dphillmet", "Lepton_pt[0]", "Lepton_pt[1]", "mll", "nJet", "nbJet", "mtw1", "mtw2", "mth", "Lepton_eta[0]", "Lepton_eta[1]", "Lepton_phi[0]", "Lepton_phi[1]", "thetall", "thetal1b1", "thetal2b2", "dark_pt", "overlapping_factor", "reco_weight"] #cosphill missing, mt2bl as well
variables = ["PuppiMET_pt", "MET_significance", "mt2ll", "mt2bl", "dphillmet", "Lepton_eta[0]-Lepton_eta[1]", "dark_pt", "overlapping_factor", "reco_weight", "cosphill", "nbJet", "mll"] 

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
def trainMVA(baseDir, inputDir, year, backgroundFiles, signalFiles, numberSignals):
    """
    Function used to train the MVA based on the signal given
    """

    massPoint = signalFiles[0].split("_")[3:9]
    massPoint = "_".join(massPoint).replace(".root", "")

    #Move to the correct directory to save the model and its weights
    outputDirTraining = baseDir + "/" + str(year) + "/" + massPoint + "/training/"
    outputDirWeights = baseDir + "/" + str(year) + "/" + massPoint
    try:
        os.stat(outputDirTraining)
    except:
        os.makedirs(outputDirTraining)
    output = ROOT.TFile.Open(outputDirTraining+'TMVA.root', 'RECREATE')

    try:
        os.stat(outputDirWeights)
    except:
        os.makedirs(outputDirWeights)

    # ===========================================
    # Setup TMVA
    # ===========================================
    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()
    factory = ROOT.TMVA.Factory('TMVAClassification', output, '!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')

    # ===========================================
    # Load data
    # ===========================================
    os.chdir(outputDirWeights)
    dataloader = ROOT.TMVA.DataLoader('dataset')
    for variable in variables:
        dataloader.AddVariable(variable)
        
    #We pass as arguments the lists containing all the files to process, let's put them in a chain, depending on their category
    if numberSignals == 1:
        signalChain = ROOT.TChain("Events")
        for signalFile in signalFiles:
            signalChain.AddFile(inputDir+signalFile)

        dataloader.AddTree(signalChain, 'Signal')

    elif numberSignals == 2: #If we have more than one signal, things a bit more complicated and require some work to separate the list into the different processes

        signalChain = ROOT.TChain("Events")
        signalChain1 = ROOT.TChain("Events")
        signalChain2 = ROOT.TChain("Events")
        processesConsidered = []

        for signalFile in signalFiles:

            process = "_".join(signalFile.split("_")[1:4])
            if process not in processesConsidered:
                processesConsidered.append(process)

            if process == processesConsidered[0]:
                signalChain1.AddFile(inputDir+signalFile)
            else:
                signalChain2.AddFile(inputDir+signalFile)
            signalChain.AddFile(inputDir+signalFile)
            
        print("\n --> I found the following signal process categories: ")
        print(' '.join(processesConsidered))
        print("Please check if it seems to be correct. \n")

        dataloader.AddTree(signalChain1, 'Signal_1')
        dataloader.AddTree(signalChain2, 'Signal_2')

    else:
        print("Currently not working for more than two signals")
        exit

    backgroundChain = ROOT.TChain("Events")
    for backgroundFile in backgroundFiles:
        backgroundChain.AddFile(inputDir+backgroundFile)

    canvas = ROOT.TCanvas("canvas")
    canvas.cd()
                
    dataloader.AddTree(backgroundChain, 'Background')

    #Define the training and testing samples
    nSignal = signalChain.GetEntries()
    nBackground = backgroundChain.GetEntries()

    nTrain_Signal = str(int(nSignal/100*50)) #10% for now
    nTrain_Background = str(int(nBackground/100*50))
    nTest_Signal = str(int(nSignal/100*50))
    nTest_Background = str(int(nBackground/100*50))

    dataloader.PrepareTrainingAndTestTree(ROOT.TCut(''), 'nTrain_Signal='+nTrain_Signal+':nTrain_Background='+nTrain_Background+':nTest_Signal='+nTest_Signal+':nTest_Background='+nTest_Background+':SplitMode=Block:NormMode=NumEvents:!V')

    # ===========================================
    # Generate keras model
    # ===========================================
    model = Sequential()
    model.add(Dense(10, activation='relu', input_dim=len(variables)))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(5, activation='relu'))
    model.add(Dense(numberSignals+1, activation='softmax'))

    # Set loss and optimizer
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy', 'mse'])

    # Store model
    #plot_model(model, to_file=outputDir+'model.png')
    model.save(outputDirTraining+'model.h5')
    model.summary() #Print the summary of the model compiled

    # Book method
    #factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, 'BDT', 'NTrees=300:BoostType=Grad:Shrinkage=0.2:MaxDepth=4:ncuts=1000000:MinNodeSize=1%:!H:!V')
    #factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, 'BDT', 'NTrees=300:BoostType=Grad:Shrinkage=0.2:MaxDepth=4:ncuts=10000:MinNodeSize=1%:!H:!V')
    factory.BookMethod(dataloader, ROOT.TMVA.Types.kPyKeras, 'PyKeras', 'H:!V:FilenameModel=' + outputDirTraining + 'model.h5:FilenameTrainedModel=' + outputDirTraining + 'modelTrained.h5:NumEpochs=120:BatchSize=500:VarTransform=N')

    # ===========================================
    # Run training, test and evaluation
    # ===========================================
    
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

#=========================================================================================================
# APPLICATION
#=========================================================================================================
def evaluateMVA(baseDir, inputDir, filename, massPoints, year, test):
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
        
    #Write the new branches in the tree
    rootfile = ROOT.TFile.Open(inputDir+filename, "UPDATE")
    inputTree = rootfile.Get("Events")

    for massPoint in massPoints:

        weightsDir = baseDir + "/" + str(year) + "/" + massPoint

        reader.BookMVA("BDT", weightsDir + "/dataset/weights/TMVAClassification_BDT.weights.xml")
        #reader.BookMVA("Fisher", weightsDir + "/dataset/weights/TMVAClassification_Fisher.weights.xml")
        reader.BookMVA("PyKeras", weightsDir + "/dataset/weights/TMVAClassification_PyKeras.weights.xml")
        #reader.BookMVA("LikelihoodD", weightsDir + "/dataset/weights/TMVAClassification_LikelihoodD.weights.xml")

        BDT_output = array("f", [0.])
        inputTree.Branch("BDT_output", BDT_output, "BDT_output/F")
        #Fisher_output = array("f", [0.])
        #inputTree.Branch("Fisher_output", Fisher_output, "Fisher_output/F")
        PyKeras_output = array("f", [0.])
        inputTree.Branch("PyKeras_output", PyKeras_output, "PyKeras_output/F")
        #LikelihoodD_output = array("f", [0.])
        #inputTree.Branch("LikelihoodD_output", LikelihoodD_output, "LikelihoodD_output/F")

        nEvents = rootfile.Events.GetEntries()
        if test:
            nEvents = 1000

        for index, ev in enumerate(rootfile.Events):
        
            if index % 100 == 0: #Update the loading bar every 100 events
                updateProgress(round(index/float(nEvents), 2))
    
            #For testing only
            if test and index == nEvents:
                break

            BDTValue = reader.EvaluateMVA("BDT")
            BDT_output[0] = BDTValue
            #FisherValue = reader.EvaluateMVA("Fisher")
            #Fisher_output[0] = FisherValue
            PyKerasValue = reader.EvaluateMVA("PyKeras")
            PyKeras_output[0] = PyKerasValue
            #LikelihoodDValue = reader.EvaluateMVA("LikelihoodD")
            #LikelihoodD_output[0] = LikelihoodDValue

            inputTree.Fill()

    inputTree.Write()
    rootfile.Close()
        
    
if __name__ == "__main__":

    # ===========================================
    # Argument parser
    # ===========================================
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-n', '--numberSignals', action='store', type=int, dest='numberSignals', default=[], help='Number of signal processes to consider for classification')
    parser.add_option('-s', '--signalFiles', action='store', type=str, dest='signalFiles', default=[], help='Name of the signal files to be used to train the MVA')
    parser.add_option('-b', '--backgroundFiles', action='store', type=str, dest='backgroundFiles', default=[], help='Name of the background files samples to train the MVA')
    parser.add_option('-f', '--filename', action='store', type=str, dest='filename', default='', help='Name of the file to be evaluated')
    parser.add_option('-i', '--inputDir', action='store', type=str, dest='inputDir', default="") 
    parser.add_option('-d', '--baseDir', action='store', type=str, dest='baseDir', default="/afs/cern.ch/user/c/cprieels/work/public/TopPlusDMRunIILegacy/CMSSW_10_4_0/src/neuralNetwork/")
    parser.add_option('-m', '--massPoints', action='store', type=str, dest='massPoints', default="scalar_LO_Mchi_1_Mphi_100")
    parser.add_option('-y', '--year', action='store', type=int, dest='year', default=2018)
    parser.add_option('-e', '--evaluate', action='store_true', dest='evaluate') #Evaluate the MVA or train it?
    parser.add_option('-t', '--test', action='store_true', dest='test') #Only run on a single file
    (opts, args) = parser.parse_args()

    numberSignals = opts.numberSignals
    signalFiles     = opts.signalFiles
    backgroundFiles = opts.backgroundFiles
    filename = opts.filename
    inputDir = opts.inputDir
    baseDir = opts.baseDir
    massPoints= opts.massPoints
    year = opts.year
    evaluate = opts.evaluate
    test = opts.test

    #To evaluate the MVA, we pass as argument one file name each time, to parallelize the jobs
    if(evaluate):
        #The mass points to be added to the trees are also passed as comma separated values
        massPointsList = [str(item) for item in massPoints.split(",")]

        evaluateMVA(baseDir, inputDir, filename, massPointsList, year, test)

    else: #To train, we need to pass a list containing all the files at once

        #Split the comma separated string for the files into lists
        signalFiles = [str(item) for item in signalFiles.split(',')]
        backgroundFiles = [str(item) for item in backgroundFiles.split(',')]
            
        trainMVA(baseDir, inputDir, year, backgroundFiles, signalFiles, numberSignals)
