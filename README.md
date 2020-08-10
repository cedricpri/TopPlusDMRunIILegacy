# t/tt+DM dileptonic Run II legacy analysis (IFCA)

## SignalProduction

Scripts used in order to read a gridpack and produce private 2016, 2017 and 2018 nanoAODv6 single top + DM signal samples.

### Step 0 (GEN-SIM)
First, the GENSIM can be produced by running the gensim<YEAR>.py file, using CRAB and the crab_cfg_gensim<YEAR>.py.
This needs to be done using CMSSW_7_1_43/lxplus6 (for 2016), CMSSW_9_3_15_patch3/lxplus6 (2017) CMSSW_10_2_16_patch1 (2018). 

For CRAB to work properly, at this stage, the gridpack name needs to be entered both in the configuration and in the gensim<YEAR>.py file. The fragment also needs to be copied within the Configuration/GenProduction/python folder within the CMSSW directory, and scram b needs to be run afterwards. Additionnally, for 2016, it is necessary to run the following command after doing the cmsenv:

    source /cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/curl/7.59.0/etc/profile.d/init.sh

### Step 1 (Premix)
Then, the Premix can be produced by running the premix<YEAR>.py file, using CRAB and the crab_cfg_premix<YEAR>.py.
This needs to be done using CMSSW_10_2_5 (2018).

### Step 2 (AOD)
Then, the AOD can be produced by running the aodsim<YEAR>.py file, using CRAB and the crab_cfg_aodsim<YEAR>.py.
This needs to be done using CMSSW_10_2_5 (2018).

### Step 3 (MiniAOD)
Then, the MiniAOD can be produced by running the miniaod<YEAR>.py file, using CRAB and the crab_cfg_miniaod<YEAR>.py.
This needs to be done using CMSSW_10_2_5 (2018).

### Step 4 (NanoAODv6)
Finally, the NanoAODv6 can be produced by running the nanoaod<YEAR>.py file, using CRAB and the crab_cfg_nanoaod<YEAR>.py.
This needs to be done using CMSSW_10_2_18/lxplus6 (2018).

## NeuralNetwork

Set of scripts able to perform the top reconstruction, compute new variables on top of the latino trees and run a BDT/DNN in order to enhance the signal/background discrimination.
These scripts need to be run within CMSSW_10_4_0 or higher to have access to keras.

### generateDistributions.py

The script generates the distributions needed to perform the smearing of the top reconstruction (such as the breit-weigner distribution of the W and the angular correction factor for leptons and jets).
If the distributions.root is downlaoded from Github, this step can be skipped as the information is already available.

### createTrees.py

This script performs several different steps at once:
- Its main goal is to read Latino nanoAODv6 files in order to create the equivalent of minitrees, by applying a global skimming, selecting ttbar-like events.
- It also performs the analytical top reconstruction method described in [arXiv: 1305.1878] (https://github.com/alantero/ttbarDM), with or without smearing, depending on the boolean value at the top of the script
- The best lepton/bjet combination is selected as the combination having the highest reco_weight value and smallest invariant mass.
- Finally, it also computes additional variables, such as the dark pt or 2016 DESY spin correlated variables.

This process has been setup to be used with condor, thanks to createJobsTrees.py. 
The job of this script is to read all the latino files matching some criterias in order to create a .sh file for each file we want to process with createTrees.py. The arguments taken are, among others:
- **t**: whether you want to create a .sh for just one file for testing purposes or all the files found
- **s**: whether the files to be processed are signals or not
- **d**: whether the files to be processes are data or MC files
- **q**: the search term to be found in the correct directory (eg, TTT02L2Nu__part can be used to process only TTbar MC files).
- **r**: resubmit option, that will find files which crashed and allow to relaunch them directly.
Once the .sh files created, then can be launched using the command condor_submit condorjob.tcl.
Several additional arguments need to be set up correctly if the user launching the command is not cprieels (such as the input, output and base directory definition).

###

Then, the MVA can be run on these previously produced files using a similar process, and the runMVA.py script.
Both the createJobsTrainMVA.py and createJobsEvaluateMVA.py can be used in order to also generate .sh files and run this script on condor.
The first script generate a single job to train the MVA, while the other generates one job per file in order to apply the variables calculated previously.
This script can now be run on one or two signals, and many different backgrounds at once, passing them as argument as a comma separated string.

## Scripts

Set of additional scripts.

### plotSignals
Small script able to plot one variable for all the signals mass points available in a single canvas.

### createjobsScalar/createjobsPseudoScalar
Two scripts allowing to divide a randomized parameters file into its different mass points.