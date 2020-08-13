# t/tt+DM dileptonic Run II legacy analysis (IFCA)

## SignalProduction

Scripts used in order to read a gridpack and produce private 2016, 2017 and 2018 nanoAODv6 single top + DM signal samples.

### Step 0 (GEN-SIM)
First, the GENSIM can be produced by running the gensim<YEAR>.py file, either locally or by using CRAB and the crab_cfg_gensim<YEAR>.py. This process needs to be done using CMSSW_7_1_43 (for 2016), CMSSW_9_3_15_patch3 (2017) CMSSW_10_2_16_patch1 (2018). The correct CMSSW_X_Y_Z release can be downloaded using the following command (unless said otherwise, we assume you should be using a slc6 architecture):

     #!/bin/bash
     export SCRAM_ARCH=<ARCHITECTURE>
     source /cvmfs/cms.cern.ch/cmsset_default.sh
     if [ -r CMSSW_X_Y_Z/src ] ; then 
     	echo release CMSSW_X_Y_Z already exists
     else
	scram p CMSSW CMSSW_X_Y_Z
     fi
     cd CMSSW_X_Y_Z/src
     eval `scram runtime -sh`
     scram b

For 2016, it is necessary to run the following command after doing the cmsenv to remove the CRIC error that usually shows up:

    source /cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/curl/7.59.0/etc/profile.d/init.sh

On one hand, to run the code locally, for testing purposes, simply switch (comment/uncomment) the gridpack path in the gensim<YEAR>.py file in order to select the gridpack with the /afs/<PATH> path instead of /srv/<PATH> and then run ```cmsRun gensim<YEAR>.py```.

On the other hand, to run the code on CRAB, the correct gridpack name needs to be entered both in the configuration and in the gensim<YEAR>.py file (in order to use CRAB, the global path /srv/ needs to be used or the script won't be able to find the gridpack), and the /afs/ path needs to be entered in the CRAB config file.

Finally, the fragment.py file also needs to be copied within the Configuration/GenProduction/python folder within the CMSSW directory, and ```scram b``` needs to be run afterwards. 

### Step 1 (Premix)
Then, the Premix can be produced by running the premix<YEAR>.py file, using CRAB and the crab_cfg_premix<YEAR>.py. The correct path of the output file produced for the first step should be entered in the crab_cfg_premix<YEAR>.py before proceeding.

This step needs to be executed using CMSSW_8_0_31 (2016), CMSSW_9_4_7 (2017) or CMSSW_10_2_5 (2018).

### Step 2 (AOD)
Then, the AOD can be produced by running the aodsim<YEAR>.py file, using CRAB and the crab_cfg_aodsim<YEAR>.py. The correct path of the output file produced for the previous step should be entered in the crab_cfg_premix<YEAR>.py before proceeding.
This needs to be done using CMSSW_10_2_5 (2018).

### Step 3 (MiniAOD)
Then, the MiniAOD can be produced by running the miniaod<YEAR>.py file, using CRAB and the crab_cfg_miniaod<YEAR>.py. The correct path of the output file produced for the previous step should be entered in the crab_cfg_premix<YEAR>.py before proceeding.

This needs to be done using CMSSW_10_2_5 (2018).

### Step 4 (NanoAODv6)
Finally, the NanoAODv6 can be produced by running the nanoaod<YEAR>.py file, using CRAB and the crab_cfg_nanoaod<YEAR>.py. The correct path of the output file produced for the previous step should be entered in the crab_cfg_premix<YEAR>.py before proceeding.

This needs to be done using CMSSW_10_2_18 (2018).

