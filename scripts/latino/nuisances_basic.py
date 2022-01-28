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

# STATISTICAL 
### statistical uncertainty

nuisances['stat']  = {
              'type'  : 'auto',   # Use the following if you want to apply the automatic combine MC stat nuisances.
              'maxPoiss'  : '10',     # Number of threshold events for Poisson modelling
              'includeSignal'  : '1', # Include MC stat nuisances on signal processes (1=True, 0=False)
              'removeZeros' : removeZeros,
              'samples' : {}
             }







# EXPERIMENTAL
# luminosity -> https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#TabLum

split_lumi = False

if not split_lumi:

    nuisances['lumi']  = {
                   'name'  : 'lumi_13TeV_'+year,
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

# trigger

nuisances['trigger']  = {
               'name'  : 'trigger_'+year,
               'samples'  : { },
               'type'  : 'lnN',
}
for sample in samples.keys():
    if not samples[sample]['isDATA']:
        nuisances['trigger']  ['samples'][sample] = trigger_uncertainty #From Luca
        #nuisances['pileup']['samples'][sample] = ['((TriggerEffWeight_2l_u)/(TriggerEffWeight_2l))*(TriggerEffWeight_2l>0.02) + (TriggerEffWeight_2l<=0.02)', '(TriggerEffWeight_2l_d)/(TriggerEffWeight_2l)'] #As in Latino

# ECAL prefiring

if '2016' in opt.tag or '2017' in opt.tag: 
    nuisances['prefiring']  = {
        'name'  : 'prefiring_'+year, 
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
    }
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            nuisances['prefiring']['samples'][sample] = [ 'PrefireWeight_Up/PrefireWeight', 'PrefireWeight_Down/PrefireWeight' ] 

# lepton reco, id, iso, fastsim
"""
for scalefactor in leptonSF:

    nuisances[scalefactor]  = {
        'name'  : scalefactor+"_"+year,
        'samples'  : { },
    }
    nuisances[scalefactor]['type'] = leptonSF[scalefactor]['type']   
    if leptonSF[scalefactor]['type']=='shape':
        nuisances[scalefactor]['kind'] = 'weight'   
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            nuisances[scalefactor]['samples'][sample] = leptonSF[scalefactor]['weight']

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
                    if (mcType=='MC'):
                        nuisances[treeNuisance+mcType]['samples'][sample] = ['1.', '1.']

            if len(nuisances[treeNuisance+mcType]['samples'].keys())==0:
                del nuisances[treeNuisance+mcType]

    if hasattr(opt, 'cardList') and treeNuisances[treeNuisance]['MCtoFS']:
        if treeNuisance+'MC' in nuisances and treeNuisance+'FS' in nuisances:
            nuisances[treeNuisance+'MC']['samples'].update(nuisances[treeNuisance+'FS']['samples']) 
            del nuisances[treeNuisance+'FS']

# b-tagging scale factors
weight1b = btagWeight1tag+'_syst/'+btagWeight1tag
weight0b = '(1.-'+btagWeight1tag+'_syst)/(1.-'+btagWeight1tag+')'

btagSF = {
    'btag1b'     : [ weight1b.replace('syst', 'b_up'),         weight1b.replace('syst', 'b_down') ],
    'btag0b'     : [ weight0b.replace('syst', 'b_up'),         weight0b.replace('syst', 'b_down') ],
    'mistag1b'   : [ weight1b.replace('syst', 'l_up'),         weight1b.replace('syst', 'l_down') ],
    'mistag0b'   : [ weight0b.replace('syst', 'l_up'),         weight0b.replace('syst', 'l_down') ],
    #'btag1bFS'   : [ weight1b.replace('syst', 'b_up_fastsim'), weight1b.replace('syst', 'b_down_fastsim') ],
    #'btag0bFS'   : [ weight0b.replace('syst', 'b_up_fastsim'), weight0b.replace('syst', 'b_down_fastsim') ],
    #'ctag1bFS'   : [ weight1b.replace('syst', 'c_up_fastsim'), weight1b.replace('syst', 'c_down_fastsim') ],
    #'ctag0bFS'   : [ weight0b.replace('syst', 'c_up_fastsim'), weight0b.replace('syst', 'c_down_fastsim') ],
    #'mistag1bFS' : [ weight1b.replace('syst', 'l_up_fastsim'), weight1b.replace('syst', 'l_down_fastsim') ],
    #'mistag0bFS' : [ weight0b.replace('syst', 'l_up_fastsim'), weight0b.replace('syst', 'l_down_fastsim') ],
}

for scalefactor in btagSF:
    nuisances[scalefactor]  = {
        'name'  : scalefactor.replace('0', '').replace('1', '') +"_"+year,
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
        'cuts'  : [ ]           
    }
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            nuisances[scalefactor]['samples'][sample] = btagSF[scalefactor]

    for cut in cuts.keys():
        if ('1b' in scalefactor and ('_Tag' in cut or 'SS_' in cut or 'Fake' in cut or 'ttZValidation' in cut or '1tag' in cut or '2tag' in cut)) or ('0b' in scalefactor and ('_Veto' in cut or '_NoTag' in cut or 'WZ_' in cut or 'WZtoWW_' in cut or 'ZZ' in cut or 'Zpeak' in cut)):
            nuisances[scalefactor]['cuts'].append(cut)
"""
# top pt reweighting

nuisances['toppt']  = {
    'name'  : 'toppt', # assuming the mismodeling is correlated through the years 
    'samples'  : { 
        'ttbar' : [ systematicTopPt+'/'+centralTopPt, '1.' ],
        'STtW' : [ systematicTopPt+'/'+centralTopPt, '1.' ]
    },
    'kind'  : 'weight',
    'type'  : 'shape',
}






# BACKGROUND NORMALIZATION
"""
#Cover DY data/MC discrepancies
nuisances['dy_syst'] = {
    'name': 'CMS_dy_syst_'+year,
    'type': 'lnN',
    'samples': {
        'DY': '1.2'
    }
}
"""





# THEORETICAL

### PDF and alpha s

# PDF for background: https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeV and https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# DY: 14.78 / 6077.22 = 0.0024320
# ttZ: 0.0008 / 0.5297 = 0.0015103
# ttW: 0.002 / 0.2043 = 0.0097895
"""
nuisances['pdf']  = {
    'name'  : 'pdf',
    'type'  : 'lnN',
    'samples'  : {
        'DY'    : '1.003',
        'ttZ'   : '1.002',
        'ttW'   : '1.01',
        'WW'    : '1.06',
        'WZ'    : '1.05',
        'ZZ'    : '1.03'
    },
}

# ttbar: 35.06 / 831.76 = 0.0421
# single top: 6.16 / 216.99 = 0.0283
#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec

nuisances['pdf_alphas']  = {
    'name'  : 'pdf_alphas',
    'type'  : 'lnN',
    'samples'  : {
        'ttbar'    : '1.05',
        'STtW'      : '1.03'
    },
}

### Scale

nuisances['scale'] = {
    'name': 'scale',
    'type': 'lnN',
    'samples': {
        'ttbar': '1.04',
        'STtW': '1.03',
        'DY': '1.02',
        'WW': '1.04',
        'WZ': '1.04',
        'ZZ': '1.03'
    }
}

### UE
nuisances['UE']  = {
    'name'  : 'UE_CUET',
    'skipCMS' : 1,
    'type': 'lnN',
    'samples': {}
}
for sample in samples.keys():
    if not samples[sample]['isDATA']:
        nuisances['samples'][sample] = nuisances['UE']
"""













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
