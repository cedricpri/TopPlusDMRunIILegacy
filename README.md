# t/tt+DM dileptonic Run II legacy analysis (IFCA)

## SignalProduction

Scripts used in order to read a gridpack and produce a nanoAODv6 file.

### Step 0 (GEN-SIM)
First, the GENSIM can be produced by running the gensim.py file, using CRAB and the crab_cfg_gensim.py.
This needs to be done using CMSSW_10_2_16_patch1. For some reason, at this stage, the gridpack name needs to be entered both in the configurationa and in the gensim.py file.

### Step 1 (Premix)
Then, the Premix can be produced by running the premix.py file, using CRAB and the crab_cfg_premix.py.
This needs to be done using CMSSW_10_2_5.

### Step 2 (AOD)
Then, the AOD can be produced by running the aodsim.py file, using CRAB and the crab_cfg_aodsim.py.
This needs to be done using CMSSW_10_2_5.

### Step 3 (MiniAOD)
Then, the MiniAOD can be produced by running the miniaod.py file, using CRAB and the crab_cfg_miniaod.py.
This needs to be done using CMSSW_10_2_5.

### Step 4 (NanoAODv6)
Finally, the NanoAODv6 can be produced by running the nanoaod.py file, using CRAB and the crab_cfg_nanoaod.py.
This needs to be done using CMSSW_10_2_18 and lxplus6.

## NeuralNetwork

Set of scripts able to run a BDT/DNN in order to enhance the signal background discrimination.
These scripts need to be run within CMSSW_10_4_0 or higher to have access to keras.

First, the getReady.py needs to be run in order to read the latino rootfiles, to skim them, select variables and perform the top reconstruction.
       python getReady.py <filename>
This will create a folder called rootfiles in which a new file <filename>_dnn.root will be created.

Then, the MVA can be run using simply the following command.
      python dnn.py
A signal and a background files can be given as argument to this script.

## Scripts

Set of additional scripts.

### plotSignals
Small script able to plot one variable for all the signals available in a single canvas.

### createjobsScalar/createjobsPseudoScalar
Two scripts allowing to divide a randomized parameters file into its different mass points.