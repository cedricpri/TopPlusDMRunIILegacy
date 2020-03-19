from CRABClient.UserUtilities import config
config = config()

config.section_("General")
config.General.transferLogs = True
config.General.requestName = 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi100_RunIIAutumn18_PREMIX_PrivateProd'
#config.General.requestName = 'DMPseudoscalar_ttbar01j_mphi_10_mchi_1_July2019' 
config.General.workArea = 'crab_output'

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'premix.py'
config.JobType.maxMemoryMB = 4000

config.section_("Data")
config.Data.splitting       = 'FileBased'
config.Data.unitsPerJob = 1
#config.Data.outputDatasetTag = 'DMPseudoscalar_ttbar01j_mphi_10_mchi_1_July2019_step1'
config.Data.outputDatasetTag = 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi100_RunIIAutumn18_PREMIX_PrivateProd'
config.Data.inputDBS = 'phys03'
config.Data.outLFNDirBase = '/store/user/cprieels/' 
config.Data.publication = True
config.Data.inputDataset = '/CRAB_PrivateMC/cprieels-DMscalar_Dilepton_top_tWChan_Mchi1_Mphi100_RunIIAutumn18_GENSIM_PrivateProd-610025f35b72a990658d644c87bd8d29/USER'

config.section_("Site")
config.Site.storageSite = 'T2_ES_IFCA'
