### nuisances

### general parameters
if '2016' in opt.tag : 
    year = '_2016'
    lumi_uncertainty     = '1.025'
    lumi_uncertainty_unc = '1.022'
    lumi_uncertainty_cor = '1.012' 
    trigger_uncertainty = '1.020'
elif '2017' in opt.tag : 
    year = '_2017'
    lumi_uncertainty     = '1.023'
    lumi_uncertainty_unc = '1.020'
    lumi_uncertainty_cor = '1.011'
    trigger_uncertainty = '1.020'
elif '2018' in opt.tag : 
    year = '_2018'
    lumi_uncertainty     = '1.025'
    lumi_uncertainty_unc = '1.015'                                                                                                       
    lumi_uncertainty_cor = '1.020'
    trigger_uncertainty = '1.020'

### nuisances = {}
 
### statistical uncertainty

nuisances['stat']  = {
              'type'  : 'auto',   # Use the following if you want to apply the automatic combine MC stat nuisances.
              'maxPoiss'  : '10',     # Number of threshold events for Poisson modelling
              'includeSignal'  : '1', # Include MC stat nuisances on signal processes (1=True, 0=False)
              'removeZeros' : removeZeros,
              'samples' : {}
             }

### lnN

# luminosity -> https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#TabLum
"""
split_lumi = False

if not split_lumi:

    nuisances['lumi']  = {
                   'name'  : 'lumi_13TeV'+year,
                   'samples'  : { },
                   'type'  : 'lnN',
                   'lumisyst' : lumi_uncertainty
    }

else:

    nuisances['lumi_unc']  = {
                   'name'  : 'lumi_13TeV'+year,
                   'samples'  : { },
                   'type'  : 'lnN',
                   'lumisyst' : lumi_uncertainty_unc
    }

    nuisances['lumi_cor']  = {
                   'name'  : 'lumi_13TeV',
                   'samples'  : { },
                   'type'  : 'lnN',
                   'lumisyst' : lumi_uncertainty_cor
    }

for lumitype in [ 'lumi', 'lumi_unc', 'lumi_cor' ]:
    if lumitype in nuisances:
        for sample in samples.keys():
            if not samples[sample]['isDATA']:
                nuisances[lumitype]['samples'][sample] = nuisances[lumitype]['lumisyst']

# trigger

nuisances['trigger']  = {
               'name'  : 'trigger'+year,
               'samples'  : { },
               'type'  : 'lnN',
}
for sample in samples.keys():
    if not samples[sample]['isDATA']:
        nuisances['trigger']  ['samples'][sample] = trigger_uncertainty

# background cross section and scale factor uncertainties

for background in normBackgroundNuisances:
    if background in samples:

        scalefactorFromData = False

        for region in normBackgroundNuisances[background]:
            nuisancename = normBackgroundNuisances[background][region]['name']
            nuisances[nuisancename]  = {
                'name'    : nuisancename+year, 
                'samples' : normBackgroundNuisances[background][region]['samples'],
                'cuts'    : normBackgroundNuisances[background][region]['cuts'], 
                'type'    : normBackgroundNuisances[background][region]['type'],
            }
            if 'kind' in normBackgroundNuisances[background][region]:
                nuisances[nuisancename]['kind'] = normBackgroundNuisances[background][region]['kind']
            scalefactorFromData = normBackgroundNuisances[background][region]['scalefactorFromData']  

        if scalefactorFromData:
            
            for lumitype in [ 'lumi', 'lumi_cor', 'lumi_unc' ]:
                if lumitype in nuisances:
                    if background in nuisances[lumitype]['samples']:
                        del nuisances[lumitype]['samples'][background]
 
            if background in nuisances['trigger']['samples']:
                del nuisances['trigger']['samples'][background]

### shapes

# lepton reco, id, iso, fastsim

for scalefactor in leptonSF:

    nuisances[scalefactor]  = {
        'name'  : scalefactor+year,
        'samples'  : { },
    }
    nuisances[scalefactor]['type'] = leptonSF[scalefactor]['type']   
    if leptonSF[scalefactor]['type']=='shape':
        nuisances[scalefactor]['kind'] = 'weight'   
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            if 'FS' not in scalefactor or samples[sample]['isFastsim']:
                nuisances[scalefactor]['samples'][sample] = leptonSF[scalefactor]['weight']

# b-tagging scale factors

weight1b = btagWeight1tag+'_syst/'+btagWeight1tag
weight0b = '(1.-'+btagWeight1tag+'_syst)/(1.-'+btagWeight1tag+')'

btagSF = {
    'btag1b'     : [ weight1b.replace('syst', 'b_up'),         weight1b.replace('syst', 'b_down') ],
    'btag0b'     : [ weight0b.replace('syst', 'b_up'),         weight0b.replace('syst', 'b_down') ],
    'mistag1b'   : [ weight1b.replace('syst', 'l_up'),         weight1b.replace('syst', 'l_down') ],
    'mistag0b'   : [ weight0b.replace('syst', 'l_up'),         weight0b.replace('syst', 'l_down') ],
    'btag1bFS'   : [ weight1b.replace('syst', 'b_up_fastsim'), weight1b.replace('syst', 'b_down_fastsim') ],
    'btag0bFS'   : [ weight0b.replace('syst', 'b_up_fastsim'), weight0b.replace('syst', 'b_down_fastsim') ],
    'ctag1bFS'   : [ weight1b.replace('syst', 'c_up_fastsim'), weight1b.replace('syst', 'c_down_fastsim') ],
    'ctag0bFS'   : [ weight0b.replace('syst', 'c_up_fastsim'), weight0b.replace('syst', 'c_down_fastsim') ],
    'mistag1bFS' : [ weight1b.replace('syst', 'l_up_fastsim'), weight1b.replace('syst', 'l_down_fastsim') ],
    'mistag0bFS' : [ weight0b.replace('syst', 'l_up_fastsim'), weight0b.replace('syst', 'l_down_fastsim') ],
}

for scalefactor in btagSF:
    nuisances[scalefactor]  = {
        'name'  : scalefactor.replace('0', '').replace('1', '') +year,
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
        'cuts'  : [ ]           
    }
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            if 'FS' not in scalefactor or samples[sample]['isFastsim']:
                nuisances[scalefactor]['samples'][sample] = btagSF[scalefactor]
    for cut in cuts.keys():
        if ('1b' in scalefactor and ('_Tag' in cut or 'SS_' in cut or 'Fake' in cut or 'ttZValidation' in cut or '1tag' in cut or '2tag' in cut)) or ('0b' in scalefactor and ('_Veto' in cut or '_NoTag' in cut or 'WZ_' in cut or 'WZtoWW_' in cut or 'ZZ' in cut or 'Zpeak' in cut)):
            nuisances[scalefactor]['cuts'].append(cut)

# pileup

nuisances['pileup']  = {
    'name'  : 'pileup', # inelastic cross section correlated through the years
    'samples'  : { },
    'kind'  : 'weight',
    'type'  : 'shape',
}
for sample in samples.keys():
    if not samples[sample]['isDATA']:
        nuisances['pileup']['samples'][sample] = [ 'puWeightUp/puWeight', 'puWeightDown/puWeight' ] 

# ECAL prefiring

if '2016' in opt.tag or '2017' in opt.tag: 
    nuisances['prefiring']  = {
        'name'  : 'prefiring'+year, 
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
    }
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            nuisances['prefiring']['samples'][sample] = [ 'PrefireWeight_Up/PrefireWeight', 'PrefireWeight_Down/PrefireWeight' ] 

# nonprompt lepton rate

nuisances['nonpromptLep']  = {
    'name'  : 'nonpromptLep'+year, 
    'samples'  : { },
    'kind'  : 'weight',
    'type'  : 'shape',
}
for sample in samples.keys():
    if not samples[sample]['isDATA']:
        nuisances['nonpromptLep']['samples'][sample] = [ nonpromptLepSF_Up+'/'+nonpromptLepSF, nonpromptLepSF_Down+'/'+nonpromptLepSF ] 

# top pt reweighting

nuisances['toppt']  = {
    'name'  : 'toppt', # assuming the mismodeling is correlated through the years 
    'samples'  : { 'ttbar' : [ systematicTopPt+'/'+centralTopPt, '1.' ] },
    'kind'  : 'weight',
    'type'  : 'shape',
}

# isr fastsim

nuisances['isrFS']  = {
    'name'  : 'isrFS', # assuming the mismodeling is correlated through the years 
    'samples'  : { },
    'kind'  : 'weight',
    'type'  : 'shape',
}
for sample in samples.keys():
    if 'isrObservable' in samples[sample]:
            if samples[sample]['isrObservable']=='njetISR':
                isrWeight = [ '0.5*(3.*isrW-1.)', '0.5*(isrW+1.)/isrW' ]
            elif samples[sample]['isrObservable']=='ptISR':
                isrWeight = [ '(2.*isrW-1.)/isrW', '1./isrW' ]
            else:
                print 'ERROR: no isrW implementation for model', model
            nuisances['isrFS']['samples'][sample] = isrWeight

### mt2ll backgrounds (special case for shape uncertainties)

# mt2ll top and WW

### Update to new bins: get SR from cuts and adjust mt2ll bins for high MT2
mt2llRegions = [ ]
for cut in cuts:
    ptmissCut = cut.split('_')[0]+'_'
    if 'SR' in ptmissCut and ptmissCut not in mt2llRegions:
        mt2llRegions.append(ptmissCut)

mt2llBins = [ ]
mt2llNuisances = False
if not hasattr(opt, 'outputDirDatacard') or mt2llNuisances:
    if 'Optim' not in opt.tag or 'MT2' not in opt.tag:
        mt2llBins = ['Bin4', 'Bin5', 'Bin6', 'Bin7']
        mt2llEdges = ['60.', '80.', '100.', '120.', '999999999.']
        mt2llSystematics = [0.05, 0.10, 0.20, 0.30]
    elif 'High' in opt.tag and 'Extra' in opt.tag:
        mt2llBins = ['Bin6', 'Bin7', 'Bin8', 'Bin9' ]
        mt2llEdges = ['100.', '160.', '240.', '370.', '999999999.']    
        mt2llSystematics = [0.20, 0.30, 0.30, 0.30] # placeholders
    elif 'High' in opt.tag:
        mt2llBins = ['Bin6', 'Bin7', 'Bin8' ]     
        mt2llEdges = ['100.', '160.', '370.', '999999999.']
        mt2llSystematics = [0.20, 0.30, 0.30] # placeholders     
    else:
        mt2llBins = ['Bin6', 'Bin7' ]
        mt2llEdges = ['100.', '160.', '999999999.']
        mt2llSystematics = [0.20, 0.30] # placeholders            

for mt2llregion in mt2llRegions: 
    for mt2llbin in range(len(mt2llBins)):

        mt2llsystname = mt2llregion + mt2llBins[mt2llbin]
        mt2llweightUp = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.+mt2llSystematics[mt2llbin])+' : 1.'  
        mt2llweightDo = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.-mt2llSystematics[mt2llbin])+' : 1.'  
        
        nuisances['Top_'+mt2llsystname]  = {
            'name'  : 'Top_'+mt2llsystname+year,
            'samples'  : { 
                'ttbar' : [ mt2llweightUp, mt2llweightDo],
                'STtW'  : [ mt2llweightUp, mt2llweightDo],
                'tW'    : [ mt2llweightUp, mt2llweightDo], # backward compatibility for background names
            },
            'kind'  : 'weight',
            'type'  : 'shape',
            'cuts'  : [ ]           
        }
        
        nuisances['WW_'+mt2llsystname]  = {
            'name'  : 'WW_'+mt2llsystname+year,
            'samples'  : { 
                'WW' : [ mt2llweightUp, mt2llweightDo],
            },
            'kind'  : 'weight',
            'type'  : 'shape',
            'cuts'  : [ ]           
        }

        for cut in cuts.keys():
            if mt2llregion in cut:
                nuisances['Top_'+mt2llsystname]['cuts'].append(cut)
                nuisances['WW_' +mt2llsystname]['cuts'].append(cut)

# mt2ll DY (from control regions)
 
# mt2ll ZZ (from k-factors)

# mt2ll signal
if '__susyMT2reco' not in directorySig:
    nuisances['ptmissfastsim']  = {
        'name'  : 'ptmissfastsim', # mismodeling correlated through the years?
        'samples'  : { },
        'kind'  : 'tree',
        'type'  : 'shape',
        'folderUp':   directorySig.replace('__susyMT2fast', '__susyMT2reco'),
        'folderDown': directorySig.replace('__susyMT2fast', '__susyMT2genm').replace('Smear', 'Nomin'),
    }
    for sample in samples.keys():
        if samples[sample]['isFastsim']:
            nuisances['ptmissfastsim']['samples'][sample] = ['1.', '1.']

### QCD scale and PDFs

exec(open('./theoryNormalizations'+year+'.py').read())

# LHE scale variation weights (w_var / w_nominal)
# [0] is muR=0.50000E+00 muF=0.50000E+00
# [1] is muR=0.50000E+00 muF=0.10000E+01
# [2] is muR=0.50000E+00 muF=0.20000E+01
# [3] is muR=0.10000E+01 muF=0.50000E+00
# [4] is muR=0.10000E+01 muF=0.10000E+01
# [5] is muR=0.10000E+01 muF=0.20000E+01
# [6] is muR=0.20000E+01 muF=0.50000E+00
# [7] is muR=0.20000E+01 muF=0.10000E+01
# [8] is muR=0.20000E+01 muF=0.20000E+01

nuisances['qcdScale'] = {
    'name': 'qcdScale', # Scales correlated through the years?
    'kind': 'weight_envelope',
    'type': 'shape',
    'samples': { },
    'cuts' : [ ], 
}
for sample in samples.keys():
    if not samples[sample]['isDATA'] and theoryNormalizations[sample]['qcdScaleStatus']==3:
        if hasattr(opt, 'outputDirDatacard'):
            if '2016' in year and (sample=='Higgs' or sample=='ttZ' or sample=='VZ' or sample=='TChipmSlepSnu_mC-325_mX-150'): continue
            if '2017' in year and (sample=='VZ' or sample=='ttZ'): continue
            if '2018' in year and (sample=='WZ' or sample=='ttW' or sample=='VZ'): continue
        qcdScaleVariations = [ ] 
        for i in [0, 1, 3, 5, 7, 8]:
            qcdScaleVariations.append('LHEScaleWeight['+str(i)+']/'+str(theoryNormalizations[sample]['qcdScale'][i]))
        nuisances['qcdScale']['samples'][sample] = qcdScaleVariations

nuisances['pdf'] = {
    'name': 'pdf', # PDFs correlated through the years?
    'kind': 'weight_envelope',
    'type': 'shape',
    'samples': { },
    'cuts' : [ ],
}
for sample in samples.keys():
    if not samples[sample]['isDATA'] and not samples[sample]['isFastsim'] and theoryNormalizations[sample]['pdfStatus']==3:
        if hasattr(opt, 'outputDirDatacard'):
            if '2016' in year and (sample=='ttW' or sample=='VZ' or sample=='TChipmSlepSnu_mC-325_mX-150'): continue
            if '2017' in year and (sample=='VZ' or sample=='ttZ'): continue
            if '2018' in year and (sample=='WZ' or sample=='ttW' or sample=='VZ'): continue  
        pdfVariations = [ ] 
        for i in range(len(theoryNormalizations[sample]['pdf'])):                              
            pdfVariations.append('LHEPdfWeight['+str(i)+']/'+str(theoryNormalizations[sample]['pdf'][i]))
        nuisances['pdf']['samples'][sample] = pdfVariations

for cut in cuts:
    if 'SR' in cut.split('_')[0]:
        nuisances['qcdScale']['cuts'].append(cut)
        nuisances['pdf']['cuts'].append(cut)

### JES, JER and MET

for treeNuisance in treeNuisances:

    for mcType in treeNuisanceDirs[treeNuisance]:
        if 'Down' not in treeNuisanceDirs[treeNuisance][mcType] or 'Up' not in treeNuisanceDirs[treeNuisance][mcType]:
            print 'nuisance warning: missing trees for', treeNuisance, mcType, 'variations'
        else:

            mcTypeName = '_'+mcTpye if (mcType=='FS' and not treeNuisances[treeNuisance]['MCtoFS']) else ''
            yearCorr = '' if treeNuisances[treeNuisance]['year'] else year # correlated through the years?

            nuisances[treeNuisance+mcType] = {
                'name': treeNuisance+mcTypeName+yearCorr, 
                'kind': 'tree',
                'type': 'shape',
                'OneSided' : treeNuisances[treeNuisance]['onesided'],
                'synchronized' : False,
                'samples': { },
                'folderDown': treeNuisanceDirs[treeNuisance][mcType]['Down'],
                'folderUp':   treeNuisanceDirs[treeNuisance][mcType]['Up'],
            }
            for sample in samples.keys():
                if not samples[sample]['isDATA'] and not ('NoDY' in opt.tag and treeNuisance=='jer' and '2017' in year and sample=='DY'):
                    if (mcType=='MC' and not samples[sample]['isFastsim']) or (mcType=='FS' and samples[sample]['isFastsim']):
                        nuisances[treeNuisance+mcType]['samples'][sample] = ['1.', '1.']

            if len(nuisances[treeNuisance+mcType]['samples'].keys())==0:
                del nuisances[treeNuisance+mcType]

    if hasattr(opt, 'cardList') and treeNuisances[treeNuisance]['MCtoFS']:
        if treeNuisance+'MC' in nuisances and treeNuisance+'FS' in nuisances:
            nuisances[treeNuisance+'MC']['samples'].update(nuisances[treeNuisance+'FS']['samples']) 
            del nuisances[treeNuisance+'FS']

### rate parameters

rateparameters = {
    'Topnorm' :  { 
        'samples' : [ 'ttbar', 'tW', 'STtW' ],
        'subcuts' : [ '' ],
    },
    'WWnorm'  : {
        'samples' : [ 'WW' ],
        'subcuts' : [ '' ],
    },
    'NoJetRate_JetBack' : {
        'samples' : [ 'ttbar', 'tW', 'STtW', 'ttW', 'ttZ' ],
        'subcuts' : [ '_NoJet_' ],
        'limits'  : '[0.5,1.5]',
    },
    'JetRate_JetBack' : {
        'samples'  : [ 'ttbar', 'tW', 'STtW', 'ttW', 'ttZ' ],
        'subcuts'  : [ '_NoTag_' ],
        'bondrate' : 'NoJetRate_JetBack',
    },
    'NoJetRate_DibosonBack' : {
        'samples' : [ 'WW', 'WZ' ],
        'subcuts' : [ '_NoJet_' ],
        'limits'  : '[0.7,1.3]'
    },
    'JetRate_DibosonBack' : {
        'samples' : [ 'WW', 'WZ' ],
        'subcuts' : [ '_NoTag_' ],
        'bondrate' : 'NoJetRate_DibosonBack',
    },
}

if 'FitCR' in opt.tag:
    backgroundCRs = { 'ttZ' : { 'samples' : [ 'ttZ' ],
                                'regions' : { '_Tag_' : [ '_NoTag_', '_Veto_', '_Tag_' ] }, },
                      'WZ'  : { 'samples' : [ 'WZ' ],  
                                'regions' : { '_Veto_' : [ '_Veto_', '_Tag_' ] , '_NoTag_' : [ '_NoTag_', '_Tag_' ], '_NoJet_' : [ '_NoJet_' ] }, },
                      'ZZ'  : { 'samples' : [ 'ZZTo2L2Nu', 'ZZTo4L' ],
                                'regions' : { '_Veto_' : [ '_Veto_', '_Tag_' ] , '_NoTag_' : [ '_NoTag_', '_Tag_' ], '_NoJet_' : [ '_NoJet_' ] }, },
                    }
    for controlregion in backgroundCRs:
        for sample in backgroundCRs[controlregion]['samples']:
            for rateparam in rateparameters.keys():
                if sample in rateparameters[rateparam]['samples']: 
                    rateparameters[rateparam]['samples'].remove(sample)
        for region in backgroundCRs[controlregion]['regions']:
            useRegion = False
            for cut in cuts:
                if region in cut:
                    useRegion = True
                    continue
            if useRegion:
                rateparameters['CR'+region+controlregion] = { }
                rateparameters['CR'+region+controlregion]['samples'] = backgroundCRs[controlregion]['samples']
                rateparameters['CR'+region+controlregion]['subcuts'] = backgroundCRs[controlregion]['regions'][region]
                rateparameters['CR'+region+controlregion]['limits'] = '[0.3,1.7]'

if hasattr(opt, 'outputDirDatacard'):
    for mt2llregion in mt2llRegions: 
        for rateparam in rateparameters: 
            
            if 'CR_' in rateparam:
                useControlRegion = False            
                for cut in cuts:
                    if mt2llregion in cut and rateparam.split('_')[1]==cut.split('_')[1]:
                        useControlRegion = True
                        continue
                if not useControlRegion: continue

            rateparamname = rateparam + '_' + mt2llregion
            
            for sample in rateparameters[rateparam]['samples']:

                if sample not in samples: continue # backward compatibility for background names

                isControlSample = True if ('isControlSample' in samples[sample] and samples[sample]['isControlSample']==1) else False

                nuisances[sample+rateparamname]  = {
                    'name'  : rateparamname+year,
                    'samples'  : { sample : '1.00' },
                    'type'  : 'rateParam',
                    'cuts'  : [ ] 
                }
                
                if 'limits' in rateparameters[rateparam].keys():
                    nuisances[sample+rateparamname]['limits'] = rateparameters[rateparam]['limits'] 
                    
                for cut in cuts.keys():
                    if (mt2llregion in cut and not isControlSample) or (mt2llregion.replace('SR', 'CR') in cut and 'CR_' in rateparam and rateparam.split('_')[2]==cut.split('_')[2]):
                        for subcut in rateparameters[rateparam]['subcuts']:
                            if subcut in cut:
                                nuisances[sample+rateparamname]['cuts'].append(cut)
                        
                if 'bondrate' in rateparameters[rateparam].keys():
                                
                    fileIn = ROOT.TFile(opt.inputFile, "READ")

                    nuisances[sample+rateparamname]['bond'] = {}

                    for cut in nuisances[sample+rateparamname]['cuts']:

                        nuisances[sample+rateparamname]['bond'][cut] = {}

                        for variable in variables.keys():

                            histoB = fileIn.Get(cut+'/'+variable+'/histo_'+sample)
                            cutB = rateparameters[rateparam]['subcuts'][0]
                            cutA = rateparameters[rateparameters[rateparam]['bondrate']]['subcuts'][0]
                            histoA = fileIn.Get(cut.replace(cutB, cutA)+'/'+variable+'/histo_'+sample)
                            yieldB = '%-.4f' % histoB.Integral()
                            yieldA = '%-.4f' % histoA.Integral()
            
                            bond_formula = '1+'+yieldA+'/'+yieldB+'*(1.-@0)' 
                            bond_parameters = rateparameters[rateparam]['bondrate']+'_'+mt2llregion+year
                            
                            nuisances[sample+rateparamname]['bond'][cut][variable] =  { bond_formula : bond_parameters }

                    fileIn.Close()

### Cleaning 

nuisanceToRemove = [ ]
for nuisance in nuisances:
    if 'cuts' in nuisances[nuisance]:
        if len(nuisances[nuisance]['cuts'])==0:
            nuisanceToRemove.append(nuisance)

for nuisance in nuisanceToRemove:
    del nuisances[nuisance]

### Nasty tricks ...

nuisanceToRemove = [ ]  

if 'SignalRegion' in opt.tag or 'ValidationRegion' in opt.tag or 'ttZNormalization' in opt.tag:

    if 'ctrl' in regionName and 'cern' in SITE : # JES and MET variations not available at cern for ctrl trees
        
        if hasattr(opt, 'batchSplit'): # Remove only when running shapes, so can make shapes in gridui and plots in lxplus
            for nuisance in nuisances:
                if 'jesTotal' in nuisance or 'unclustEn' in nuisance: 
                    nuisanceToRemove.append(nuisance)
        
    else:
        pass

else:

    for nuisance in nuisances:
        if nuisance!='stat' and nuisance!='lumi': # example ...
            nuisanceToRemove.append(nuisance)

for nuisance in nuisanceToRemove:
    del nuisances[nuisance]
"""
