import ROOT
from subprocess import call
from os.path import isfile

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.regularizers import l2
from keras.optimizers import SGD, RMSprop, Adam
from keras.utils import plot_model
from keras.models import load_model

import optparse, os, fnmatch, sys
from array import array

# ===========================================
# Arguments to be updated
# ===========================================

#Training variables
#variables = ["METcorrected_pt", "mt2ll", "dphillmet", "nbJet", "mblt", "mt2bl", "massT", "reco_weight", "cosphill", "costhetall", "dark_pt", "overlapping_factor", "r2l", "r2l4j"]
variables = {}
variables["ST"] = ["METcorrected_pt", "mt2ll", "ptllb", "mllb"]
variables["TTbar"] = ["METcorrected_pt", "mt2ll", "ptllb", "mllb", "dark_pt", "chel"]

trainPercentage = 50
normalizeProcesses = False #Normalize all the processes to have the same input training events in each case

baseCut = "mt2ll > 80."
nJet = "Sum$(CleanJet_pt >= 20. && abs(CleanJet_eta) < 2.4)"
cuts ={}
cuts["ST"] = baseCut + " && (( " + nJet + " == 1) || ( " + nJet + " == 2 && nbJet == 1))"
cuts["TTbar"] = baseCut + " && (( " + nJet + " > 1) || ( " + nJet + " > 2 || nbJet > 1))"

#=========================================================================================================
# HELPERS
#=========================================================================================================
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Progress bar
def updateProgress(progress):
    barLength = 50 # Modify this to change the length of the progress bar
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

def splitByProcess(inputFiles, test = False, background = False):
    processes = [] #List of dictionnaries with the different processes as keys and a list of files as values
    
    for inputFile in inputFiles:
        #process = "_".join(inputFile.split("_")[1:5]) #TODO: try to find a better way to estimate the process name?
        start = "nanoLatino_"
        end = "__part"
        process = inputFile[inputFile.find(start)+len(start):inputFile.rfind(end)].replace('_ext', '')

        #However, at least for now, let's group all the background processes if the option is set
        if background:
            process = 'backgrounds'
        else:
            #if 'ST' in process: process = 'ST'
            process = "signals"

        alreadyFound = [i for i, d in enumerate(processes) if process in d.keys()]
        if len(alreadyFound) == 0:
            processes.append({process: [inputFile]})
        else:
            if not test or len(processes[alreadyFound[0]][process]) < 30:
                processes[alreadyFound[0]][process].append(inputFile)

    return processes

#=========================================================================================================
# TRAINING
#=========================================================================================================
def trainMVA(baseDir, inputDir, year, backgroundFiles, signalFiles, tag, singleTopRegion, test):
    """
    Function used to train the MVA based on the signal given
    """

    signalFiles = filter(None, signalFiles) #Filter possible empty values
    massPoint = signalFiles[-1].split("_")[10:16]
    if(tag != ""): massPoint = "_".join(massPoint).replace(".root", "") + "_" + tag
    else: massPoint = "_".join(massPoint).replace(".root", "")

    """
    if "DMscalar" in signalFiles[0]:
        massPoint = massPoint.replace("top_tWChan", "ST_scalar_LO").replace("__part0", "").replace("Mchi", "Mchi_").replace("Mphi", "Mphi_")
    elif "DMpseudoscalar" in signalFiles[0]:
        massPoint = massPoint.replace("top_tWChan", "ST_pseudoscalar_LO").replace("__part0", "").replace("Mchi", "Mchi_").replace("Mphi", "Mphi_")
    else:
        massPoint = "TTbar_" + massPoint
    """

    #Move to the correct directory to save the model and its weights
    outputDirTraining = baseDir + "/" + str(year) + "/" + massPoint + "/training/"
    outputDirWeights = baseDir + "/" + str(year) + "/" + massPoint
    try:
        os.stat(outputDirTraining)
    except:
        os.makedirs(outputDirTraining)
    output = ROOT.TFile.Open(outputDirTraining+'TMVA.root', 'UPDATE')

    outputDirWeights = outputDirWeights.replace(".root", "")
    try:
        os.stat(outputDirWeights)
    except:
        os.makedirs(outputDirWeights)

    # ===========================================
    # Load data
    # ===========================================
    os.chdir(outputDirWeights)
    dataloader = ROOT.TMVA.DataLoader('dataset')
    dataloader.SetWeightExpression("baseW")

    if singleTopRegion:
        regionString = "ST"
    else:
        regionString = "TTbar"

    for variable in variables[regionString]:
        dataloader.AddVariable(variable)
        
    #Let's know try to find out how many signal and background processes have been passed as argument
    signalProcesses = splitByProcess(signalFiles, test, False)
    backgroundProcesses = splitByProcess(backgroundFiles, test, True)

    print(bcolors.WARNING + "\n --> I found " + str(len(signalProcesses)) + " signal and " + str(len(backgroundProcesses)) + " background processes.")
    print("Please check if these numbers seem to be correct! \n" + bcolors.ENDC)

    #Now add all the files to the corresponding processes in the dataloader and define the testing and training subsets
    numberSignals = len(signalProcesses)
    numberProcesses = len(signalProcesses) + len(backgroundProcesses)

    signalEvents =[]
    backgroundEvents = []
    minEvents = 9999999999 #Used if required to have exactly the same number of events for each process to avoid biases

    for index in range(len(signalProcesses)):
        signalFiles = signalProcesses[index].values()[0]
        signalChain = ROOT.TChain("Events")

        for signalFile in signalFiles:
            signalChain.AddFile(inputDir+signalFile)

        signalEvents.append(signalChain.GetEntries(cuts[regionString]))
        #if signalChain.GetEntries(cuts[regionString]) < minEvents: 
        #    minEvents = signalChain.GetEntries(cuts[regionString])

        if numberSignals > 1:
            dataloader.AddTree(signalChain, 'Signal' + str(index))
        else:
            dataloader.AddSignalTree(signalChain)

    for index in range(len(backgroundProcesses)):
        backgroundFiles = backgroundProcesses[index].values()[0]
        backgroundChain = ROOT.TChain("Events")

        for backgroundFile in backgroundFiles:
            backgroundChain.AddFile(inputDir+backgroundFile)

        backgroundEvents.append(backgroundChain.GetEntries(cuts[regionString]))
        #if backgroundChain.GetEntries(cuts[regionString]) < minEvents: 
        #    minEvents = backgroundChain.GetEntries(cuts[regionString])

        #for event in openedFile.Events:
        #    baseW = event.baseW
        #    break

        if numberProcesses > 2:
            dataloader.AddTree(backgroundChain, 'Background' + str(index))
        else:
            dataloader.AddBackgroundTree(backgroundChain)

    # ===========================================
    # TMVA setup
    # ===========================================

    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()
    if numberSignals > 1:
        factory = ROOT.TMVA.Factory('TMVAClassification', output, '!V:!Silent:Color:DrawProgressBar:AnalysisType=multiclass')
    else:
        factory = ROOT.TMVA.Factory('TMVAClassification', output, '!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')

    testPercentage = 100 - trainPercentage

    dataloaderOptions = ''
    for i, signalProcess in enumerate(signalProcesses):
        if normalizeProcesses:
            numberEvents = minEvents
        else:
            numberEvents = signalEvents[i]

        if numberSignals > 1:
            dataloaderOptions = dataloaderOptions + ':nTrain_Signal' + str(i) + '=' + str(int(numberEvents*trainPercentage/100)) + ':nTest_Signal' + str(i) + '=' + str(int(numberEvents*testPercentage/100))
        else:
            dataloaderOptions = dataloaderOptions + ':nTrain_Signal' + '=' + str(int(numberEvents*trainPercentage/100)) + ':nTest_Signal' + '=' + str(int(numberEvents*testPercentage/100))

    for i, backgroundProcess in enumerate(backgroundProcesses):
        if not normalizeProcesses: 
            numberEvents = backgroundEvents[i]

        if(numberProcesses > 2):
            dataloaderOptions = dataloaderOptions + ':nTrain_Background' + str(i) + '=' + str(int(numberEvents*trainPercentage/100)) + ':nTest_Background' + str(i) + '=' + str(int(numberEvents*testPercentage/100))
        else:
            dataloaderOptions = dataloaderOptions + ':nTrain_Background' + '=' + str(int(numberEvents*trainPercentage/100)) + ':nTest_Background' + '=' + str(int(numberEvents*testPercentage/100))

    dataloader.PrepareTrainingAndTestTree(ROOT.TCut(cuts[regionString]), dataloaderOptions + ':SplitMode=Random:NormMode=NumEvents:!V')

    # ===========================================
    # Keras model
    # ===========================================
    model = Sequential()
    model.add(Dense(40, activation='relu', input_dim=len(variables[regionString])))
    model.add(Dense(40, activation='relu'))
    model.add(Dense(30, activation='relu'))
    model.add(Dense(numberProcesses, activation='softmax'))
    #model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='categorical_crossentropy', optimizer=Adam(0.005), metrics=['accuracy', 'mse'])
    #model.compile(loss='binary_crossentropy', optimizer=Adam(0.005), metrics=['accuracy', 'mse'])
    #plot_model(model, to_file=outputDirTraining+'trainingModel.png')
    model.save(outputDirTraining+'PyKeras.h5')
    model.summary()

    # Book method
    #factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, 'BDT', 'NTrees=500:BoostType=AdaBoost:AdaBoostBeta=0.3:SeparationType=CrossEntropy:MaxDepth=3:ncuts=20:MinNodeSize=2:!H:!V')
    #factory.BookMethod(dataloader, ROOT.TMVA.Types.kMLP, "MLP", "H:!V:NeuronType=sigmoid:NCycles=500:VarTransform=N:HiddenLayers=80,80,40:TestRate=5:LearningRate=0.01:EstimatorType=MSE");
    factory.BookMethod(dataloader, ROOT.TMVA.Types.kPyKeras, 'PyKeras', 'H:!V:FilenameModel=' + outputDirTraining + 'PyKeras.h5:FilenameTrainedModel=' + outputDirTraining + 'PyKerasTrained.h5:NumEpochs=30:BatchSize=100:VarTransform=N')

    # ===========================================
    # Run training, test and evaluation
    # ===========================================
    
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()


#=========================================================================================================
# APPLICATION
#=========================================================================================================
def evaluateMVA(baseDir, inputDir, filenames, weightsDir, year, evaluationBackgroundThreshold, test):
    """
    Function used to evaluate the MVA after being trained
    """
    # ===========================================
    # Setup TMVA
    # ===========================================
    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()

    #Write the new branches in a new tree
    try:
        os.makedirs(inputDir[:-1] + '_weighted/')
    except:
        pass

    #Check if the weighted tree already exists
    for filename in filenames:
        print(bcolors.WARNING + "\n \n \n Now evaluating the file " + str(filename) + bcolors.ENDC)

        outputDir = inputDir[:-1] + '_weighted/' + filename.split("__part")[0] + "/"
        try:
            os.stat(outputDir)
        except:
            os.makedirs(outputDir)

        #Check if the weighted tree already exists
        inputFile = ROOT.TFile.Open(inputDir + filename, "READ")
        inputTree = inputFile.Get("Events")
        inputTree.SetBranchStatus("*", 1)

        outputFile = ROOT.TFile.Open(outputDir + filename, "RECREATE")
        outputTree = inputTree.CloneTree(0)
        #inputTree.SetBranchStatus("*", 0)
        #inputTree.SetBranchStatus("mt2ll", 1)
        #inputTree.SetBranchStatus("nbJet", 1)

        reader = {}
        branchesAddresses = {}
        """
        BDT_output_signal = {}
        BDT_output_background = {}
        BDT_output_category = {}
        """
        DNN_output_signal = {}
        DNN_output_background = {}
        DNN_output_category = {}

        for SR in ["ST", "TTbar", "Both"]:
            reader[SR] = {}
            branchesAddresses[SR] = {}
            """
            BDT_output_signal[SR] = {}
            BDT_output_background[SR] = {}
            BDT_output_category[SR] = {}
            """
            DNN_output_signal[SR] = {}
            DNN_output_background[SR] = {}
            DNN_output_category[SR] = {}

            for weightTag in weightsDir:
                branches = {}
                allBranchesAddresses = []
                branchesAddresses[SR][weightTag] = []

                if SR is not "Both":
                    reader[SR][weightTag] = ROOT.TMVA.Reader("Color:!Silent")
                
                    #Read the variables used for the training
                    weightsLocation = baseDir + "/" + str(year) + "/" + weightTag + "_" + SR
                    trainingFile = ROOT.TFile.Open(weightsLocation + "/training/TMVA.root", "READ")
                    trainingTree = trainingFile.Get("dataset/TrainTree")
                    trainingVariables = trainingTree.GetListOfBranches()
                
                    for variable in trainingVariables:
                        variableName = variable.GetName().replace("_0_", "[0]").replace("_1_", "[1]")
                        if variableName not in ["classID", "className", "weight", "BDT", "PyKeras"]:
                            branch = inputTree.GetBranch(variableName)
                            try:
                                branchName = branch.GetName()
                            except Exception as e:
                                branchName = variableName

                            branches[branchName] = array('f', [-999.0])
                            reader[SR][weightTag].AddVariable(branchName, branches[branchName])
                            branchesAddresses[SR][weightTag].append([branchName, branches[branchName]])
                            allBranchesAddresses.append([branchName, branches[branchName]])
                            inputTree.SetBranchStatus(branchName, 1)
                            #inputTree.SetBranchAddress(branchName, branches[branchName])
                            #outputTree.SetBranchAddress(branchName, branches[branchName])
                            
                    #reader[SR][weightTag].BookMVA("BDT", weightsLocation + "/dataset/weights/TMVAClassification_BDT.weights.xml")
                    reader[SR][weightTag].BookMVA("PyKeras", weightsLocation + "/dataset/weights/TMVAClassification_PyKeras.weights.xml")
                else:
                    for branchAddress in allBranchesAddresses:
                        branchesAddresses[SR][weightTag].append(branchAddress)

                """
                BDT_output_signal[SR][weightTag] = array("f", [0.])
                BDT_output_background[SR][weightTag] = array("f", [0.])
                BDT_output_category[SR][weightTag] = array("i", [0]) #Which category gets the highest output?
                outputTree.Branch(SR + "_BDT_output_signal_" + weightTag, BDT_output_signal[SR][weightTag], SR + "_BDT_output_signal_" + weightTag + "/F")
                outputTree.Branch(SR + "_BDT_output_background_" + weightTag, BDT_output_background[SR][weightTag], SR + "_BDT_output_background_" + weightTag + "/F")
                outputTree.Branch(SR + "_BDT_output_category_" + weightTag, BDT_output_category[SR][weightTag], SR + "_BDT_output_category_" + weightTag + "/I")
                """

                DNN_output_signal[SR][weightTag] = array("f", [0.])
                DNN_output_background[SR][weightTag] = array("f", [0.])
                DNN_output_category[SR][weightTag] = array("i", [0])
                outputTree.Branch(SR + "_DNN_output_signal_" + weightTag, DNN_output_signal[SR][weightTag], SR + "_DNN_output_signal_" + weightTag + "/F")
                outputTree.Branch(SR + "_DNN_output_background_" + weightTag, DNN_output_background[SR][weightTag], SR + "_DNN_output_background_" + weightTag + "/F")
                outputTree.Branch(SR + "_DNN_output_category_" + weightTag, DNN_output_category[SR][weightTag], SR + "_DNN_output_category_" + weightTag + "/I")

                trainingFile.Close()

        #Now we can apply the weights
        nEvents = inputTree.GetEntries("mt2ll > 80 && nbJet >= 1")
        if test:
            nEvents = min(nEvents, 1000)

        eventsPassed = 0
        for index, ev in enumerate(inputTree):
            #Skimming to reduce the size of the trees
            if ev.nbJet < 1 or ev.mt2ll < 80:
                continue

            eventsPassed = eventsPassed + 1
            if eventsPassed % 100 == 0 and nEvents != 0: #Update the loading bar every 100 events
                updateProgress(round(eventsPassed/float(nEvents), 2))

            #For testing only
            if test and index == nEvents:
                break

            #Let's get started
            for SR in ["ST", "TTbar", "Both"]:
                for weightTag in weightsDir:

                    for branch in branchesAddresses[SR][weightTag]:
                        inputTree.SetBranchAddress(branch[0], branch[1])
                    inputTree.GetEntry(index)

                    eventSR = SR #Which SR do we want to consider based on the observed event?
                    if SR == "Both":
                        nJet = 0
                        for j, jet in enumerate(ev.CleanJet_pt):
                            if ev.CleanJet_pt[j] >= 20 and abs(ev.CleanJet_eta[j]) < 2.4:
                                nJet = nJet + 1
                                
                        if nJet == 1 or (nJet == 2 and ev.nbJet == 1):
                            eventSR = "ST"
                        else:
                            eventSR = "TTbar"

                    #Fill the DNN variables
                    DNNValues = list(reader[eventSR][weightTag].EvaluateMulticlass("PyKeras"))
                    DNN_output_signal[SR][weightTag][0] = DNNValues[0]
                    DNN_output_background[SR][weightTag][0] = DNNValues[1]

                    if evaluationBackgroundThreshold > 0:
                        if DNN_output_background[SR][weightTag][0] > evaluationBackgroundThreshold:
                            DNN_output_category[SR][weightTag][0] = 1
                        else:
                            DNN_output_category[SR][weightTag][0] = 0
                    else:
                        DNN_output_category[SR][weightTag][0] = DNNValues.index(max(DNNValues))

            outputTree.Fill()

        outputFile.cd()
        outputTree.SetBranchStatus("*", 1)
        outputTree.Write()
        inputFile.Close()
        outputFile.Close()

if __name__ == "__main__":

    # ===========================================
    # Argument parser
    # ===========================================
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0', add_help_option=False)
    parser.add_option('-s', '--signalFiles', action='store', type=str, dest='signalFiles', default=[], help='Name of the signal files to be used to train the MVA')
    parser.add_option('-b', '--backgroundFiles', action='store', type=str, dest='backgroundFiles', default=[], help='Name of the background files samples to train the MVA')
    parser.add_option('-f', '--filenames', action='store', type=str, dest='filenames', default=[], help='Name of the file to be evaluated')
    parser.add_option('-i', '--inputDir', action='store', type=str, dest='inputDir', default="") 
    parser.add_option('-d', '--baseDir', action='store', type=str, dest='baseDir', default="/afs/cern.ch/user/c/cprieels/work/public/TopPlusDMRunIILegacy/CMSSW_10_4_0/src/neuralNetwork/")
    parser.add_option('-w', '--weightsDir', action='store', type=str, dest='weightsDir', default="scalar_LO_Mchi_1_Mphi_100_default")
    parser.add_option('-y', '--year', action='store', type=int, dest='year', default=2018)
    parser.add_option('-g', '--tags', action='store', type=str, dest='tags', default="")
    parser.add_option('-r', '--singleTopRegion', action='store_true', dest='singleTopRegion', default=False)
    parser.add_option('-h', '--threshold', action='store', type=float, dest='threshold', default=1.0)
    parser.add_option('-e', '--evaluate', action='store_true', dest='evaluate') #Evaluate the MVA or train it?
    parser.add_option('-t', '--test', action='store_true', dest='test') #Only run on a single file
    (opts, args) = parser.parse_args()

    signalFiles     = opts.signalFiles
    backgroundFiles = opts.backgroundFiles
    filenames = opts.filenames
    inputDir = opts.inputDir
    baseDir = opts.baseDir
    weightsDir= opts.weightsDir
    year = opts.year
    tags = opts.tags
    singleTopRegion = opts.singleTopRegion
    threshold = opts.threshold
    evaluate = opts.evaluate
    test = opts.test

    #To evaluate the MVA, we pass as argument one file name each time, to parallelize the jobs
    if(evaluate):

        #The mass points to be added to the trees are also passed as comma separated values
        filenames = [str(item) for item in filenames.split(",")]
        weightsList = [str(item) for item in weightsDir.split(",")]
        evaluateMVA(baseDir, inputDir, filenames, weightsList, year, threshold, test)

    else: #To train, we need to pass a list containing all the files at once

        #Split the comma separated string for the files into lists
        signalFiles = [str(item) for item in signalFiles.split(',')]
        backgroundFiles = [str(item) for item in backgroundFiles.split(',')]            
        trainMVA(baseDir, inputDir, year, backgroundFiles, signalFiles, tags, singleTopRegion, test)
