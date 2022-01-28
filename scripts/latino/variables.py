import re
# variables
    
# Flags  
gv   = ' [GeV]'
pt   = '#font[50]{p}_{T}'
met  = pt+'^{miss}'
sll  = '#font[12]{ll}'
pll  = '('+sll+')'
mt2  = '#font[50]{m}_{T2}'
ptll = pt+'^{'+sll+'}'
dphill = '#Delta#phi(lep1,lep2)'
dphillptmiss = '#Delta#phi('+sll+','+met+')'
dphiminlepptmiss = '#Delta#phi^{min}(lep,'+met+')'
dphijetptmiss  = '#Delta#phi(jet,'+met+')'
dphijet0ptmiss = '#Delta#phi(lead. jet,'+met+')'
dphijet1ptmiss = '#Delta#phi(trai. jet,'+met+')'
drll = '#Delta R(lep1,lep2)'
mtllptmiss = '#font[50]{m}_{T}('+sll+','+met+')'

# Complex variables
sumLeptonPt = 'Lepton_pt['+lep0idx+']+Lepton_pt['+lep1idx+']'
deltaMET    = 'MET_pt     - GenMET_pt' 
deltaMETFix = 'METFixEE2017_pt - GenMET_pt'
nbjets = 'Sum$(CleanJet_pt>='+bTagPtCut+' && abs(CleanJet_eta)<'+bTagEtaMax+' && Jet_'+btagAlgo+'[CleanJet_jetIdx]>='+bTagCut+')'
# variables = {}

## mkShape
#overflow  = 1
#underflow = 2
## mkShapeMulti
overflow  = 2
underflow = 1

ctrltag = ''
if 'SameSign' in opt.tag or 'Fake' in opt.tag or 'WZVal' in opt.tag or 'WZtoWW' in opt.tag or 'ttZ' in opt.tag or 'ZZVal' in opt.tag or 'FitCRWZ' in opt.tag or 'FitCRZZ' in opt.tag:
    if 'SameSign' in opt.tag: ctrltag = '_SameSign'
    if 'Fake'     in opt.tag: ctrltag = '_Fake'
    if 'WZVal'    in opt.tag: ctrltag = '_WZ'
    if 'WZtoWW'   in opt.tag: ctrltag = '_WZtoWW'
    if 'ttZ'      in opt.tag: ctrltag = '_ttZ'
    if 'ZZVal'    in opt.tag: ctrltag = '_ZZ'
    if 'FitCRWZ'  in opt.tag: ctrltag = '_WZ'
    if 'FitCRZZ'  in opt.tag: ctrltag = '_ZZ'

if 'Preselection' in opt.tag:

    variables['ptmiss']        = {  'name'  : 'ptmiss',                #   variable name    
                                    'range' : (  40,    0.,  400.),    #   variable range
                                    'xaxis' : met + gv,                #   x axis name
                                    'fold'  : overflow                 #   fold overflow
                                }
    
    variables['njets']         = {  'name'  : 'nCleanJet',             #   variable name    
                                    'range' : (  6,    0.,     6.),    #   variable range
                                    'xaxis' : 'number of jets',        #   x axis name
                                    'fold'  : overflow                 #   fold overflow
                                }
    
    variables['nbjets']        = {  'name'  : nbjets,                    #   variable name    
                                    'range' : (  5,    0.,     5.),      #   variable range
                                    'xaxis' : 'number of b-tagged jets', #   x axis name
                                    'fold'  : overflow                   #   fold overflow
                                }
    
    variables['mt2ll']         = {   'name'  : 'mt2ll',                #   variable name    
                                     'range' : (  20,    0.,  200.),   #   variable range
                                     'xaxis' : mt2 + pll + gv,         #   x axis name
                                     'fold'  : overflow                #   fold overflow
                                 }
    
    variables['jetpt']         = {   'name'  : 'CleanJet_pt',          #   variable name    
                                     'range' : (  40,    0.,  200.),   #   variable range
                                     'xaxis' : 'jet ' + pt + gv,       #   x axis name
                                     'fold'  : overflow                #   fold overflow
                                 }
    
    variables['Lep1pt']        = {   'name'  : 'Lepton_pt['+lep0idx+']',     #   variable name    
                                     'range' : (  40,    0.,  200.),         #   variable range
                                     'xaxis' : 'leading lepton ' + pt + gv,  #   x axis name
                                     'fold'  : overflow                      #   fold overflow
                                 }
    
    variables['Lep2pt']        = {   'name'  : 'Lepton_pt['+lep1idx+']',     #   variable name    
                                     'range' : (  40,    0.,  200.),         #   variable range
                                     'xaxis' : 'trailing lepton ' + pt + gv, #   x axis name
                                     'fold'  : overflow                      #   fold overflow
                                 }

    variables['nPV']           = {   'name'  : 'PV_npvs',                    #   variable name    
                                     'range' : (  80,    0.,  80.),          #   variable range
                                     'xaxis' : 'Number of PVs',              #   x axis name
                                     'fold'  : overflow                      #   fold overflow
                                 }
    
    variables['mll']           = {   'name'  : 'mll',                #   variable name    
                                     'range' : ( 100,    0.,  200.), #   variable range
                                     'xaxis' : 'm' + pll + gv,       #   x axis name
                                     'fold'  : overflow              #   fold overflow
                                 }

    variables['MET_significance']   = {  'name'  : MET_significance,         #   variable name    
                                  'range' : (  25,    0.,  25.),      #   variable range
                                  'xaxis' : met+' significance',      #   x axis name
                                  'fold'  : overflow                  #   fold overflow
                               }

    variables['dPhillptmiss']   = {  'name'  : dPhillptmiss,        #   variable name    
                                     'range' : (  10,    0.,  3.2), #   variable range
                                     'xaxis' : dphillptmiss,        #   x axis name
                                     'fold'  : overflow             #   fold overflow
                                  }

    variables['ptll']          = {  'name'  : pTll,                    #   variable name    
                                    'range' : ([0, 20, 30, 40, 50, 60, 70, 80, 100, 120, 150, 200, 250, 300, 400, 500, 1000],[1]), #   variable range
                                    'xaxis' : ptll + gv,               #   x axis name
                                    'fold'  : overflow                 #   fold overflow
                                 }
    
if 'CR' in opt.tag or 'Rinout' in opt.tag or 'SR' in opt.tag or 'Test' in opt.tag:

    variables['events']  = {   'name': '1',
                               'range' : (1,0,2),
                               'xaxis' : 'events',
                               'fold' : 3
                           }

    variables['pt1']  = {   'name': 'Lepton_pt[0]',
                            'range' : (40,0,600),
                            'xaxis' : 'p_{T} 1st lep',
                            'fold'  : 3
                        }

    ptbinning = ([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 240, 280, 320, 400, 480, 600],)
    variables['pt1_customBins']  = {   'name': 'Lepton_pt[0]',
                                       'range' : ptbinning,
                                       'xaxis' : 'p_{T} 1st lep',
                                    'fold'  : 3
                        }
    
    variables['pt2']  = {   'name': 'Lepton_pt[1]',
                            'range' : (50,0,400),
                            'xaxis' : 'p_{T} 2nd lep',
                            'fold'  : 3
                        }

    variables['pt2_customBins']  = {   'name': 'Lepton_pt[1]',
                            'range' : ptbinning,
                            'xaxis' : 'p_{T} 2nd lep',
                            'fold'  : 3
                        }

    variables['eta1']  = {  'name': 'Lepton_eta[0]',
                            'range' : (40,-3,3),
                            'xaxis' : '#eta 1st lep',
                            'fold'  : 3
                        }

    variables['eta2']  = {  'name': 'Lepton_eta[1]',
                            'range' : (40,-3,3),
                            'xaxis' : '#eta 2nd lep',
                            'fold'  : 3
                        }

    if 'Test' not in opt.tag:
        variables['dphill']  = {   'name': 'abs(dphill)',
                                   'range' : (40,0,3.14),
                                   'xaxis' : '#Delta#phi_{ll}',
                                   'fold' : 3
                               }
    
        variables['dphillmet']  = {   'name': 'abs(dphillmet)',
                                      'range' : (40,0,3.14),
                                      'xaxis' : '#Delta#phi_{ll, MET}',
                                      'fold' : 3
                                  }

        variables['njet']  = {    'name': 'nJetMine',
                                  'range' : (6,0,6),
                                  'xaxis' : 'Number of jets',
                                  'fold' : 3
                              }

        variables['nbjet']  = {    'name': 'nbJet',
                                   'range' : (5,0,5),
                                   'xaxis' : 'Medium deepCSV b-jets',
                                   'fold' : 0
                               }
        
        variables['mblt']  = {   'name': 'mblt',
                                 'range' : (40,0,600),
                                 'xaxis' : 'm_{bl}^{t} [GeV]',
                                 'fold' : 0
                             }
        
        variables['jetpt1']  = {    'name': 'CleanJetMine_pt[0]',
                                    'range' : (40,0,600),
                                    'xaxis' : 'p_{T} 1st jet',
                                    'fold' : overflow
                                }
        
        variables['jetpt2']  = {    'name': 'CleanJetMine_pt[1]',
                                    'range' : (40,0,600),
                                    'xaxis' : 'p_{T} 2nd jet',
                                    'fold' : overflow
                            }
    
        variables['jeteta1']  = {  'name': 'CleanJetMine_eta[0]',
                                   'range' : (40,-4.0,4.0),
                                   'xaxis' : '#eta 1st jet',
                                   'fold'  : overflow
                               }
    
        variables['jeteta2']  = {  'name': 'CleanJetMine_eta[1]',
                                   'range' : (40,-4.0,4.0),
                                   'xaxis' : '#eta 2nd jet',
                                   'fold'  : overflow
                               }

    #Discriminating variables 
    variables['mll']  = {   'name': 'mll',
                            'range' : (40,0,1000),
                            'xaxis' : 'm_{ll} [GeV]',
                            'fold' : 3
                        }

    mllbinning = ([0, 80, 120, 160, 200, 240, 280, 320, 360, 400, 500, 600, 800, 1000],)
    variables['mll_customBins']  = {   'name': 'mll',
                            'range' : mllbinning,
                            'xaxis' : 'm_{ll} [GeV]',
                            'fold' : 3
                        }
    
    variables['mllpeak']  = {   'name': 'mll',
                            'range' : (20,70,120),
                            'xaxis' : 'm_{ll} [GeV]',
                            'fold' : 3
                        }

    variables['puppimet']  = {   'name': 'PuppiMET_pt',
                                 'range' : (40,0,800),
                                 'xaxis' : 'puppimet [GeV]',
                                 'fold'  : 3
                             }

    variables['pfmet_short']  = {   'name': 'MET_pt',
                                    'range' : (40,0,200),
                                    'xaxis' : 'pfmet [GeV]',
                                    'fold'  : 3
                                }

    variables['pfmet']  = {   'name': 'MET_pt',
                              'range' : (40,0,600),
                              'xaxis' : 'pfmet [GeV]',
                              'fold'  : 3
                          }

    variables['pfmet_extended']  = {   'name': 'MET_pt',
                          'range' : (40,0,800),
                          'xaxis' : 'pfmet [GeV]',
                          'fold'  : 3
                      }

    metbinning = ([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 240, 280, 320, 400, 600],)
    metbinningCombine = ([0, 30, 60, 90, 120, 150, 300],)
    variables['pfmet_customBins']  = {   'name': 'MET_pt',
                                         'range' : metbinning,
                                         'xaxis' : 'pfmet [GeV]',
                                         'fold'  : 3
                                     }

    if 'Test' not in opt.tag:
        variables['METcorrected_pt']  = {   'name': 'METcorrected_pt',
                                            'range' : (40,0,600),
                                            'xaxis' : 'pfmet [GeV]',
                                            'fold'  : 3
                                        }

        variables['METcorrected_pt_customBins']  = {   'name': 'METcorrected_pt',
                                                       'range' : metbinning,
                                                       'xaxis' : 'pfmet [GeV]',
                                                       'fold'  : 3
                                                   }

        variables['METcorrected_pt_customBins_combine']  = {   'name': 'METcorrected_pt',
                                                               'range' : metbinningCombine,
                                                               'xaxis' : 'pfmet [GeV]',
                                                               'fold'  : 3
                                                           }
        
        variables['pfmet_phi']  = {   'name': 'MET_phi',
                                      'range' : (40,-3.2,3.2),
                                      'xaxis' : 'pfmet #phi',
                                      'fold'  : 3
                                  }

        
        variables['METcorrected_phi']  = {   'name': 'METcorrected_phi',
                                             'range' : (40,-3.2,3.2),
                                             'xaxis' : 'pfmet #phi',
                                             'fold'  : 3
                                         }

    variables['MET_significance']  = {   'name': 'MET_significance',
                                         'range' : (40,0,500),
                                         'xaxis' : 'MET significance',
                                         'fold'  : 3
    }

    variables['mt2ll']  = {   'name': 'mt2ll',
                              'range' : (40,0,300),
                              'xaxis' : 'm_{T2}^{ll} [GeV]',
                              'fold'  : 3
                          }
    
    if 'Test' not in opt.tag:
        variables['mt2bl']  = {   'name': 'mt2bl',
                                  'range' : (40,0,300),
                                  'xaxis' : 'm_{T2}^{bl} [GeV]',
                                  'fold'  : 2
                              }

        variables['mt2llMine']         = {   'name'  : 'mt2llMine',                #   variable name    
                                             'range' : (  20,    0.,  200.),   #   variable range
                                             'xaxis' : mt2 + pll + gv,         #   x axis name
                                             'fold'  : overflow                #   fold overflow
                                         }

        variables['costhetall']  = {   'name': 'costhetall',
                                       'range' : (40,-1.2,1.2),
                                       'xaxis' : 'cos(#theta_{l0,l1}) [rad]',
                                       'fold'  : 2
                                   }

        variables['cosphill']  = {   'name': 'cosphill',
                                     'range' : (40, -1.2, 1.2),
                                     'xaxis' : 'cos(#phi_{ll}) (parent rest frame) [rad]',
                                     'fold' : 2
                                 }
    
        variables['massT']  = {   'name': 'massT',
                                  'range' : (40,0,1500),
                                  'xaxis' : 'massT [GeV]',
                                  'fold'  : 3
                              }

        variables['totalET']  = {   'name': 'totalET',
                                    'range' : (40,0,2000),
                                    'xaxis' : 'Total ET [GeV]',
                                    'fold'  : 3
                                }

        variables['dark_pt']  = {   'name': 'dark_pt',
                                    'range' : (40,0,2000),
                                    'xaxis' : 'dark p_{T} [GeV]',
                                    'fold'  : 0
                                }
        
        variables['overlapping_factor']  = {   'name': 'overlapping_factor',
                                               'range' : (40,0,5),
                                               'xaxis' : 'Overlapping factor R',
                                               'fold'  : 0
                                        }

        variables['reco_weight']  = {   'name': 'reco_weight',
                                        'range' : (20,0,6),
                                        'xaxis' : 'log(#omega)',
                                        'fold'  : 2
                                    }

        #ATLAS variables    
        variables['r2l'] = {   'name': 'PuppiMET_pt / (Lepton_pt[0] + Lepton_pt[1])',
                               'range': (40,0,4),
                               'xaxis': 'r2l',
                               'fold': 0
                           }
    
        variables['r2l4j'] = {   'name': 'PuppiMET_pt / (Lepton_pt[0] + Lepton_pt[1] + CleanJetMine_pt[0] + CleanJetMine_pt[1] + CleanJetMine_pt[2] + CleanJetMine_pt[3])',
                                 'range': (40,0,3),
                                 'xaxis': 'r2l4j',
                                 'fold': 0
                             }


if ('ctrlTrees' in opt.tag and 'ttZ' in opt.tag):# or ('Test' in opt.tag):

    variables['events']  = {   'name': '1',
                               'range' : (1,0,2),
                               'xaxis' : 'events',
                               'fold' : 3
                           }
    
    variables['pt1']  = {   'name': 'Lepton_pt[0]',
                            'range' : (40,0,600),
                            'xaxis' : 'p_{T} 1st lep',
                            'fold'  : 3
                        }

    ptbinning = ([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 240, 280, 320, 400, 480, 600],)
    variables['pt1_customBins']  = {   'name': 'Lepton_pt[0]',
                                       'range' : ptbinning,
                                       'xaxis' : 'p_{T} 1st lep',
                                    'fold'  : 3
                        }
    
    variables['pt2']  = {   'name': 'Lepton_pt[1]',
                            'range' : (50,0,400),
                            'xaxis' : 'p_{T} 2nd lep',
                            'fold'  : 3
                        }

    variables['pt2_customBins']  = {   'name': 'Lepton_pt[1]',
                            'range' : ptbinning,
                            'xaxis' : 'p_{T} 2nd lep',
                            'fold'  : 3
                        }

    variables['eta1']  = {  'name': 'Lepton_eta[0]',
                            'range' : (40,-3,3),
                            'xaxis' : '#eta 1st lep',
                            'fold'  : 3
                        }

    variables['eta2']  = {  'name': 'Lepton_eta[1]',
                            'range' : (40,-3,3),
                            'xaxis' : '#eta 2nd lep',
                            'fold'  : 3
                        }

    variables['njets']         = {  'name'  : 'nCleanJet',             #   variable name    
                                    'range' : (  6,    0.,     6.),    #   variable range
                                    'xaxis' : 'number of jets',        #   x axis name
                                    'fold'  : overflow                 #   fold overflow
                                }

    mt2ll = 'mt2ll' + ctrltag
    variables['mt2ll']         = {   'name'  : mt2ll,                #   variable name    
                                     'range' : (  20,    0.,  200.),   #   variable range
                                     'xaxis' : mt2 + pll + gv,         #   x axis name
                                     'fold'  : overflow                #   fold overflow
                                 }

    mll = 'mll' + ctrltag
    variables['mll']  = {   'name': mll,
                            'range' : (40,0,1000),
                            'xaxis' : 'm_{ll} [GeV]',
                            'fold' : 3
                        }

    mllbinning = ([0, 80, 120, 160, 200, 240, 280, 320, 360, 400, 500, 600, 800, 1000],)
    variables['mll_customBins']  = {   'name': mll,
                            'range' : mllbinning,
                            'xaxis' : 'm_{ll} [GeV]',
                            'fold' : 3
                        }
    
    variables['mllpeak']  = {   'name': mll,
                            'range' : (20,70,120),
                            'xaxis' : 'm_{ll} [GeV]',
                            'fold' : 3
                        }

    variables['pfmet']  = {   'name': "MET_pt",
                            'range' : (40,0,300),
                            'xaxis' : 'MET_pt [GeV]',
                            'fold' : 3
                        }



if 'ctrlTrees' in opt.tag and 'SameSign' in opt.tag:

    variables['events']  = {   'name': '1',
                               'range' : (1,0,2),
                               'xaxis' : 'events',
                               'fold' : 3
                           }
    
    variables['pt1']  = {   'name': 'Lepton_pt[0]',
                            'range' : (40,0,600),
                            'xaxis' : 'p_{T} 1st lep',
                            'fold'  : 3
                        }

    ptbinning = ([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 240, 280, 320, 400, 480, 600],)
    variables['pt1_customBins']  = {   'name': 'Lepton_pt[0]',
                                       'range' : ptbinning,
                                       'xaxis' : 'p_{T} 1st lep',
                                    'fold'  : 3
                        }
    
    variables['pt2']  = {   'name': 'Lepton_pt[1]',
                            'range' : (50,0,400),
                            'xaxis' : 'p_{T} 2nd lep',
                            'fold'  : 3
                        }

    variables['pt2_customBins']  = {   'name': 'Lepton_pt[1]',
                            'range' : ptbinning,
                            'xaxis' : 'p_{T} 2nd lep',
                            'fold'  : 3
                        }

    variables['eta1']  = {  'name': 'Lepton_eta[0]',
                            'range' : (40,-3,3),
                            'xaxis' : '#eta 1st lep',
                            'fold'  : 3
                        }

    variables['eta2']  = {  'name': 'Lepton_eta[1]',
                            'range' : (40,-3,3),
                            'xaxis' : '#eta 2nd lep',
                            'fold'  : 3
                        }

    variables['pfmet_short']  = {   'name': 'MET_pt',
                                    'range' : (40,0,200),
                                    'xaxis' : 'pfmet [GeV]',
                                    'fold'  : 3
                                }
    
    variables['pfmet']  = {   'name': 'MET_pt',
                              'range' : (40,0,600),
                              'xaxis' : 'pfmet [GeV]',
                              'fold'  : 3
                          }

    variables['pfmet_extended']  = {   'name': 'MET_pt',
                          'range' : (40,0,800),
                          'xaxis' : 'pfmet [GeV]',
                          'fold'  : 3
                      }

    variables['njets']         = {  'name'  : 'nCleanJet',             #   variable name    
                                    'range' : (  6,    0.,     6.),    #   variable range
                                    'xaxis' : 'number of jets',        #   x axis name
                                    'fold'  : overflow                 #   fold overflow
                                }

    mt2ll = 'mt2ll' + ctrltag
    variables['mt2ll']         = {   'name'  : mt2ll,                #   variable name    
                                     'range' : (  20,    0.,  200.),   #   variable range
                                     'xaxis' : mt2 + pll + gv,         #   x axis name
                                     'fold'  : overflow                #   fold overflow
                                 }

    mll = 'mll' + ctrltag
    variables['mll']  = {   'name': mll,
                            'range' : (40,0,1000),
                            'xaxis' : 'm_{ll} [GeV]',
                            'fold' : 3
                        }

    mllbinning = ([0, 80, 120, 160, 200, 240, 280, 320, 360, 400, 500, 600, 800, 1000],)
    variables['mll_customBins']  = {   'name': mll,
                            'range' : mllbinning,
                            'xaxis' : 'm_{ll} [GeV]',
                            'fold' : 3
                        }
    
    variables['mllpeak']  = {   'name': mll,
                            'range' : (20,70,120),
                            'xaxis' : 'm_{ll} [GeV]',
                            'fold' : 3
                        }

if 'SR' in opt.tag:
    exec(open('./signalMassPoints.py').read())

    for massPoint in signalMassPoints:
        if massPointInSignalSet(massPoint, opt.sigset):

            options = massPoint.split("-")
            modelSelected = options[0]

            fullMassPoint = re.match(r"([a-zA-Z]+)([0-9]+)",options[1])
            mediatorSelected = fullMassPoint.group(1).replace("pseudo", "pseudoscalar")
            massPointSelected = fullMassPoint.group(2).replace("pseudo", "").replace("scalar", "")

            DNNbinning0 = ([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],)

            BDTbinning0 = ([-1.0, -0.65, -0.3, -0.1, 0.0, 0.1, 0.3, 0.65, 1.0],)
            BDTbinning1 = ([-1.0, -0.2, -0.1, 0.0, 0.1, 0.2, 1.0],)
            BDTbinning2 = ([-1.0, -0.4, -0.2, -0.1, 0.0, 0.1, 0.2, 0.4, 1.0],)
            BDTbinning3 = ([-1.0, -0.6, -0.4, -0.2, -0.1, 0.0, 0.1, 0.2, 0.4, 0.6, 1.0],)
            BDTbinning4 = ([-1.0, -0.5, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.5, 1.0],)
            BDTbinning5 = ([-1.0, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0],)
            BDTbinning6 = ([-1.0, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 1.0],)
            BDTbinning7 = ([-1.0, -0.55, -0.35, -0.2, -0.1, 0.0, 0.1, 0.2, 0.35, 0.55, 1.0],)

            for model in ["ST", "TTbar"]:
                training = {
                    'tag': model + '_DNN_output_signal_DM' + mediatorSelected + '_Dilepton_top_tWChan_Mchi1_Mphi' + massPointSelected,
                    'shortName': mediatorSelected + massPointSelected
                }
            
                variables[model + '_DNN_output_' + training['shortName']] = {   'name': training['tag'],
                                                                       'range' : (30,0,1),
                                                                       'xaxis' : 'DNN output',
                                                                       'fold' : 3
                                                                   }  

                training = {
                    'tag': model + '_BDT_output_signal_DM' + mediatorSelected + '_Dilepton_top_tWChan_Mchi1_Mphi' + massPointSelected,
                    'shortName': mediatorSelected + massPointSelected
                }
            
                variables[model + '_BDT_output_' + training['shortName']] = {   'name': training['tag'],
                                                                       'range' : (30,-1,1),
                                                                       'xaxis' : 'BDT output',
                                                                       'fold' : 3
                                                                   }  

                variables[model + '_BDT_output_' + training['shortName'] + '_customBinsAttempt0'] = {   'name': training['tag'],
                                                                                           'range' : BDTbinning0,
                                                                                           'xaxis' : 'BDT output',
                                                                                           'fold' : 3
                                                                                       }  

                variables[model + '_BDT_output_' + training['shortName'] + '_customBinsAttempt1'] = {   'name': training['tag'],
                                                                                               'range' : BDTbinning1,
                                                                                               'xaxis' : 'BDT output',
                                                                                               'fold' : 3
                                                                                           }  

                variables[model + '_BDT_output_' + training['shortName'] + '_customBinsAttempt2'] = {   'name': training['tag'],
                                                                                               'range' : BDTbinning2,
                                                                                               'xaxis' : 'BDT output',
                                                                                               'fold' : 3
                                                                                           }  

                variables[model + '_BDT_output_' + training['shortName'] + '_customBinsAttempt3'] = {   'name': training['tag'],
                                                                                               'range' : BDTbinning3,
                                                                                               'xaxis' : 'BDT output',
                                                                                               'fold' : 3
                                                                                           }  

                variables[model + '_BDT_output_' + training['shortName'] + '_customBinsAttempt4'] = {   'name': training['tag'],
                                                                                               'range' : BDTbinning4,
                                                                                               'xaxis' : 'BDT output',
                                                                                               'fold' : 3
                                                                                           }  

                variables[model + '_BDT_output_' + training['shortName'] + '_customBinsAttempt5'] = {   'name': training['tag'],
                                                                                               'range' : BDTbinning5,
                                                                                               'xaxis' : 'BDT output',
                                                                                               'fold' : 3
                                                                                           }  

                variables[model + '_BDT_output_' + training['shortName'] + '_customBinsAttempt6'] = {   'name': training['tag'],
                                                                                               'range' : BDTbinning6,
                                                                                               'xaxis' : 'BDT output',
                                                                                               'fold' : 3
                                                                                           }  

                variables[model + '_BDT_output_' + training['shortName'] + '_customBinsAttempt7'] = {   'name': training['tag'],
                                                                                               'range' : BDTbinning7,
                                                                                               'xaxis' : 'BDT output',
                                                                                               'fold' : 3
                                                                                           }  
                


"""
if 'Test' in opt.tag: 
    
    variables['nbjets']        = {  'name'  : nbjets,                    #   variable name    
                                    'range' : (  3,    0.,     3.),      #   variable range
                                    'xaxis' : 'number of b-tagged jets', #   x axis name
                                    'fold'  : overflow                   #   fold overflow
                                }

elif 'METFix' in opt.tag:
    variables['deltaMET']   = {  'name'  : deltaMET,                 #   variable name    
                                  'range' : (  40,    -20.,  20.),   #   variable range
                                  'xaxis' : deltaMET,             #   x axis name
                                  'fold'  : overflow                 #   fold overflow
                              }   
    variables['deltaMETfix']   = {  'name'  : deltaMETFix,           #   variable name    
                                    'range' : (  40,    -20.,  20.), #   variable range
                                    'xaxis' : deltaMETFix,           #   x axis name
                                    'fold'  : overflow               #   fold overflow
                                 }   
    variables['deltaMET_2']   = {  'name'  : deltaMET,                 #   variable name    
                                   'range' : (  40,    -50.,  50.),    #   variable range
                                   'xaxis' : deltaMET,              #   x axis name
                                   'fold'  : overflow                  #   fold overflow
                              }   
    variables['deltaMETfix_2']   = {  'name'  : deltaMETFix,           #   variable name    
                                      'range' : (  40,    -50.,  50.), #   variable range
                                      'xaxis' : deltaMETFix,           #   x axis name
                                      'fold'  : overflow               #   fold overflow
                                 }   
    variables['deltaMET_3']   = {  'name'  : deltaMET,                   #   variable name    
                                   'range' : (  40,    -100.,  100.),    #   variable range
                                   'xaxis' : deltaMET,                #   x axis name
                                   'fold'  : overflow                    #   fold overflow
                              }   
    variables['deltaMETfix_3']   = {  'name'  : deltaMETFix,             #   variable name    
                                      'range' : (  40,    -100.,  100.), #   variable range
                                      'xaxis' : deltaMETFix,             #   x axis name
                                      'fold'  : overflow                 #   fold overflow
                                 }   
    
    
elif 'DYchecks' in opt.tag:
    #print "inside this plots"
    #exit()
    variables['PuppiMET_pt']  = {  'name'  : 'PuppiMET_pt',           #   variable name    
                                    'range' : (  60,    0.,  350.),    #   variable range
                                    'xaxis' : "Puppi " + met + gv,      #   x axis name
                                    'fold'  : overflow                 #   fold overflow
                                }


    variables['ptmIss']        = {  'name'  : 'ptmiss',                #   variable name    
                                    'range' : (  60,    0.,  350.),    #   variable range
                                    'xaxis' : met + gv,                #   x axis name
                                    'fold'  : overflow                 #   fold overflow
                                }

    variables['njets']         = {  'name'  : 'nCleanJet',             #   variable name    
                                    'range' : (  6 ,    0.,  6.),      #   variable range
                                    'xaxis' : "number of jets",        #   x axis name
                                    'fold'  : overflow                 #   fold overflow
                                }

    variables['nbjets']         = {  'name'  : nbjets,                 #   variable name    
                                    'range' : (  5 ,    0.,  5.),      #   variable range
                                    'xaxis' : "number of b-taggedjets",#   x axis name
                                    'fold'  : overflow                 #   fold overflow
                                }
    variables['mt2ll']         = {  'name'  : 'mt2ll',                 #   variable name    
                                    'range' : (  40,    0.,  150.),    #   variable range
                                    'xaxis' : mt2+ pll  + gv,          #   x axis name
                                    'fold'  : overflow                 #   fold overflow
                                }

    variables['mll']           = {  'name'  : 'mll'  ,                 #   variable name    
                                    'range' : (  60,    0.,  200.),    #   variable range
                                    'xaxis' : 'm' + pll  + gv,         #   x axis name
                                    'fold'  : overflow                 #   fold overflow
                                }

elif 'VetoNoiseEE' in opt.tag:

    variables['jetRawPtEENoise'] = { 'name'  : jetrawpteenoise,                      #   variable name    
                                     'range' : (  20, 0., 100.),                     #   variable range
                                     'xaxis' : 'jet raw ' + pt + ' (EE Noise)' + gv, #   x axis name
                                     'fold'  : overflow                              #   fold overflow
                                    }
        
    variables['dPhiEENoisePtMissPt50'] = { 'name'  : dPhieenoiseptmiss_pt50, #   variable name    
                                           'range' : (  10,    0.,  3.2),    #   variable range
                                           'xaxis' : dphijetptmiss,          #   x axis name
                                           'fold'  : overflow                #   fold overflow
                                          }
    
    variables['dPhiEENoisePtMissPt30'] = { 'name'  : dPhieenoiseptmiss_pt30, #   variable name    
                                           'range' : (  10,    0.,  3.2),    #   variable range
                                           'xaxis' : dphijetptmiss,          #   x axis name
                                           'fold'  : overflow                #   fold overflow
                                          }
    
    variables['dPhiEENoisePtMissPt15'] = { 'name'  : dPhieenoiseptmiss_pt15, #   variable name    
                                           'range' : (  10,    0.,  3.2),    #   variable range
                                           'xaxis' : dphijetptmiss,          #   x axis name
                                           'fold'  : overflow                #   fold overflow
                                          }

    variables['dPhiEENoisePtMissHard'] = { 'name'  : dPhieenoiseptmiss_hard, #   variable name
                                           'range' : (  10,    0.,  3.2),    #   variable range
                                           'xaxis' : dphijetptmiss,          #   x axis name
                                           'fold'  : overflow                #   fold overflow
                                          }
        
    variables['dPhiEENoisePtMissPt30NoRawCut'] = { 'name'  : dPhieenoiseptmiss_pt30_norawcut, #   variable name    
                                                   'range' : (  10,    0.,  3.2),    #   variable range
                                                   'xaxis' : dphijetptmiss,          #   x axis name
                                                   'fold'  : overflow                #   fold overflow
                                                  }
    
    variables['dPhiEENoisePtMissPt15NoRawCut'] = { 'name'  : dPhieenoiseptmiss_pt15_norawcut, #   variable name    
                                                   'range' : (  10,    0.,  3.2),    #   variable range
                                                   'xaxis' : dphijetptmiss,          #   x axis name
                                                   'fold'  : overflow                #   fold overflow
                                                  }

    variables['HTForwardSoft'] = { 'name'  : HTForwardSoft,             #   variable name    
                                   'range' : (  30,    0.,  300),       #   variable range
                                   'xaxis' : 'H_{T} forward soft' + gv, #   x axis name
                                   'fold'  : overflow                   #   fold overflow
                                  }

    variables['HTForward']     = { 'name'  : HTForward,            #   variable name    
                                   'range' : (  30,    0.,  300),  #   variable range
                                   'xaxis' : 'H_{T} forward' + gv, #   x axis name
                                   'fold'  : overflow              #   fold overflow
                                  }

elif 'HighPtMissOptimisationRegion' in opt.tag: 
    
    variables['ptmissmt2ll']      = {  'name'  : 'ptmiss:mt2ll',                                             #   variable name    
                                       'range' : ([   0.,   10.,   20.,   30.,   40.,   50.,   60.,   70.,   80., 90.,  100.,  110.,  120.,  130.,  140.,  150.,  160.,  170., 180.,  190.,  200.,  210.,  220.,  230.,  240.,  250.,  260., 270.,  280.,  290.,  300.,  310.,  320.,  330.,  340.,  350., 360.,  370.,  380.,  390.,  400.,  410.,  420.,  430.,  440., 450.,  460.,  470.,  480.,  490.,  500.,  510.,  520.,  530.,  540.,  550.,  560.,  570.,  580.,  590.,  600.,  610.,  620., 630.,  640.,  650.,  660.,  670.,  680.,  690.,  700.,  710.,  720.,  730.,  740.,  750.,  760.,  770.,  780.,  790.,  800., 810.,  820.,  830.,  840.,  850.,  860.,  870.,  880.,  890.,  900.,  910.,  920.,  930.,  940.,  950.,  960.,  970.,  980., 990., 1000.],[   0.,   20.,   40.,   60.,   80.,  100.,  120.,  140.,  160.,  180.,  200.,  220.,  240.,  260.,  280.,  300.,  320.,  340.,  360.,  380.,  400.,  420.,  440.,  460.,  480.,  500.,  520.,   540.,  560.,  580.,  600.,  620.,  640.,  660.,  680.,  700.,  720.,  740.,  760.,  780.,  800.,  820.,  840.,  860.,  880.,  900.,  920.,  940.,  960.,  980., 1000., 1020., 1040., 1060.,  1080., 1100., 1120., 1140., 1160., 1180., 1200., 1220., 1240.,  1260., 1280., 1300., 1320., 1340., 1360., 1380., 1400., 1420.,  1440., 1460., 1480., 1500., 1520., 1540., 1560., 1580., 1600.,  1620., 1640., 1660., 1680., 1700., 1720., 1740., 1760., 1780.,  1800., 1820., 1840., 1860., 1880., 1900., 1920., 1940., 1960., 1980., 2000.]),  #   variable range
                                    'xaxis' : '2D #ptmiss:MT2',                                                      #   x axis name
                                    'fold'  : overflow                                                           #   fold overflow
                                    }
    variables['mt2ll']      = {  'name'  : 'mt2ll',                                             #   variable name    
                                     'range' : ([   0.,   10.,   20.,   30.,   40.,   50.,   60.,   70.,   80., 90.,  100.,  110.,  120.,  130.,  140.,  150.,  160.,  170., 180.,  190.,  200.,  210.,  220.,  230.,  240.,  250.,  260., 270.,  280.,  290.,  300.,  310.,  320.,  330.,  340.,  350., 360.,  370.,  380.,  390.,  400.,  410.,  420.,  430.,  440., 450.,  460.,  470.,  480.,  490.,  500.,  510.,  520.,  530.,  540.,  550.,  560.,  570.,  580.,  590.,  600.,  610.,  620., 630.,  640.,  650.,  660.,  670.,  680.,  690.,  700.,  710.,  720.,  730.,  740.,  750.,  760.,  770.,  780.,  790.,  800., 810.,  820.,  830.,  840.,  850.,  860.,  870.,  880.,  890.,  900.,  910.,  920.,  930.,  940.,  950.,  960.,  970.,  980., 990., 1000.],[1]),  #   variable range
                                    'xaxis' : 'MT2ll',                                                      #   x axis name
                                    'fold'  : overflow                                                           #   fold overflow
                                    }
    variables['ptmiss']      = {  'name'  : 'ptmiss',                                             #   variable name    
                                     'range' : ([   0.,   20.,   40.,   60.,   80.,  100.,  120.,  140.,  160.,  180.,  200.,  220.,  240.,  260.,  280.,  300.,  320.,  340.,  360.,  380.,  400.,  420.,  440.,  460.,  480.,  500.,  520.,   540.,  560.,  580.,  600.,  620.,  640.,  660.,  680.,  700.,  720.,  740.,  760.,  780.,  800.,  820.,  840.,  860.,  880.,  900.,  920.,  940.,  960.,  980., 1000., 1020., 1040., 1060.,  1080., 1100., 1120., 1140., 1160., 1180., 1200., 1220., 1240.,  1260., 1280., 1300., 1320., 1340., 1360., 1380., 1400., 1420.,  1440., 1460., 1480., 1500., 1520., 1540., 1560., 1580., 1600.,  1620., 1640., 1660., 1680., 1700., 1720., 1740., 1760., 1780.,  1800., 1820., 1840., 1860., 1880., 1900., 1920., 1940., 1960., 1980., 2000.],[1]),  #   variable range
                                    'xaxis' : 'ptmiss',                                                      #   x axis name
                                    'fold'  : overflow                                                           #   fold overflow
                                    }


elif 'btagefficiencies' in opt.tag: 
    
    variables['jetpteta']      = {  'name'  : 'abs(Jet_eta):Jet_pt',                                             #   variable name    
                                    'range' : ([20, 30, 40, 50, 60, 70, 80, 100, 120, 150, 200, 250, 400, 1000],[0.,0.2,0.4,0.8,1.2,1.6,2.0,2.5]),  #   variable range
                                    'xaxis' : '2D eta:#pt',                                                      #   x axis name
                                    'fold'  : overflow                                                           #   fold overflow
                                    }
                                   
    variables['jetpt']  = { 'name'  : 'Jet_pt',                              #   variable name    
                            'range' : ([20, 30, 40, 50, 60, 70, 80, 100, 120, 150, 200, 250, 400, 1000],[1]), #   variable range
                            'xaxis' : 'jet'+pt+gv,                           #   x axis name
                            'fold'  : overflow                               #   fold overflow
                            } 
    
    variables['jeteta'] = { 'name'  : 'abs(Jet_eta)',              #   variable name    
                            'range' : ([0.,0.2,0.4,0.8,1.2,1.6,2.0,2.5],[1]),  #   variable range
                            'xaxis' : 'jet pseudorapodity',        #   x axis name
                            } 

elif 'Trigger' in opt.tag:

    variables['Leptonpt1pt2']  = {  'name'  : 'Lepton_pt[1]:Lepton_pt[0]',                                         #   variable name  
                                    'range' : ([20, 25, 30, 40, 50, 70, 100, 150],[20, 25, 30, 40, 50, 70, 100, 150]), #   variable range
                                    'xaxis' : '2D pt',                                                             #   x axis name
                                    'fold'  : overflow                                                             #   fold overflow
                                   } 

    variables['Lepton1pteta']  = {  'name'  : 'Lepton_eta[0]:Lepton_pt[0]',                                        #   variable name
                                    'range' : ([20, 25, 30, 40, 50, 70, 100, 150, 300],[-2.4, -0.8, 0, 0.8, 2.4]), #   variable range
                                    'xaxis' : '2D eta:#pt'                                                         #   x axis name
                                  }

    #variables['Lepton1pt']     = {  'name'  : 'Lepton_pt[0]',                                                      #   variable name 
    #                                'range' : ([20, 25, 30, 40, 50, 70, 100, 150, 300],[1]),                       #   variable range    
    #                                'xaxis' : '1D pt',                                                             #   x axis name
    #                                'fold'  : overflow                                                             #   fold overflow
    #                              }
                                    
    #variables['Lepton1eta']    = {  'name'  : 'Lepton_eta[0]',                                                     #   variable name
    #                                'range' : ([-2.4, -0.8, 0, 0.8, 2.4][1]),                                      #   variable range   
    #                                'xaxis' : '1D eta',                                                            #   x axis name
    #                                'fold'  : 0                                                                    #   fold overflow
    #                              }

    if 'Latino' in opt.tag:
    
        variables['mT2']         = {   'name'  : 'mT2',                 #   variable name    
                                       'range' : (  20,    0.,  200.),  #   variable range
                                       'xaxis' : mt2 + pll + gv,        #   x axis name
                                       'fold'  : overflow               #   fold overflow
                                   }
    
        variables['mT2cr']       = {   'name'  : 'mT2',                 #   variable name    
                                       'range' : ([0, 20, 40, 60, 80, 100, 140, 240, 340],[1]),  # variable range
                                       'xaxis' : mt2 + pll + gv,        #   x axis name
                                       'fold'  : overflow               #   fold overflow
                                   }

    if 'HMControlRegion' in opt.tag:
        
        variables['mt2cr']       = {   'name'  : 'mt2ll',                #   variable name    
                                       'range' : ([0, 20, 40, 60, 80, 100, 140, 240, 340],[1]),  # variable range
                                       'xaxis' : mt2 + pll + gv,         #   x axis name
                                       'fold'  : overflow                #   fold overflow
                                   }

elif 'ttZNormalization' in opt.tag:

    variables['mll'] = {   'name'  : '90.',                #   variable name
                           'range' : (  1,    80.,  100.), #   variable range
                           'xaxis' : 'm' + pll + gv,       #   x axis name
                       }
  
    ptmissTTZ = ptmissNano
    if 'AddZ' in opt.tag:
        ptmissTTZ = ptmiss_ttZLoose

    variables['ptmiss'] = {  'name'  : ptmissTTZ,               #   variable name
                             'range' : (  20,    0.,  400.),    #   variable range
                             'xaxis' : met + gv,                #   x axis name
                             'fold'  : overflow                 #   fold overflow
                           }
 
    variables['ptmissSR'] = {  'name'  : ptmissTTZ,             #   variable name
                               'range' : ([0, 20, 40, 60, 80, 100, 120, 160, 220, 280, 380, 480],[1]), #   variable range
                               'xaxis' : met + gv,                #   x axis name
                               'fold'  : overflow                 #   fold overflow
                             }

    variables['njets']  = {  'name'  : 'nCleanJet',             #   variable name
                             'range' : (  6,    0.,     6.),    #   variable range
                             'xaxis' : 'number of jets',        #   x axis name
                             'fold'  : overflow                 #   fold overflow
                           }

    variables['jets']   = {  'name'  : 'nCleanJet>0',           #   variable name
                             'range' : (  2,    0.,     2.),    #   variable range 
                             'xaxis' : 'number of jets',        #   x axis name
                             'fold'  : overflow                 #   fold overflow
                           }

elif 'Validation' in opt.tag or 'Signal' in opt.tag:

    mt2ll = 'mt2ll' + ctrltag

    if 'FitCRttZ' in opt.tag: # this is not really right, but it's just for normalization
        mt2ll = 'mt2ll_WZtoWW*('+nLooseLepton+'==3) + mt2ll_ttZ*('+nLooseLepton+'==4)'

    if 'FakeValidationRegion' in opt.tag:
        mt2ll = T0+'*mt2llfake0+'+T1+'*mt2llfake1+'+T2+'*mt2llfake2'

    if 'StudyHighMT2' in opt.tag:
 
        variables['mt2ll']         = {   'name'  : mt2ll,                  #   variable name    
                                         'range' : (  40,    0.,  800.),   #   variable range
                                         'xaxis' : mt2 + pll + gv,         #   x axis name
                                         'fold'  : overflow                #   fold overflow
                                     }

    elif 'Optim' in opt.tag and 'MT2' in opt.tag:
        if 'High' in opt.tag:
            
            if 'Extrabin' in opt.tag:
                variables['mt2ll']         = {   'name'  : mt2ll,                  #   variable name    
                                                 'range' : ([0, 20, 40, 60, 80, 100, 160, 240,370,500],[1]), # variable range
                                                 'xaxis' : mt2 + pll + gv,         #   x axis name
                                                 'fold'  : overflow,               #   fold overflow
                                                 'CRbins' : [1, 4] 
                                             }

            else:
                variables['mt2ll']         = {   'name'  : mt2ll,                  #   variable name    
                                                 'range' : ([0, 20, 40, 60, 80, 100, 160, 370, 500],[1]), # variable range
                                                 'xaxis' : mt2 + pll + gv,         #   x axis name
                                                 'fold'  : overflow,               #   fold overflow
                                                 'CRbins' : [1, 4] 
                                             }

        else:
            variables['mt2ll']         = {   'name'  : mt2ll,                  #   variable name    
                                             'range' : ([0, 20, 40, 60, 80, 100, 160, 220],[1]), # variable range
                                             'xaxis' : mt2 + pll + gv,         #   x axis name
                                             'fold'  : overflow,               #   fold overflow
                                             'CRbins' : [1, 4] 
                                         }

    else:
    
        variables['mt2ll']         = {   'name'  : mt2ll,                  #   variable name    
                                         'range' : (   7,    0.,  140.),   #   variable range
                                         'xaxis' : mt2 + pll + gv,         #   x axis name
                                         'fold'  : overflow,               #   fold overflow
                                         'CRbins' : [1, 4] 
                                     }

        if 'ValidationRegion' in opt.tag:

            mt2llOptimBin = [0, 20, 40, 60, 80, 100, 160, 220]

            variables['mt2llOptim'] = {   'name'  : mt2ll,                  #   variable name    
                                          'range' : (mt2llOptimBin,[1]),    #   variable range
                                          'xaxis' : mt2 + pll + gv,         #   x axis name
                                          'fold'  : overflow,               #   fold overflow
                                          'CRbins' : [1, 4] 
                                      }

	    if 'ZZValidationRegion' in opt.tag or 'ttZValidationRegion' in opt.tag or 'DYValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag or 'WZValidationRegion' in opt.tag or 'FakeValidationRegion' in opt.tag:

                mt2llOptimHighBin = [0, 20, 40, 60, 80, 100, 160, 370, 500]                                                                                               

                variables['mt2llOptimHigh'] = {   'name'  : mt2ll,                   #   variable name
                                                  'range' : (mt2llOptimHighBin,[1]), #   variable range
                                                  'xaxis' : mt2 + pll + gv,          #   x axis name
                                                  'fold'  : overflow,                #   fold overflow
                                                  'CRbins' : [1, 4]                                                                                                                                                      }
                mt2llOptimHighExtraBin = [0, 20, 40, 60, 80, 100, 160, 240, 370, 500]

                variables['mt2llOptimHighExtra'] = {   'name'  : mt2ll,                        #   variable name
                                                       'range' : (mt2llOptimHighExtraBin,[1]), # variable range
                                                       'xaxis' : mt2 + pll + gv,               #   x axis name
                                                       'fold'  : overflow,                     #   fold overflow
                                                       'CRbins' : [1, 4]
                                                    }

    if 'StudyVisHT' in opt.tag:
 
        visht = sumLeptonPt+'+Sum$(CleanJet_pt)'
        
        variables['visht']         = {   'name'  : visht,                  #   variable name    
                                         'range' : ( 120,    0., 3000.),   #   variable range
                                         'xaxis' : 'visht' + gv,           #   x axis name
                                         'fold'  : overflow               #   fold overflow
                                     }
        
        variables['ht']            = {   'name'  : 'Sum$(CleanJet_pt)',    #   variable name    
                                         'range' : ( 120,    0., 3000.),   #   variable range
                                         'xaxis' : 'ht' + gv,              #   x axis name
                                         'fold'  : overflow                #   fold overflow
                                     }
        
        variables['sumLepPt']      = {   'name'  : sumLeptonPt,            #   variable name    
                                         'range' : ( 120,    0., 3000.),   #   variable range
                                         'xaxis' : 'sumleppt' + gv,        #   x axis name
                                         'fold'  : overflow                #   fold overflow
                                     }
    
        variables['njets']         = {  'name'  : 'nCleanJet',             #   variable name    
                                        'range' : (  6,    0.,     6.),    #   variable range
                                        'xaxis' : 'number of jets',        #   x axis name
                                        'fold'  : overflow                 #   fold overflow
                                    }

    if 'ttZValidationRegion' in opt.tag or 'ZZValidationRegion' in opt.tag or 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag or 'DYValidationRegion' in opt.tag: 

        variables['ptmiss']        = {  'name'  : 'ptmiss'+ctrltag,        #   variable name    
                                        'range' : (  20,    0.,  400.),    #   variable range                             
                                        'xaxis' : met + gv,                #   x axis name
                                        'fold'  : overflow                 #   fold overflow
                                     }

        variables['ptmissSR']     = {  'name'  : 'ptmiss'+ctrltag,        #   variable name    
                                        'range' : ([0, 20, 40, 60, 80, 100, 120, 160, 220, 280, 380, 480],[1]), #   variable range
                                        'xaxis' : met + gv,                #   x axis name
                                        'fold'  : overflow                 #   fold overflow
                                     }

        if 'DYValidationRegion' in opt.tag:   

            variables['deltaPhiLep']   = {  'name'  : dPhill,                  #   variable name    
                                            'range' : (  10,    0.,  3.2),     #   variable range
                                            'xaxis' : dphill,                  #   x axis name
                                            'fold'  : overflow                 #   fold overflow
                                         }

            variables['ptll']          = {  'name'  : pTll,                    #   variable name    
                                            'range' : ([0, 20, 30, 40, 50, 60, 70, 80, 100, 120, 150, 200, 250, 300, 400, 500, 1000],[1]), #   variable range
                                            'xaxis' : ptll + gv,               #   x axis name
                                            'fold'  : overflow                 #   fold overflow
                                         } 

        if 'ttZValidationRegion' in opt.tag or 'ZZValidationRegion' in opt.tag or 'WZValidationRegion' in opt.tag: 
    
            variables['njets']         = {  'name'  : 'nCleanJet',             #   variable name    
                                            'range' : (  6,    0.,     6.),    #   variable range
                                            'xaxis' : 'number of jets',        #   x axis name
                                            'fold'  : overflow                 #   fold overflow
                                         } 
    
            variables['jets']          = {  'name'  : 'nCleanJet>0',           #   variable name    
                                            'range' : (  2,    0.,     2.),    #   variable range
                                            'xaxis' : 'number of jets',        #   x axis name
                                            'fold'  : overflow                 #   fold overflow
                                         }
     
"""
