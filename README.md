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

Set of scripts able to perform the top reconstruction, compute new variables on top of the latino trees and run a BDT/DNN in order to enhance the signal background discrimination.
These scripts need to be run within CMSSW_10_4_0 or higher to have access to keras.

First, the createTrees.py script needs to be run in order to read the latino rootfiles, to skim them, select variables and perform the top reconstruction.
The top reconstruction is based on the one performed in https://github.com/alantero/ttbarDM.
This process has been setup to be used with condor, thanks to createJobs.py. The job of this script is to read all the latino files matching some criterias in order to create a .sh file for each file we want to process with createTrees.py. The arguments taken are, among others:
- **a**: whether you want to create a .sh for ALL the files found or just one for testing purposes
- **s**: whether the files to be processed are signals or not
- **d**: whether the files to be processes are data or MC files
- **t**: the search term to be found in the correct directory (eg, TTT02L2Nu__part can be used to process only TTbar MC files).
Once the .sh files created, then can be launched using the command condor_submit condorjob.tcl.

For the smearing involved in the ttbar reconstruction process, several histograms need to be generated first of all using the generateDistributions.py script.

Then, the MVA can be run on these previously produced files using simply the following command.
      python dnn.py
A signal and a background files can be given as arguments to this script.

## Scripts

Set of additional scripts.

### plotSignals
Small script able to plot one variable for all the signals mass points available in a single canvas.

### createjobsScalar/createjobsPseudoScalar
Two scripts allowing to divide a randomized parameters file into its different mass points.