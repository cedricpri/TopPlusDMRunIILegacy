import os
import subprocess
import math
import string
from LatinoAnalysis.Tools.commonTools import *

### Generals

opt.lumi = 0.
if '2016' in opt.tag : 
    opt.lumi += 35.9 # 35.92
    yeartag = '2016'
if '2017' in opt.tag : 
    opt.lumi += 41.5 # 41.53
    yeartag = '2017'
if '2018' in opt.tag : 
    opt.lumi += 59.7 # 59.74
    yeartag = '2018'
print 'Value of lumi set to', opt.lumi

treePrefix= 'nanoLatino_'

### Directories
  
SITE=os.uname()[1]
if 'cern' not in SITE and 'ifca' not in SITE and 'cloud' not in SITE: SITE = 'cern'

if  'cern' in SITE :
    print 'nanoAODv8 trees not available yet on cern'

if '2016' in yeartag :
    ProductionMC   = 'Summer20UL16_106X_nAODv8_Full2016v8/MCSusy2016v8__MCSusyCorr2016v8__MCSusyNomin2016v8'
    ProductionSig  = 'Summer16FS_102X_nAODv6_Full2016v6loose/hadd__susyGen__susyW__FSSusy2016v6loose__FSSusyCorr2016v6loose__FSSusyNomin2016v6loose'
    ProductionData = 'Run2016_106X_nAODv8_Full2016v8/DATASusy2016v8__hadd'
elif '2017' in yeartag :
    ProductionMC   = 'Summer20UL17_106X_nAODv8_Full2017v8/MCSusy2017v8__MCSusyCorr2017v8__MCSusyNomin2017v8'
    ProductionSig  = 'Fall2017FS_102X_nAODv6_Full2017v6loose/hadd__susyGen__susyW__FSSusy2017v6loose__FSSusyCorr2017v6loose__FSSusyNomin2017v6loose'
    ProductionData = 'Run2017_106X_nAODv8_Full2017v8/DATASusy2017v8__hadd'
elif '2018' in yeartag :
    ProductionMC   = 'Summer20UL18_106X_nAODv8_Full2018v8/MCSusy2018v8__MCSusyCorr2018v8__MCSusyNomin2018v8'
    ProductionSig  = 'Autumn18FS_102X_nAODv6_Full2018v6loose/hadd__susyGen__susyW__FSSusy2018v6loose__FSSusyCorr2018v6loose__FSSusyNomin2018v6loose'
    ProductionData = 'Run2018_106X_nAODv8_Full2018v8/DATASusy2018v8__hadd'

metnom, metsmr = 'Nomin', 'Smear'
if 'Smear' in opt.tag:
    metnom, metsmr = 'Smear', 'Nomin'

regionName = '__susyMT2reco'+metnom+'/'
ctrltag = ''

if 'SameSign' in opt.tag or 'Fake' in opt.tag or 'WZVal' in opt.tag or 'WZtoWW' in opt.tag or 'ttZ' in opt.tag or 'ZZVal' in opt.tag or 'FitCRWZ' in opt.tag or 'FitCRZZ' in opt.tag:
    regionName = regionName.replace('reco', 'ctrl')
    if 'SameSign' in opt.tag: ctrltag = '_SameSign'
    if 'Fake'     in opt.tag: ctrltag = '_Fake'
    if 'WZVal'    in opt.tag: ctrltag = '_WZ'
    if 'WZtoWW'   in opt.tag: ctrltag = '_WZtoWW'
    if 'ttZ'      in opt.tag: ctrltag = '_ttZ'
    if 'ZZVal'    in opt.tag: ctrltag = '_ZZ'
    if 'FitCRWZ'  in opt.tag: ctrltag = '_WZ'
    if 'FitCRZZ'  in opt.tag: ctrltag = '_ZZ'

directoryBkg  = treeBaseDirMC   + ProductionMC   + regionName
directorySig  = treeBaseDirSig  + ProductionSig  + regionName.replace('reco',  'fast')
directoryData = treeBaseDirData + ProductionData + regionName.replace('Smear', 'Nomin')

#removeZeros = 1 #if 'StatZero' in opt.tag else 0
removeZeros = 0 if 'NoStat0' in opt.tag else 1

treeNuisances = { }
## TODO: when all trees for systematics are available
#if metnom=='Nomin':
#    treeNuisances['jer']       = { 'name' : metsmr,                    'year' : False, 'MCtoFS' : True, 'onesided' : True  }
#    treeNuisances['jesTotal']  = { 'name' : 'JES',  'jetname' : 'JES', 'year' : False, 'MCtoFS' : True, 'onesided' : False }
#    treeNuisances['unclustEn'] = { 'name' : 'MET',                     'year' : False, 'MCtoFS' : True, 'onesided' : False }
#elif metnom=='Smear':
#    #treeNuisances['jer']      = { 'name' : 'JER',  'jetname' : 'JER', 'year' : False, 'MCtoFS' : True, 'onesided' : False }
#    treeNuisances['jer']       = { 'name' : metsmr,                    'year' : False, 'MCtoFS' : True, 'onesided' : True  }
#    treeNuisances['jesTotal']  = { 'name' : 'SJS',  'jetname' : 'JES', 'year' : False, 'MCtoFS' : True, 'onesided' : False }
#    treeNuisances['unclustEn'] = { 'name' : 'SMT',                     'year' : False, 'MCtoFS' : True, 'onesided' : False }

treeNuisanceDirs = { }
#treeNuisanceSuffix = '' if  'ctrl' in regionName else '__hadd'
treeNuisanceSuffix = '__hadd' if  'cern' in SITE else ''
for treeNuisance in treeNuisances:
    treeNuisanceDirs[treeNuisance] = { 'MC' : { }, 'FS' : { }, }
    if treeNuisance=='jer' and treeNuisances[treeNuisance]['name']!='JER':
        treeNuisanceDirs['jer']['MC']['Up']   = directoryBkg.replace(metnom+'/', metsmr+'/') 
        treeNuisanceDirs['jer']['MC']['Down'] = directoryBkg
        treeNuisanceDirs['jer']['FS']['Up']   = directorySig.replace(metnom+'/', metsmr+'/') 
        treeNuisanceDirs['jer']['FS']['Down'] = directorySig
    else:
        directoryBkgTemp = directoryBkg.replace(metnom+'/', treeNuisances[treeNuisance]['name']+'variation'+treeNuisanceSuffix+'/') 
        directorySigTemp = directorySig.replace(metnom+'/', treeNuisances[treeNuisance]['name']+'variation'+treeNuisanceSuffix+'/') 
        if 'jetname' in treeNuisances[treeNuisance]:
            directoryBkgTemp = directoryBkgTemp.replace('SusyNomin', 'Susy'+treeNuisances[treeNuisance]['jetname']+'variation')
            directorySigTemp = directorySigTemp.replace('SusyNomin', 'Susy'+treeNuisances[treeNuisance]['jetname']+'variation') 
        for variation in [ 'Down', 'Up' ]:
            treeNuisanceDirs[treeNuisance]['MC'][variation]  = directoryBkgTemp.replace('variation', variation[:2])
            treeNuisanceDirs[treeNuisance]['FS'][variation]  = directorySigTemp.replace('variation', variation[:2])

# Complex cut variables

ElectronWP = 'Lepton_isTightElectron_cutBasedMediumPOG'
if 'EleTightPOG' in opt.tag:
    ElectronWP = 'Lepton_isTightElectron_cutBasedTightPOG'
MuonWP     = 'Lepton_isTightMuon_mediumRelIsoTight'

if 'TriggerLatino' in opt.tag:
    if '2016' in yeartag:
        ElectronWP = 'Lepton_isTightElectron_cut_WP_Tight80X' #'Lepton_isTightElectron_mva_90p_Iso2016'
        MuonWP     = 'Lepton_isTightMuon_cut_Tight80x'
    elif '2017' in yeartag or '2018' in yeartag:
        ElectronWP = 'Lepton_isTightElectron_cutFall17V2Iso_Tight' #'Lepton_isTightElectron_mvaFall17V2Iso_WP90'
        MuonWP     = 'Lepton_isTightMuon_cut_Tight_HWWW'
ElectronSF = ElectronWP.replace('isTightElectron', 'tightElectron')
MuonSF     = MuonWP.replace('isTightMuon', 'tightMuon')

lep0idx = '0'
lep1idx = '1'
lep2idx = '2'

nLooseLepton = 'nLepton'
nTightLepton = 'Sum$(('+ElectronWP+'+'+MuonWP+')==1)'

pxll = '(Lepton_pt['+lep0idx+']*cos(Lepton_phi['+lep0idx+'])+Lepton_pt['+lep1idx+']*cos(Lepton_phi['+lep1idx+']))'
pyll = '(Lepton_pt['+lep0idx+']*sin(Lepton_phi['+lep0idx+'])+Lepton_pt['+lep1idx+']*sin(Lepton_phi['+lep1idx+']))'
pTll = 'sqrt('+pxll+'*'+pxll+'+'+pyll+'*'+pyll+')'
phill = 'atan('+pyll+'/'+pxll+')'
dPhill = 'acos(cos(Lepton_phi['+lep1idx+']-Lepton_phi['+lep0idx+']))'
dEtall = 'Lepton_eta['+lep1idx+']-Lepton_eta['+lep0idx+']'
dRll = 'sqrt('+dPhill+'*'+dPhill+'+'+dEtall+'*'+dEtall+')'
ptmiss_phi = 'ptmiss_phi'+ctrltag
if "MET" in opt.tag:
    ptmiss_phi = 'MET_phi' 
mTllptmiss = 'sqrt(2*'+pTll+'*ptmiss*(1.-cos('+phill+'-'+ptmiss_phi+')))'
dPhillptmiss = 'acos(cos('+phill+'-'+ptmiss_phi+'))'
dPhilep0ptmiss = 'acos(cos(Lepton_phi['+lep0idx+']-'+ptmiss_phi+'))'
dPhilep1ptmiss = 'acos(cos(Lepton_phi['+lep1idx+']-'+ptmiss_phi+'))'
dPhiMinlepptmiss = 'TMath::Min('+dPhilep0ptmiss+','+dPhilep1ptmiss+')'
dPhijet0ptmiss = 'acos(cos(CleanJet_phi[0]-'+ptmiss_phi+'))'
dPhijet1ptmiss = 'acos(cos(CleanJet_phi[1]-'+ptmiss_phi+'))'
jetrawpteenoise = '(Jet_pt*(1.-Jet_rawFactor)*(2*(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)-1))'
jetpteenoise = '(Jet_pt*(2*(Jet_pt*(1.-Jet_rawFactor)<50. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)-1))'
dPhieenoiseptmiss_pt30 = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
dPhieenoiseptmiss_pt50 = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>50. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
dPhieenoiseptmiss_pt15 = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>15. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
dPhieenoiseptmiss_hard = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt*(1.-Jet_rawFactor)>50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
dPhieenoiseptmiss_pt30_norawcut = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
dPhieenoiseptmiss_pt15_norawcut = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt>15. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
HTForward     = 'Sum$(Jet_pt*(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139))'
HTForwardSoft = 'Sum$(Jet_pt*(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139 && Jet_pt*(1.-Jet_rawFactor)<50.))'
jetpteenoisedphi = '(Jet_pt*(2*(Jet_pt*(1.-Jet_rawFactor)<50. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139 && acos(cos(Jet_phi-'+ptmiss_phi+'))<0.96)-1))'

ptmissNano = 'MET_pt'
if 'Data' not in opt.sigset: # data do not have pt_nom, but it's equal to pt as the JEC in central production were the final ones
    if metnom=='Nomin': ptmissNano = 'MET_T1_pt'
    elif metnom=='Smear': ptmissNano = 'MET_T1Smear_pt'
ptmissPhiNano = ptmissNano.replace('_pt', '_phi')

ptxLep = 'Lepton_pt[abs(lepidx_WZtoWW)]*cos(Lepton_phi[abs(lepidx_WZtoWW)])'
ptyLep = 'Lepton_pt[abs(lepidx_WZtoWW)]*sin(Lepton_phi[abs(lepidx_WZtoWW)])'
chrLep = '((Lepton_pdgId[abs(lepidx_WZtoWW)]*Lepton_pdgId[abs(lep2idx_WZtoWW)])<0)'
metx_ttZ3Lep = '(ptmiss_WZtoWW*cos(ptmiss_phi_WZtoWW)+'+ptxLep.replace('lepidx', 'lep0idx')+'*'+chrLep.replace('lepidx', 'lep0idx')+'+'+ptxLep.replace('lepidx', 'lep1idx')+'*'+chrLep.replace('lepidx', 'lep1idx')+')' 
mety_ttZ3Lep = '(ptmiss_WZtoWW*sin(ptmiss_phi_WZtoWW)+'+ptyLep.replace('lepidx', 'lep0idx')+'*'+chrLep.replace('lepidx', 'lep0idx')+'+'+ptyLep.replace('lepidx', 'lep1idx')+'*'+chrLep.replace('lepidx', 'lep1idx')+')'
ptmiss_ttZ3Lep = 'sqrt('+metx_ttZ3Lep+'*'+metx_ttZ3Lep+'+'+mety_ttZ3Lep+'*'+mety_ttZ3Lep+')'
ptmiss_phi_ttZ3Lep = 'atan2('+mety_ttZ3Lep+', '+metx_ttZ3Lep+')' 
ptmiss_ttZLoose = '('+ptmiss_ttZ3Lep+'*(ptmiss_WZtoWW>=0.) + ptmiss_ttZ*(ptmiss_ttZ>=0.))'
ptmiss_phi_ttZLoose = '('+ptmiss_phi_ttZ3Lep+'*(ptmiss_WZtoWW>=0.) + ptmiss_phi_ttZ*(ptmiss_ttZ>=0.))'
 
OC =  nTightLepton + '==2 && mll'+ctrltag+'>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && (Lepton_pdgId[0]*Lepton_pdgId[1])<0'
SS =  nTightLepton + '==2 && mll'+ctrltag+'>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && (Lepton_pdgId[0]*Lepton_pdgId[1])>0'
SSP = nTightLepton + '==2 && mll'+ctrltag+'>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && Lepton_pdgId[0]<0 && Lepton_pdgId[1]<0'
SSM = nTightLepton + '==2 && mll'+ctrltag+'>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && Lepton_pdgId[0]>0 && Lepton_pdgId[1]>0'

LL = 'fabs(Lepton_pdgId[0])==fabs(Lepton_pdgId[1])'
DF = 'fabs(Lepton_pdgId[0])!=fabs(Lepton_pdgId[1])'
EE = 'fabs(Lepton_pdgId[0])==11 && fabs(Lepton_pdgId[1])==11'
MM = 'fabs(Lepton_pdgId[0])==13 && fabs(Lepton_pdgId[1])==13'

T0 = '('+ElectronWP+'[0]+'+MuonWP+'[0])'
T1 = '('+ElectronWP+'[1]+'+MuonWP+'[1])'
T2 = '('+ElectronWP+'[2]+'+MuonWP+'[2])'

LepId2of3 = nLooseLepton+'==3 && ('+T0+'+'+T1+'+'+T2+')==2'

C2 = '(Lepton_pdgId[0]*Lepton_pdgId[1])'
C1 = '(Lepton_pdgId[0]*Lepton_pdgId[2])'
C0 = '(Lepton_pdgId[1]*Lepton_pdgId[2])'
OCT = '('+C2+'*'+T0+'*'+T1+'+'+C1+'*'+T0+'*'+T2+'+'+C0+'*'+T1+'*'+T2+')<0'

MET_significance = 'MET_significance'

btagAlgo = 'btagDeepB'
bTagWP = 'M'
bTagPtCut  = '20.'
if 'pt25' in opt.tag: bTagPtCut  = '25.' 
if 'pt30' in opt.tag: bTagPtCut  = '30.' 
bTagEtaMax = '2.4' if ('2016' in opt.tag) else '2.5'
if '2016' in yeartag: 
    bTagCut = '0.6321'
    btagWP  = '2016'
elif '2017' in yeartag: 
    bTagCut = '0.4941'
    btagWP  = '2017'
elif '2018' in yeartag: 
    bTagCut = '0.4184'
    btagWP  = '2018'
btagWP += bTagWP

bTagPass = '(leadingPtTagged_'+btagAlgo+bTagWP+'_1c>='+bTagPtCut+')' 
bTagVeto = '!'+bTagPass
b2TagPass = bTagPass.replace('leadingPt', 'trailingPt')

btagWeight1tag = 'btagWeight_1tag_'+btagAlgo+bTagWP+'_1c'
if 'pt25' in opt.tag: btagWeight1tag += '_Pt25'
if 'pt30' in opt.tag: btagWeight1tag += '_Pt30'
btagWeight0tag = '(1.-'+btagWeight1tag+')'
btagWeight2tag = btagWeight1tag.replace('_1tag_', '_2tag_')

ISRCut = 'CleanJet_pt[0]>150. && CleanJet_pt[0]!=leadingPtTagged_'+btagAlgo+bTagWP+'_1c && acos(cos(ptmiss_phi-CleanJet_phi[0]))>2.5'
ISRCutData = ' '+ISRCut+' && '
ISRCutMC   = '&& '+ISRCut

### MET Filters # https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#UL_data (checked on may20)
METFilters_Common = 'Flag_goodVertices*Flag_globalSuperTightHalo2016Filter*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter*Flag_BadPFMuonDzFilter' 

if '2017' in opt.tag or '2018' in opt.tag :
    MetFilters_Common += '*Flag_ecalBadCalibFilter'
    if 'noisyhits' in opt.tag: METFilters_Common += '*Flag_hfNoisyHitsFilter'
METFilters_MC     = METFilters_Common
METFilters_Data   = METFilters_Common + '*Flag_eeBadScFilter'
METFilters_FS     = METFilters_Common



### EE Noise in 2017 and HEM Issue in 2018

VetoEENoise, VetoHEMdata, VetoHEMmc  = '1.', '1.', '1.'
if '2017' in yeartag and 'EENoise' in opt.tag:
    VetoEENoise = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==0)'
    if 'EENoiseHT' in opt.tag:
        VetoEENoise = '('+HTForwardSoft+'<40.)'
    elif 'EENoiseDPhiHard' in opt.tag:
        VetoEENoise = '(Sum$('+dPhieenoiseptmiss_hard+'>1.257)==0)'
    elif 'EENoiseDPhiSoftPt50' in opt.tag:
        VetoEENoise = '(Sum$('+dPhieenoiseptmiss_pt50+'>0. && '+dPhieenoiseptmiss_pt50+'<0.96)==0)'
    elif 'EENoiseDPhiSoft' in opt.tag:
        VetoEENoise = '(Sum$('+dPhieenoiseptmiss_pt30+'>0. && '+dPhieenoiseptmiss_pt30+'<0.96)==0)'
    elif 'EENoiseDPhi' in opt.tag:
        VetoEENoise = '(Sum$('+dPhieenoiseptmiss_hard+'>1.257)==0 && Sum$('+dPhieenoiseptmiss_pt50+'>0. && '+dPhieenoiseptmiss_pt50+'<0.96)==0)'
    if 'Veto' in opt.tag:
        #VetoEENoise = '(1. - '+VetoEENoise+')'
        VetoEENoise = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'

elif '2018' in yeartag and 'HEM' in opt.tag:
    hemPtCut = '20.' if 'HEM20' in opt.tag else '30.' 
    VetoHEMele  = '(Sum$(Electron_pt>'+hemPtCut+' && Electron_eta>-3.0 && Electron_eta<-1.4 && Electron_phi>-1.57 && Electron_phi<-0.87)==0)'
    VetoHEMjet  = '(Sum$(Jet_pt>'+hemPtCut+' && Jet_eta>-3.2 && Jet_eta<-1.2 && Jet_phi>-1.77 && Jet_phi<-0.67)==0)'
    VetoHEM     = '('+VetoHEMele+' && '+VetoHEMjet+')'
    VetoHEMdata = '(run<319077 || '+VetoHEM+')'
    VetoHEMmc   = '('+VetoHEM+' + (1.-'+VetoHEM+')*0.35225285)'

### Trigger Efficiencies

TriggerEff = 'TriggerEffWeight_2l' if 'Trigger' not in opt.tag else '1.'

if 'WZtoWW' in opt.tag or 'WZVal' in opt.tag or 'ZZVal' in opt.tag or 'ttZ' in opt.tag or 'FitCRZZ' in opt.tag or 'FitCRWZ' in opt.tag:
    TriggerEff = 'TriggerEffWeight_3l'

### MC weights

# generation weights

XSWeight       = 'baseW*genWeight'

# lepton weights

if '2016' in opt.tag:
    LepRecoSF      = '((abs(Lepton_pdgId[LEPIDX])==13)+(Lepton_RecoSF[LEPIDX]*(abs(Lepton_pdgId[LEPIDX])==11)))'
    RecoWeight     = LepRecoSF.replace('LEPIDX', '0') + '*' + LepRecoSF.replace('LEPIDX', '1')
else: 
    RecoWeight     = 'Lepton_RecoSF[0]*Lepton_RecoSF[1]'
EleWeight      = ElectronSF+'_IdIsoSF[0]*'+ElectronSF+'_IdIsoSF[1]'
MuoWeight      = MuonSF+'_IdIsoSF[0]*'+MuonSF+'_IdIsoSF[1]'
LepWeight      = EleWeight + '*' + MuoWeight
EleWeightFS    = EleWeight.replace('IdIsoSF', 'FastSimSF')
MuoWeightFS    = MuoWeight.replace('IdIsoSF', 'FastSimSF')
LepWeightFS    = LepWeight.replace('IdIsoSF', 'FastSimSF')

weightReco  = '('+RecoWeight.replace('RecoSF', 'RecoSF_Syst')+')/('+RecoWeight+')'
weightEle   = '('+EleWeight.replace('IdIsoSF', 'IdIsoSF_Syst')+')/('+EleWeight+')'
weightMuo   = '('+MuoWeight.replace('IdIsoSF', 'IdIsoSF_Syst')+')/('+MuoWeight+')'
weightLep   = '('+LepWeight.replace('IdIsoSF', 'IdIsoSF_Syst')+')/('+LepWeight+')'
weightEleFS = weightEle.replace('IdIsoSF', 'FastSimSF')
weightMuoFS = weightMuo.replace('IdIsoSF', 'FastSimSF')
weightLepFS = weightLep.replace('IdIsoSF', 'FastSimSF')

leptonSF = { 
    #'trkreco'         : { 'type' : 'shape', 'weight' : [ '1.', '1.' ] }, ->  no scale factor required
    'lepreco'         : { 'type' : 'shape', 'weight' : [ weightReco.replace('Syst', 'Up'), weightReco.replace('Syst', 'Down') ] },
    #'electronIdIso'   : { 'type' : 'shape', 'weight' : [ weightEle.replace('Syst', 'Up'), weightEle.replace('Syst', 'Down') ] },
    #'muonIdIso'       : { 'type' : 'shape', 'weight' : [ weightMuo.replace('Syst', 'Up'), weightMuo.replace('Syst', 'Down') ] },
    'leptonIdIso'     : { 'type' : 'shape', 'weight' : [ weightLep.replace('Syst', 'Up'), weightLep.replace('Syst', 'Down') ] }, 
    #'electronIdIsoFS' : { 'type' : 'shape', 'weight' : [ weightEleFS.replace('Syst', 'Up'), weightEleFS.replace('Syst', 'Down') ] },
    #'muonIdIsoFS'     : { 'type' : 'shape', 'weight' : [ weightMuoFS.replace('Syst', 'Up'), weightMuoFS.replace('Syst', 'Down') ] },
    #'leptonIdIsoFS'   : { 'type' : 'shape', 'weight' : [ weightLepFS.replace('Syst', 'Up'), weightLepFS.replace('Syst', 'Down') ] }, 
    'leptonIdIsoFS'   : { 'type' : 'lnN', 'weight' : '1.04' },   
}

# nonprompt lepton rate

#nonpromptLep = { 'rate' : '1.00', 'rateUp' : '1.50', 'rateDown' : '0.50' } 
#nonpromptLep = { 'rate' : '1.08', 'rateUp' : '1.29', 'rateDown' : '0.87' } 
if '2016' in yeartag:   nonpromptLep = { 'rate' : '1.23', 'rateUp' : '1.31', 'rateDown' : '1.15' } 
elif '2017' in yeartag: nonpromptLep = { 'rate' : '1.48', 'rateUp' : '1.62', 'rateDown' : '1.37' } 
elif '2018' in yeartag: nonpromptLep = { 'rate' : '1.30', 'rateUp' : '1.36', 'rateDown' : '1.21' } 
if 'nonpromptSF' in opt.tag:
    # To check that mismodelling doesnt change much the limits
    if '2016' in yeartag:   nonpromptLep = { 'rate' : '1.00', 'rateUp' : '1.23', 'rateDown' : '0.77' } 
    elif '2017' in yeartag: nonpromptLep = { 'rate' : '1.00', 'rateUp' : '1.48', 'rateDown' : '0.52' } 
    elif '2018' in yeartag: nonpromptLep = { 'rate' : '1.00', 'rateUp' : '1.30', 'rateDown' : '0.70' } 

promptLeptons = 'Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1]'
nonpromptLepSF      = '( ' + promptLeptons + ' + (1. - ' + promptLeptons + ')*' + nonpromptLep['rate']      + ')'
nonpromptLepSF_Up   = '( ' + promptLeptons + ' + (1. - ' + promptLeptons + ')*' + nonpromptLep['rateUp']    + ')'
nonpromptLepSF_Down = '( ' + promptLeptons + ' + (1. - ' + promptLeptons + ')*' + nonpromptLep['rateDown']  + ')'

# global SF weights 

SFweightCommon = 'puWeight*' + TriggerEff + '*' + RecoWeight + '*' + LepWeight + '*' + nonpromptLepSF
if '2016' in yeartag or '2017' in yeartag: 
    SFweightCommon += '*PrefireWeight'
if '2017' in yeartag and 'EENoise' in opt.tag:
    SFweightCommon += '*' + VetoEENoise
if '2018' in yeartag and 'HEM' in opt.tag: 
    SFweightCommon += '*' + VetoHEMmc
SFweight       = SFweightCommon + '*' + METFilters_MC
SFweightFS     = SFweightCommon + '*' + METFilters_FS + '*' + LepWeightFS + '*isrW'

# Primary Vertex Reweighting

if 'pu1sigma' in opt.tag: 
    SFweight = SFweight.replace('puWeight', 'puWeightUp')
elif 'pu2sigma' in opt.tag:
    SFweight = SFweight.replace('puWeight', '(2.*(puWeightUp-puWeight)+puWeight)')	

if 'PVw' in opt.tag:
    if '2016' in yeartag:
        SFweight += '*((1./0.97916503)*((1.11250e+00)+(1.69184e-02)*PV_npvs+(-1.30092e-03)*PV_npvs*PV_npvs+(-1.99571e-05)*PV_npvs*PV_npvs*PV_npvs+(1.10773e-06)*PV_npvs*PV_npvs*PV_npvs*PV_npvs))'
    elif '2017' in yeartag: 
        SFweight += '*((1./1.0028780)*((8.05485e-01)+(-2.30668e-02)*PV_npvs+(2.62330e-03)*PV_npvs*PV_npvs+(-7.65300e-05)*PV_npvs*PV_npvs*PV_npvs+(7.54356e-07)*PV_npvs*PV_npvs*PV_npvs*PV_npvs))'
    elif '2018' in yeartag: 
        SFweight += '*((1./0.95395364)*((9.48824e-01)+(-3.22506e-02)*PV_npvs+(3.42005e-03)*PV_npvs*PV_npvs+(-1.42342e-04)*PV_npvs*PV_npvs*PV_npvs+(2.03952e-06)*PV_npvs*PV_npvs*PV_npvs*PV_npvs))'
    
### Special weights

# background cross section uncertainties and normalization scale factors

isDatacardOrPlot = hasattr(opt, 'outputDirDatacard') or hasattr(opt, 'postFit')

normBackgrounds = {}

if 'SignalRegions' in opt.tag or 'BackSF' in opt.tag:

    normBackgrounds['STtW']      = { 'all'   : { 'scalefactor' : { '1.00' : '0.10' }, 'selection' : '1.' } }
    normBackgrounds['ttW']       = { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'selection' : '1.' } } 
    normBackgrounds['Higgs']     = { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'selection' : '1.' } } 
    normBackgrounds['VZ']        = { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'selection' : '1.' } } 
    normBackgrounds['VVV']       = { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'selection' : '1.' } } 
    normBackgrounds['DY']        = { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'selection' : '1.' } }

    if 'FitCR' not in opt.tag:

        if '2016' in yeartag:
            normBackgrounds['WZ']        = { 'all'   : { 'scalefactor' : { '0.86' : '0.08' }, 'selection' : '1.' } }
            normBackgrounds['ttZ']       = { 'all'   : { 'scalefactor' : { '1.29' : '0.28' }, 'selection' : '1.' } }
            normBackgrounds['ZZTo2L2Nu'] = { 'nojet' : { 'scalefactor' : { '1.13' : '0.31' }, 'cuts' : [ '_NoJet', '_Veto' ],         'selection' : '(nCleanJet==0)' },
                                             'notag' : { 'scalefactor' : { '1.25' : '0.23' }, 'cuts' : [ '_NoTag', '_Tag', '_Veto' ], 'selection' : '(nCleanJet>=1)' },
                                           }
            if 'kZZmass' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '1.00' : '0.27' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '1.12' : '0.20' }
                #normBackgrounds['ZZTo2L2Nu']['veto']['scalefactor'] = { '1.08' : '0.16' }
            elif 'kZZpt' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.91' : '0.25' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.85' : '0.16' }
            elif 'kZZdphi' in opt.tag: 
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '1.00' : '0.27' } 
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '1.13' : '0.21' } 

        elif '2017' in yeartag:
            normBackgrounds['WZ']        = { 'all'   : { 'scalefactor' : { '1.04' : '0.08' }, 'selection' : '1.' } }
            normBackgrounds['ttZ']       = { 'all'   : { 'scalefactor' : { '1.45' : '0.27' }, 'selection' : '1.' } }
            normBackgrounds['ZZTo2L2Nu'] = { 'nojet' : { 'scalefactor' : { '0.83' : '0.25' }, 'cuts' : [ '_NoJet', '_Veto' ],         'selection' : '(nCleanJet==0)' },  
                                             'notag' : { 'scalefactor' : { '0.94' : '0.18' }, 'cuts' : [ '_NoTag', '_Tag', '_Veto' ], 'selection' : '(nCleanJet>=1)' },
                                           }
            if 'kZZmass' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.74' : '0.22' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.84' : '0.16' }
                #normBackgrounds['ZZTo2L2Nu']['veto']['scalefactor'] = { '0.81' : '0.13' }
            elif 'kZZpt' in opt.tag: 
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.68' : '0.20' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.66' : '0.12' }
            elif 'kZZdphi' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.74' : '0.22' } 
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.86' : '0.16' }        

        elif '2018' in yeartag:
            normBackgrounds['WZ']        = { 'all'   : { 'scalefactor' : { '0.86' : '0.06' }, 'selection' : '1.' } }
            normBackgrounds['ttZ']       = { 'all'   : { 'scalefactor' : { '1.43' : '0.22' }, 'selection' : '1.' } }
            normBackgrounds['ZZTo2L2Nu'] = { 'nojet' : { 'scalefactor' : { '1.08' : '0.23' }, 'cuts' : [ '_NoJet', '_Veto' ],         'selection' : '(nCleanJet==0)' },
                                             'notag' : { 'scalefactor' : { '0.83' : '0.14' }, 'cuts' : [ '_NoTag', '_Tag', '_Veto' ], 'selection' : '(nCleanJet>=1)' },
                                           }
            if 'kZZmass' in opt.tag:   
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.95' : '0.20' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.75' : '0.13' }
                #normBackgrounds['ZZTo2L2Nu']['veto']['scalefactor'] = { '0.81' : '0.11' }
            elif 'kZZpt' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.88' : '0.19' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.58' : '0.10' }
            elif 'kZZdphi' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.96' : '0.20' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.76' : '0.13' }

        if 'BackSF' in opt.tag: 
            if 'ZZValidationRegion' in opt.tag or 'ttZValidationRegion' in opt.tag or 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag or 'DYValidationRegion' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['cuts'] = [ 'ptmiss-160' ]
                normBackgrounds['ZZTo2L2Nu']['notag']['cuts'] = [ 'ptmiss-160' ]
                normBackgrounds['ZZTo2L2Nu']['nojet']['selection'] = '(nCleanJet==0 && ptmiss'+ctrltag+'>=160.)'
                normBackgrounds['ZZTo2L2Nu']['notag']['selection'] = '(nCleanJet>=1 && ptmiss'+ctrltag+'>=160.)'
                normBackgrounds['ZZTo4L'] = normBackgrounds['ZZTo2L2Nu']
                normBackgrounds['ttZ']['all']['cuts'] = [ 'ptmiss-160' ] 
                normBackgrounds['ttZ']['all']['selection'] = '(ptmiss'+ctrltag+'>=160.)'
                normBackgrounds['WZ']['all']['cuts'] = [ 'ptmiss-160' ]
                normBackgrounds['WZ']['all']['selection'] = '(ptmiss'+ctrltag+'>=160.)'

# top pt reweighting

Top_pTrw = '(TMath::Sqrt( TMath::Exp(0.0615-0.0005*topGenPt) * TMath::Exp(0.0615-0.0005*antitopGenPt) ) )'
centralTopPt = Top_pTrw 
systematicTopPt = '1.'

### Data info

if '2016' in yeartag or '2017' in yeartag :

    if '2016' in opt.tag : # TODO 
        DataRun = [ 
            ['B','Run2016B-Nano25Oct2019_ver2-v1'],
            ['C','Run2016C-Nano25Oct2019-v1'] ,
            ['D','Run2016D-Nano25Oct2019-v1'] ,
            ['E','Run2016E-Nano25Oct2019-v1'] ,
            ['F','Run2016F-Nano25Oct2019-v1'] ,
            ['G','Run2016G-Nano25Oct2019-v1'] ,
            ['H','Run2016H-Nano25Oct2019-v1'] 
        ]
    elif '2017' in yeartag :
        DataRun = [ 
            ['B','Run2017B-UL2017_MiniAODv1_NanoAODv2-v1'],
            ['C','Run2017C-UL2017_MiniAODv1_NanoAODv2-v1'],
            ['D','Run2017D-UL2017_MiniAODv1_NanoAODv2-v1'],
            ['E','Run2017E-UL2017_MiniAODv1_NanoAODv2-v1'],
            ['F','Run2017F-UL2017_MiniAODv1_NanoAODv2-v1'],
        ]

    DataSets = ['MuonEG','DoubleMuon','SingleMuon','DoubleEG','SingleElectron']

    DataTrig = {
        'MuonEG'         : '(Trigger_ElMu)' ,
        'DoubleMuon'     : '(!Trigger_ElMu && Trigger_dblMu)' ,
        'SingleMuon'     : '(!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu)' ,
        'DoubleEG'       : '(!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && Trigger_dblEl)' ,
        'SingleElectron' : '(!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && !Trigger_dblEl && Trigger_sngEl)' ,
    }

elif '2018' in yeartag :

    DataRun = [ 
        ['A','Run2018A-UL2018_MiniAODv1_NanoAODv2-v1'] ,
        ['B','Run2018B-UL2018_MiniAODv1_NanoAODv2-v1'] ,
        ['C','Run2018C-UL2018_MiniAODv1_NanoAODv2-v1'] ,
        ['D','Run2018D-UL2018_MiniAODv1_NanoAODv2-v1'] ,
    ]

    if '2018AB' in opt.tag :
        DataRun.remove( ['C','Run2018C-UL2018_MiniAODv1_NanoAODv2-v1'] )
        DataRun.remove( ['D','Run2018D-UL2018_MiniAODv1_NanoAODv2-v1'] )

    if '2018CD' in opt.tag :
        DataRun.remove( ['A','Run2018A-UL2018_MiniAODv1_NanoAODv2-v1'] )
        DataRun.remove( ['B','Run2018B-UL2018_MiniAODv1_NanoAODv2-v1'] )

    DataSets = ['MuonEG','DoubleMuon','SingleMuon','EGamma']

    DataTrig = {
        'MuonEG'         : '(Trigger_ElMu)' ,
        'DoubleMuon'     : '(!Trigger_ElMu && Trigger_dblMu)' ,
        'SingleMuon'     : '(!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu)' ,
        'EGamma'         : '(!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && (Trigger_sngEl || Trigger_dblEl))' ,
    }

### Backgrounds

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:

    ttbarFlag = ''
    samples['ttbar'] = {    'name'   : getSampleFiles(directoryBkg,'TTTo2L2Nu'+ttbarFlag,False,treePrefix),
                            'weight' : XSWeight+'*'+SFweight+'*'+centralTopPt ,
                        }

    if 'btagefficiencies' in opt.tag:

        samples['T2tt'] = { 'name'   : getSampleFiles(directorySig,'T2tt__mStop-400to1200',False,treePrefix),
                            'weight' : XSWeight+'*'+SFweightFS ,
                            }

    if 'btagefficiencies' not in opt.tag and 'Test' not in opt.tag:
    
        #tWext = '_ext1' if ('2018' in yeartag) else '' # TODO missing 
        #samples['STtW']    = {    'name'   :   getSampleFiles(directoryBkg,'ST_tW_antitop'+tWext,False,treePrefix) +
        #                                       getSampleFiles(directoryBkg,'ST_tW_top'+tWext,    False,treePrefix),
        #                          'weight' : XSWeight+'*'+SFweight ,
        #                     }

        ttZToLLext = '' # TODO missing 2016
        ttZToQQext = ''
        samples['ttZ']   = {    'name'   :   getSampleFiles(directoryBkg,'TTZToLLNuNu_M-10'+ttZToLLext,False,treePrefix) + 
                                             getSampleFiles(directoryBkg,'TTZToQQ'         +ttZToQQext,False,treePrefix),
                                'weight' : XSWeight+'*'+SFweight ,
                                }
        
        ttWToLLext = '' # TODO missing 2016
        samples['ttW']   = {    'name'   :   getSampleFiles(directoryBkg,'TTWJetsToLNu'+ttWToLLext,False,treePrefix) ,#+
                                             #getSampleFiles(directoryBkg,'TTWJetsToQQ',False,treePrefix), # TODO missing 
                                'weight' : XSWeight+'*'+SFweight ,
                                }

        # TODO missing
        #samples['WW']    = {    'name'   :   getSampleFiles(directoryBkg,'WWTo2L2Nu',           False,treePrefix),
        #                        'weight' : XSWeight+'*'+SFweight ,
        #}
        #if '2016' in yeartag : 
        #    samples['WW']['name'] += getSampleFiles(directoryBkg,'GluGluWWTo2L2Nu_MCFM',False,treePrefix) 
        #else : 
        #    samples['WW']['name'] += getSampleFiles(directoryBkg,'GluGluToWWToENEN',False,treePrefix) \
        #                           + getSampleFiles(directoryBkg,'GluGluToWWToENMN',False,treePrefix) \
        #                           + getSampleFiles(directoryBkg,'GluGluToWWToENTN',False,treePrefix) \
        #                           + getSampleFiles(directoryBkg,'GluGluToWWToMNEN',False,treePrefix) \
        #                           + getSampleFiles(directoryBkg,'GluGluToWWToMNMN',False,treePrefix) \
        #                           + getSampleFiles(directoryBkg,'GluGluToWWToMNTN',False,treePrefix) \
        #                           + getSampleFiles(directoryBkg,'GluGluToWWToTNEN',False,treePrefix) \
        #                           + getSampleFiles(directoryBkg,'GluGluToWWToTNMN',False,treePrefix) \
        #                           + getSampleFiles(directoryBkg,'GluGluToWWToTNTN',False,treePrefix)

        # TODO missing
        #WZext = '_ext1' if ('2018' in yeartag) else ''
        #samples['WZ']    = {    'name'   :   getSampleFiles(directoryBkg,'WZTo3LNu'+WZext,False,treePrefix),
        #                        'weight' : XSWeight+'*'+SFweight ,
        #                        }

        ZZext = ''
        samples['ZZTo2L2Nu']  = {  'name'   : getSampleFiles(directoryBkg,'ZZTo2L2Nu'+ZZext,False,treePrefix) ,#+
                                              #getSampleFiles(directoryBkg,'ggZZ2e2n',       False,treePrefix) + # TODO missing for 2016 and 2017
                                              #getSampleFiles(directoryBkg,'ggZZ2m2n',       False,treePrefix),  # TODO missing for 2016 and 2017
                                   'weight' : XSWeight+'*'+SFweight ,
                                 }

        # TODO missing HT binned samples
        DYM10ext = ''
        DYMlow = 'M-4to50' 
        DYMlowHT70ext, DYMlowHT100ext, DYMlowHT200ext, DYMlowHT400ext, DYMlowHT600ext = '', '', '', '', '' 
        DYM50ext = ''
        DYMhighHT70ext, DYMhighHT100ext, DYMhighHT200ext, DYMhighHT400ext, DYMhighHT600ext, DYMhighHT800ext, DYMhighHT1200ext, DYMhighHT2500ext = '', '', '', '', '', '', '', ''
        samples['DY'] = { 'name' : getSampleFiles(directoryBkg,'DYJetsToLL_M-10to50-LO'+DYM10ext,        False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-70to100'+DYMlowHT70ext, False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-100to200'+DYMlowHT100ext,False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-200to400'+DYMlowHT200ext,False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-400to600'+DYMlowHT400ext,False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-600toInf'+DYMlowHT600ext,False,treePrefix) +
                                   getSampleFiles(directoryBkg,'DYJetsToLL_M-50-LO'+DYM50ext,   False,treePrefix) ,#+
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-70to100'+DYMhighHT70ext,    False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-100to200'+DYMhighHT100ext,   False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-200to400'+DYMhighHT200ext,   False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-400to600'+DYMhighHT400ext,   False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-600to800'+DYMhighHT600ext,   False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-800to1200'+DYMhighHT800ext,  False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-1200to2500'+DYMhighHT1200ext, False,treePrefix) +
                                   #getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-2500toInf'+DYMhighHT2500ext,  False,treePrefix) ,
                          'weight' : XSWeight+'*'+SFweight ,
                        }  
        #addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO'+DYM10ext,  'LHE_HT<70.0')
        #addSampleWeight(samples,'DY','DYJetsToLL_M-50-LO'+DYM50ext, 'LHE_HT<70.0')

        # TODO missing
        #ggHWWgen = ''
        #ggHTText = ''
        #samples['Higgs']   = {  'name'   :   getSampleFiles(directoryBkg,'GluGluHToWWTo2L2Nu'+ggHWWgen+'_M125',False,treePrefix) + 
        #                                     getSampleFiles(directoryBkg,'GluGluHToTauTau_M125'+ggHTText,      False,treePrefix) + 
        #                                     getSampleFiles(directoryBkg,'VBFHToWWTo2L2Nu_M125',               False,treePrefix) + 
        #                                     getSampleFiles(directoryBkg,'VBFHToTauTau_M125',                  False,treePrefix) + 
        #                                     getSampleFiles(directoryBkg,'HWplusJ_HToWW_M125',                 False,treePrefix) +  
        #                                     getSampleFiles(directoryBkg,'HWplusJ_HToTauTau_M125',             False,treePrefix) + 
        #                                     getSampleFiles(directoryBkg,'HWminusJ_HToWW_M125',                False,treePrefix) + 
        #                                     getSampleFiles(directoryBkg,'HWminusJ_HToTauTau_M125',            False,treePrefix) ,
        #                        'weight' : XSWeight+'*'+SFweight ,
        #                        }

        # TODO missing
        #samples['VZ']    = {    'name'   :   getSampleFiles(directoryBkg,'WZTo2L2Q',False,treePrefix) + 
        #                                     getSampleFiles(directoryBkg,'ZZTo2L2Q',False,treePrefix),
        #                        'weight' : XSWeight+'*'+SFweight
        #}
        
        samples['VVV']   = {    'name'   :   getSampleFiles(directoryBkg,'WWW',False,treePrefix) + 
                                             #getSampleFiles(directoryBkg,'WWZ',False,treePrefix) + # TODO missing for 2016 and 2018
                                             #getSampleFiles(directoryBkg,'WZZ',False,treePrefix) + # TODO missing
                                             getSampleFiles(directoryBkg,'ZZZ',False,treePrefix) ,#+
                                             #getSampleFiles(directoryBkg,'WWG',False,treePrefix), # TODO missing
                                'weight' : XSWeight+'*'+SFweight ,
                                }
        
        if 'ZZValidationRegion' in opt.tag or 'ttZ' in opt.tag or 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag or 'FitCRWZ' in opt.tag or 'FitCRZZ' in opt.tag or ('FitCR' in opt.tag and isDatacardOrPlot):
            
            ZZ4Lext = '' # TODO missing
            #samples['ZZTo4L']   = {    'name'   :   getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ZZTo4L'+ZZ4Lext, False,treePrefix) + 
            #                                        getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ4e',              False,treePrefix) +
            #                                        getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ4m',              False,treePrefix) +
            #                                        getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ4t',              False,treePrefix) +
            #                                        getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ2e2m',            False,treePrefix) +
            #                                        getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ2e2t',            False,treePrefix) +
            #                                        getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ2m2t',            False,treePrefix) +
            #                                        getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'VBFHToZZTo4L_M125',   False,treePrefix) +
            #                                        getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'GluGluHToZZTo4L_M125',False,treePrefix),
            #                           'weight' : XSWeight+'*'+SFweight ,
            #                           'JobsPerSample' : 6,
            #                           'isControlSample' : 1,
            #                       }

            #for kZZvariable in [ 'kZZmass', 'kZZdphi', 'kZZpt' ]:
            #    if kZZvariable in opt.tag:  
            #        addSampleWeight(samples,'ZZTo4L','ZZTo4L'+ZZ4Lext, kZZvariable.replace('kZZ', 'kZZ_'))

        if 'SameSignValidationRegion' in opt.tag:
    
            ttSemilepFlag = '' # TODO missing for 2016
            samples['ttSemilep'] = { 'name'   : getSampleFiles(directoryBkg,'TTToSemiLeptonic'+ttSemilepFlag,False,treePrefix),
                                     'weight' : XSWeight+'*'+SFweight ,
                                     'isControlSample' : 1,
                                    }

if 'Backgrounds' in opt.sigset and opt.sigset not in 'Backgrounds' and 'Backgrounds-' not in opt.sigset:

    sampleToRemove = [ ] 

    for sample in samples:
        if 'Veto' in opt.sigset:
            if sample in opt.sigset:
                sampleToRemove.append(sample)
        elif 'Backgrounds'+sample!= opt.sigset:
            sampleToRemove.append(sample)

    for sample in sampleToRemove:
        del samples[sample]

for sample in samples:
    samples[sample]['isSignal']  = 0
    samples[sample]['isDATA']    = 0
    samples[sample]['isFastsim'] = 0
    samples[sample]['suppressNegative'] = ['all']
    samples[sample]['suppressNegativeNuisances'] = ['all']
    samples[sample]['suppressZeroTreeNuisances'] = ['all']

### Data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    samples['DATA']  = {   'name': [ ] ,    
                           'weight' : METFilters_Data+'*'+VetoHEMdata+'*'+VetoEENoise, 
                           'weights' : [ ],
                           'isData': ['all'],
                           'isSignal'  : 0,
                           'isDATA'    : 1, 
                           'isFastsim' : 0
                       }

    for Run in DataRun :
        for DataSet in DataSets :
            datasetName = DataSet+'_'+Run[1]
            if DataSet=='SingleMuon' and 'Run2017F' in Run[1]: datasetName = datasetName.replace('-v1', '-v2')
            if DataSet=='DoubleMuon' and 'Run2018B' in Run[1]: datasetName = datasetName.replace('-v1', '-v2')
            FileTarget = getSampleFiles(directoryData,datasetName,True,treePrefix)
            for iFile in FileTarget:
                samples['DATA']['name'].append(iFile)
                samples['DATA']['weights'].append(DataTrig[DataSet])

if 'MET' in opt.sigset:

    if 'cern' in SITE: 
        print 'MET datasets not available on lxplus, please use gridui' 

    metTriggers = 'Alt$(HLT_PFMET120_PFMHT120_IDTight, 0)==1'
    if '2016' in yeartag: 
        metTriggers += ' || Alt$(HLT_PFMET90_PFMHT90_IDTight, 0)==1'
        metTriggers += ' || Alt$(HLT_PFMET100_PFMHT100_IDTight, 0)==1'
        metTriggers += ' || Alt$(HLT_PFMET110_PFMHT110_IDTight, 0)==1'
    elif '2017' in yeartag or '2018' in yeartag: 
        metTriggers += ' || Alt$(HLT_PFMET120_PFMHT120_IDTight_PFHT60, 0)==1'

    samples['DATA']  = {   'name': [ ] ,
                           'weight' : METFilters_Data+'*'+VetoHEMdata+'*'+VetoEENoise,
                           'weights' : [ ],
                           'isData': ['all'],
                           'isSignal'  : 0,
                           'isDATA'    : 1,
                           'isFastsim' : 0
                       }

    directoryMET = directoryData.split('__hadd')[0]+'__hadd/'
    if 'TriggerLatino' in opt.tag: directoryMET = directoryMET.replace('DATASusy', 'DATALatino')

    for Run in DataRun :
        datasetName = 'MET_'+Run[1]
        if 'Run2018B' in Run[1]: datasetName = datasetName.replace('-v1', '-v4')
        FileTarget = getSampleFiles(directoryMET,datasetName,True,treePrefix)
        for iFile in FileTarget:
            samples['DATA']['name'].append(iFile)
            if 'Run2017B' in Run[1]:
                samples['DATA']['weights'].append( '(Alt$(HLT_PFMET120_PFMHT120_IDTight, 0)==1 || Alt$(HLT_PFMET110_PFMHT110_IDTight, 0)==1)' )
            elif 'Run2017C' in Run[1] or 'Run2017D' in Run[1] or 'Run2017E' in Run[1] or 'Run2017F' in Run[1]:
                samples['DATA']['weights'].append( '(Alt$(HLT_PFMET120_PFMHT120_IDTight, 0)==1)' )
            else:
                samples['DATA']['weights'].append( '('+metTriggers+')' )
            
### Files per job

#if hasattr(opt, 'batchSplit'):
    #if 'AsMuchAsPossible' in opt.batchSplit or 'Files' in opt.batchSplit: 
for sample in samples:
    if 'FilesPerJob' not in samples[sample]:
        ntrees = len(samples[sample]['name']) 
        multFactor = 6 if 'JobsPerSample' not in samples[sample] else int(samples[sample]['JobsPerSample'])
        samples[sample]['FilesPerJob'] = int(math.ceil(float(ntrees)/multFactor))

### Signals

exec(open('./signalMassPoints.py').read())

for model in signalMassPoints:
    if model in opt.sigset:

        isrObservable = 'ptISR' if ('T2' not in model and '2016' in opt.tag) else 'njetISR'

        for massPoint in signalMassPoints[model]:
            if massPointInSignalSet(massPoint, opt.sigset):

                #if  os.path.isfile('./Shapes/'+opt.tag.replace(yeartag, yeartag+'/')+'/Samples/plots_'+opt.tag+'_ALL_'+massPoint+'.root'): continue

                samples[massPoint] = { 'name'   : getSampleFiles(directorySig,signalMassPoints[model][massPoint]['massPointDataset'],False,treePrefix),
                                       'weight' : XSWeight+'*'+SFweightFS+'*'+signalMassPoints[model][massPoint]['massPointCut'] ,
                                       'FilesPerJob' : 2 ,
                                       'suppressNegative':['all'],
                                       'suppressNegativeNuisances' :['all'],
                                       'suppressZeroTreeNuisances' : ['all'],
                                       'isrObservable' : isrObservable,
                                       'isSignal'  : 1,
                                       'isDATA'    : 0, 
                                       'isFastsim' : 1
                                   }
                
