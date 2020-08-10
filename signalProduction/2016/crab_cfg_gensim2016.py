from WMCore.Configuration import Configuration
import os

config = Configuration()

## General options for the client
config.section_("General")
config.General.requestName   = 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000_RunIISummer16_GENSIM_PrivateFullProd'
config.General.workArea = 'crab_output'

## Specific option of the job type
## these options are directly readable from the job type plugin
config.section_("JobType")
config.JobType.pluginName  = 'PrivateMC'
config.JobType.psetName    = 'gensim2016.py'
config.JobType.inputFiles = ['/afs/cern.ch/work/d/dpinna/public/forCedric/DMScalar_top_tWChan_Mchi1_Mphi1000_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz']

## Specific data options
config.section_("Data")
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 2000
config.Data.totalUnits = 400000
config.Data.outputPrimaryDataset = 'CRAB_PrivateMC'
config.Data.publication = True

#config.Data.inputDataset = '/TTbarDMJets_Dilepton_scalar_LO_TuneCP5_13TeV-madgraph-mcatnlo-pythia8/RunIIAutumn18MiniAOD-rp_102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
config.Data.outputDatasetTag   = 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000_RunIISummer16_GENSIM_PrivateFullProd'

config.Data.publication     = True
config.Data.outLFNDirBase = '/store/user/cprieels/'

config.section_("Site")
config.Site.storageSite = 'T2_ES_IFCA'
#config.Site.storageSite = 'T2_CH_CERN'
