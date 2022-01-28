# plot configuration

legend['lumi'] = 'L = '+str(opt.lumi)+'/fb'
legend['sqrt'] = '#sqrt{s} = 13 TeV'

sl  = '#font[12]{l}'
sllatex = '\\font[12]{l}'

# groupPlot = {}
# 
# Groups of samples to improve the plots.
# If not defined, normal plots is used
#

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:

    groupPlot['DY']  = {
        'nameHR' : 'Drell-Yan',
        'nameLatex' : '\\DY',
        'isSignal' : 0,
        'color': 877,
        'samples'  : ['DY'] 
    }

    if not 'GroupedBkg' in opt.tag:
        groupPlot['ttV']  = {
            'nameHR' : 't#bar{t}V',
            'nameLatex' : '\\ttV',
            'isSignal' : 0,
            'color': 434,
            'samples'  : ['ttZ', 'ttW'] 
        }

        groupPlot['ttSemilep']  = {
            'nameHR' : 't#bar{t} Semilep.',
            'nameLatex' : '\\ttbar Semilep.',
            'isSignal' : 0,
            'color': 920,
            'samples'  : ['ttSemilep'] 
        }

    groupPlot['STtW']  = {
        'nameHR' : 'tW',
        'nameLatex' : '\\tW',
        'isSignal' : 0,
        'color': 432,
        'samples'  : ['STtW'] 
    }

    groupPlot['ttbar']  = {
        'nameHR' : 't#bar{t}',
        'nameLatex' : '\\ttbar',
        'isSignal' : 0,
        'color': 600,
        'samples'  : ['ttbar'] 
    }

    if not 'GroupedBkg' in opt.tag:
        groupPlot['VV']  = {
            'nameHR' : 'VV',
            'nameLatex' : 'VV',
            'isSignal' : 0,
            'color': 800,
            'samples'  : ['WW', 'WZ', 'ZZ'] 
        }
        
        groupPlot['VVV']  = {
            'nameHR' : 'VVV',
            'nameLatex' : 'VVV',
            'isSignal' : 0,
            'color': 609,
            'samples'  : ['VVV'] 
        }
    else:
        groupPlot['Others']  = {
            'nameHR' : 'Others',
            'nameLatex' : 'Others',
            'isSignal' : 0,
            'color': 920,
            'samples'  : ['Others']
        }
        
#plot = {}

# keys here must match keys in samples.py    
#                    

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:
    
    plot['DY']  = {  
        'nameHR' : 'Drell-Yan',
        'nameLatex' : '\\DY',
        'color': 877,
        'isSignal' : 0,
        'isData'   : 0, 
        'scale'    : 1.   ,
    }
    
    plot['ttbar'] = {   
        'nameHR' : 't#bar{t}',
        'nameLatex' : '\\ttbar',
        'color': 600,
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }

    plot['STtW'] = {
        'nameHR' : 'tW',
        'nameLatex' : '\\tW',
        'color': 432,
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }

    if not 'GroupedBkg' in opt.tag:
        plot['ttSemilep'] = {   
            'nameHR' : 't#bar{t} Semilep.',
            'nameLatex' : '$\\ttbar Semilep.',
            'color': 920,
            'isSignal' : 0,
            'isData'   : 0 ,
            'scale'    : 1.0
        }

        plot['ttZ'] = { 
            'nameHR' : 't#bar{t}Z',
            'nameLatex' : '\\ttZ',
            'color'    : 434,
            'isSignal' : 0,
            'isData'   : 0,
            'scale'    : 1.0
        }
        
        plot['ttW'] = { 
            'nameHR' : 't#bar{t}W',
            'nameLatex' : '\\ttW',
            'color'    : 432,
            'isSignal' : 0,
            'isData'   : 0,
            'scale'    : 1.0
        }

        plot['WW']  = {  
            'nameHR' : 'WW',
            'nameLatex' : '\\WW',
            'color': 851,    # kAzure-9
            'isSignal' : 0,
            'isData'   : 0,
            'scale'    : 1.0                  
        }

        plot['WZ']  = {
            'nameHR' : 'WZ',  
            'nameLatex' : '\\WZ',
            'color': 798,    # kOrange-2
            'isSignal' : 0,
            'isData'   : 0,
            'scale'    : 1.0                  
        }

        plot['ZZ'] = { 
            'nameHR' : 'ZZ',
            'nameLatex' : '\\ZZ',
            'color'    : 803,   # kOrange+3
            'isSignal' : 0,
            'isData'   : 0,
            'scale'    : 1.0
        }
        
        plot['VVV'] = { 
            'nameHR' : 'VVV',
            'nameLatex' : '\\VVV',   
            'color'    : 394, #  kYellow-6
            'isSignal' : 0,
            'isData'   : 0,
            'scale'    : 1.0
        }
    else:
        plot['Others'] = { 
            'nameHR' : 'Others',
            'nameLatex' : 'Others',   
            'color'    : 920,
            'isSignal' : 0,
            'isData'   : 0,
            'scale'    : 1.0
        }

# Backward compatibility for background names
#plot['tW']  = plot['STtW']
#plot['ZZ']  = plot['ZZTo2L2Nu']
#plot['HWW'] = plot['Higgs']

sampleToRemoveFromPlot = [ ] 

for sample in plot:
    if sample not in samples:
        sampleToRemoveFromPlot.append(sample)

for sample in sampleToRemoveFromPlot:
    del plot[sample]

groupToRemoveFromPlot = [ ] 

for group in groupPlot:
    for sample in sampleToRemoveFromPlot:
        if sample in groupPlot[group]['samples']:
            groupPlot[group]['samples'].remove(sample)
    if len(groupPlot[group]['samples'])==0:
        groupToRemoveFromPlot.append(group)
    
for group in groupToRemoveFromPlot:
    del groupPlot[group]

# data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    plot['DATA']  = { 
        'nameHR' : 'Data',
        'color': 1 ,  
        'isSignal' : 0,
        'isData'   : 1 ,
        #'isBlind'  : 1
    }

# Signal  

if 'SR' in opt.tag:
    signalColor = 632 if opt.postFit=='n' else 880 # kViolet

    exec(open('./signalMassPoints.py').read())

    for massPoint in signalMassPoints:
        if massPointInSignalSet(massPoint, opt.sigset, False):

            options = massPoint.split("-")
            modelSelected = options[0]
            massPointSelected = options[1]
            mediatorSelected = ''.join([i for i in options[1] if not i.isdigit()])

            scaleFactor = "1000" if "500" in massPointSelected else "100" 
            massPointName = modelSelected + " " + massPointSelected.replace("pseudo", "PS").replace("scalar", "S") + " x" + scaleFactor

            plot[modelSelected + "-" + massPointSelected]  = {
                'nameHR' : massPointName,
                'nameLatex' : massPointName,
                'color': signalColor,
                'isSignal' : 2,
                'isData'   : 0,
                'scale'    : float(scaleFactor)
            }

            groupPlot[modelSelected + "-" + massPointSelected]  = {
                'nameHR' : massPointName,
                'nameLatex' : massPointName,
                'isSignal' : 2,
                'color': signalColor,
                'samples'  : [modelSelected + "-" + massPointSelected],
                'scale'    : float(scaleFactor)
            }

            signalColor += 2

for group in groupPlot:
    cutToRemoveFromGroup = [ ]
    for cut in cuts:
        samplesInCut = [ ]
        for sample in groupPlot[group]['samples']:
            if not ('removeFromCuts' in samples[sample] and cut in samples[sample]['removeFromCuts']):
                samplesInCut.append(sample)
        if len(samplesInCut)==0:
            cutToRemoveFromGroup.append(cut)
    if len(cutToRemoveFromGroup)>0:
        groupPlot[group]['removeFromCuts'] = cutToRemoveFromGroup
