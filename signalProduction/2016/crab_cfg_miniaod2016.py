from CRABClient.UserUtilities import config
config = config()

config.section_("General")
config.General.transferLogs = True
config.General.requestName = 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000_RunIISummer16_MINIAOD_PrivateFullProd'
#config.General.requestName = 'DMPseudoscalar_ttbar01j_mphi_10_mchi_1_July2019' 
config.General.workArea = 'crab_output'

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'miniaod2016.py'
#config.JobType.maxMemoryMB = 4000

config.section_("Data")
config.Data.splitting       = 'FileBased'
config.Data.unitsPerJob = 1
#config.Data.outputDatasetTag = 'DMPseudoscalar_ttbar01j_mphi_10_mchi_1_July2019_step1'
config.Data.outputDatasetTag = 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000_RunIISummer16_MINIAOD_PrivateFullProd'
config.Data.inputDBS = 'phys03'
config.Data.outLFNDirBase = '/store/user/cprieels/' 
config.Data.publication = True
config.Data.inputDataset = '/CRAB_PrivateMC/cprieels-DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000_RunIISummer16_AODSIM_PrivateFullProd-f7b11725a86c799f51ca60747917325e/USER'

config.section_("Site")
config.Site.storageSite = 'T2_ES_IFCA'
