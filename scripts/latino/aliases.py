
### aliases = { }

if '2016' in opt.tag:
    yeartag = '2016'
    zerohitElectronRootFile = 'Full2016v2/ElectronScaleFactors_Run2016_SUSY.root'
elif '2017' in opt.tag:
    yeartag = '2017'
    zerohitElectronRootFile = 'Full2017/ElectronScaleFactors_Run2017_SUSY.root'
elif '2018' in opt.tag:
    yeartag = '2018' 
    zerohitElectronRootFile = 'Full2018/ElectronScaleFactors_Run2018_SUSY.root'

fastsimLeptonScaleFactorFile = os.getenv('PWD')+'/Data/'+yeartag+'/fastsimLeptonWeights.root'
fastsimMuonScaleFactorHisto = 'Muo_tight_fullsim'
fastsimElectronScaleFactorHisto = 'Ele_tight_fullsim'

aliases['fastsimLeptonWeight'] = {
        'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/fastsimLeptonWeightReader.cc+' ],
        'class': 'FastsimLeptonWeightReader',
        'args': ( fastsimLeptonScaleFactorFile, fastsimMuonScaleFactorHisto, fastsimElectronScaleFactorHisto ),
        'samples': [ ]
} 

for sample in samples:
    if 'isFastsim' in samples[sample] and samples[sample]['isFastsim']:
        aliases['fastsimLeptonWeight']['samples'].append(sample)
        samples[sample]['weight'] = samples[sample]['weight'].replace(LepWeightFS, 'fastsimLeptonWeight')

zerohitElectronScaleFactorFile = os.getenv('CMSSW_BASE')+'/src/LatinoAnalysis/NanoGardener/python/data/scale_factor/'+zerohitElectronRootFile
zerohitElectronScaleFactorHisto = 'Run'+yeartag+'_ConvIHit0'

aliases['zerohitLeptonWeight'] = {
        'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/zerohitLeptonWeightReader.cc+' ],
        'class': 'ZeroHitLeptonWeightReader',
        'args': ( zerohitElectronScaleFactorFile , zerohitElectronScaleFactorHisto ),
        'samples': [ ]
}

"""
for sample in samples:
    if not samples[sample]['isDATA']:
        aliases['zerohitLeptonWeight']['samples'].append(sample)
        samples[sample]['weight'] = samples[sample]['weight'].replace(EleWeight, EleWeight+'*zerohitLeptonWeight')
"""
