from WMCore.Configuration import Configuration
import os

config = Configuration()

## General options for the client
config.section_("General")
config.General.requestName   = 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000_RunIISummer16_NANOAOD_PrivateFullProd'
config.General.workArea = 'crab_output'

## Specific option of the job type
## these options are directly readable from the job type plugin
config.section_("JobType")
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName    = 'nanoaod2016.py'

## Specific data options
config.section_("Data")
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

config.Data.inputDataset = '/CRAB_PrivateMC/cprieels-DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000_RunIISummer16_MINIAOD_PrivateFullProd-bd3e7bcff6c9bcad356ea4ed7e4f08b4/USER'
config.Data.outputDatasetTag   = 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000_RunIISummer16_NANOAOD_PrivateFullProd'

config.Data.publication     = True
config.Data.outLFNDirBase = '/store/user/cprieels/'

config.section_("Site")
config.Site.storageSite = 'T2_ES_IFCA'
#config.Site.storageSite = 'T2_CH_CERN'
