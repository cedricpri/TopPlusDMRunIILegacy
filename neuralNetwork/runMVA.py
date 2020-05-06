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
variables = ["PuppiMET_pt", "MET_significance", "mt2ll", "mt2bl", "dphillmet", "Lepton_pt[0]", "Lepton_pt[1]", "Lepton_eta[0]", "Lepton_eta[1]", "dark_pt", "overlapping_factor", "reco_weight", "cosphill", "nbJet", "mll"] 

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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def splitByProcess(inputFiles, background = False):
    processes = [] #List of dictionnaries with the different processes as keys and a list of files as values
    
    for inputFile in inputFiles:
        #process = "_".join(inputFile.split("_")[1:5]) #TODO: try to find a better way to estimate the process?
        start = "nanoLatino_"
        end = "__part"
        process = inputFile[inputFile.find(start)+len(start):inputFile.rfind(end)].replace('_ext', '')

        #However, at least for now, let's group all the background processes
        if background:
            process = 'backgrounds'
        #if 'ST' in process: process = 'ST'

        alreadyFound = [i for i, d in enumerate(processes) if process in d.keys()]
        if len(alreadyFound) == 0:
            processes.append({process: [inputFile]})
        else:
            processes[alreadyFound[0]][process].append(inputFile)

    return processes

#=========================================================================================================
# TRAINING
#=========================================================================================================
def trainMVA(baseDir, inputDir, year, backgroundFiles, signalFiles):
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
    # Load data
    # ===========================================
    os.chdir(outputDirWeights)
    dataloader = ROOT.TMVA.DataLoader('dataset')
    for variable in variables:
        dataloader.AddVariable(variable)
        
    #Let's know try to find out how many signal and background processes have been passed as argument
    signalProcesses = splitByProcess(signalFiles, False)
    backgroundProcesses = splitByProcess(backgroundFiles, True)

    print(bcolors.WARNING + "\n --> I found " + str(len(signalProcesses)) + " signal processes and " + str(len(backgroundProcesses)) + " background processes.")
    print("Please check if these numbers seem to be correct! \n" + bcolors.ENDC)

    #canvas = ROOT.TCanvas("canvas")
    #canvas.cd()

    #Now add all the files to the corresponding processes in the dataloader and define the testing and training subsets
    numberSignals = len(signalProcesses)
    numberProcesses = len(signalProcesses) + len(backgroundProcesses)
    minEntries = 999999999 #Used to have exactly the same number of events for each process toa void biases

    for index in range(len(signalProcesses)):

        signalFiles = signalProcesses[index].values()[0]
        signalChain = ROOT.TChain("Events")

        for signalFile in signalFiles:
            signalChain.AddFile(inputDir+signalFile)
        if signalChain.GetEntries() < minEntries: 
            minEntries = signalChain.GetEntries()

        dataloader.AddTree(signalChain, 'Signal' + str(index))

    for index in range(len(backgroundProcesses)):

        backgroundFiles = backgroundProcesses[index].values()[0]
        backgroundChain = ROOT.TChain("Events")

        for backgroundFile in backgroundFiles:
            backgroundChain.AddFile(inputDir+backgroundFile)
        if backgroundChain.GetEntries() < minEntries: 
            minEntries = backgroundChain.GetEntries()

        dataloader.AddTree(backgroundChain, 'Background' + str(index))

    # ===========================================
    # TMVA setup
    # ===========================================

    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()
    if numberSignals > 1:
        factory = ROOT.TMVA.Factory('TMVAClassification', output, '!V:!Silent:Color:DrawProgressBar:AnalysisType=multiclass')
    else:
        factory = ROOT.TMVA.Factory('TMVAClassification', output, '!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')

    dataloaderOptions = ''
    for i, signalProcess in enumerate(signalProcesses):
        dataloaderOptions = dataloaderOptions + ':nTrain_Signal' + str(i) + '=' + str(int(minEntries/2)) + ':nTest_Signal' + str(i) + '=' + str(int(minEntries/2)) #TOCHECK: for now, we consider a 50%/50% splitting
    for i, backgroundProcess in enumerate(backgroundProcesses):
        dataloaderOptions = dataloaderOptions + ':nTrain_Background' + str(i) + '=' + str(int(minEntries/2)) + ':nTest_Background' + str(i) + '=' + str(int(minEntries/2)) #TOCHECK: for now, we consider a 50%/50% splitting
    dataloader.PrepareTrainingAndTestTree(ROOT.TCut(''), dataloaderOptions + ':SplitMode=Block:NormMode=NumEvents:!V')

    # ===========================================
    # Generate keras model
    # ===========================================
    model = Sequential()
    model.add(Dense(15, activation='relu', input_dim=len(variables)))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(5, activation='relu'))
    model.add(Dense(numberProcesses, activation='softmax'))

    # Set loss and optimizer
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy', 'mse'])

    # Store model
    #plot_model(model, to_file=outputDir+'model.png')
    model.save(outputDirTraining+'model.h5')
    model.summary() #Print the summary of the model compiled

    # Book method
    #factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, 'BDT', 'NTrees=300:BoostType=Grad:Shrinkage=0.2:MaxDepth=4:ncuts=1000000:MinNodeSize=1%:!H:!V')
    #factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, 'BDT', 'NTrees=300:BoostType=Grad:Shrinkage=0.2:MaxDepth=4:ncuts=10000:MinNodeSize=1%:!H:!V')
    factory.BookMethod(dataloader, ROOT.TMVA.Types.kPyKeras, 'PyKeras', 'H:!V:FilenameModel=' + outputDirTraining + 'model.h5:FilenameTrainedModel=' + outputDirTraining + 'modelTrained.h5:NumEpochs=200:BatchSize=250:VarTransform=N')

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
            
        trainMVA(baseDir, inputDir, year, backgroundFiles, signalFiles)
