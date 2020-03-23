
universe                = vanilla
executable              = $(filename)
output                  = /afs/cern.ch/user/c/cprieels/work/public/TopPlusDMRunIILegacy/CMSSW_10_4_0/src/neuralNetwork/log/$(ClusterId).$(ProcId).out
error                   = /afs/cern.ch/user/c/cprieels/work/public/TopPlusDMRunIILegacy/CMSSW_10_4_0/src/neuralNetwork/log/$(ClusterId).$(ProcId).err
log                     = /afs/cern.ch/user/c/cprieels/work/public/TopPlusDMRunIILegacy/CMSSW_10_4_0/src/neuralNetwork/log/$(ClusterId).log
+JobFlavour = "tomorrow" 
queue filename matching (sh/send_*sh)
