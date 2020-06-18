from ROOT import TCanvas, TLegend, TChain, TFile, TH1F
import fnmatch, os, math

#=============================================================================
#SETUP
#=============================================================================
signalDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
trailer="*"
baseCut = "baseW"
cuts = [baseCut, baseCut + " * (mt2ll > 20)", baseCut + " * (mt2ll > 40)", baseCut + " * (mt2ll > 60)", baseCut + " * (mt2ll > 80)", baseCut + " * (mt2ll > 100)"]

scalarFiles = [{'file': 'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_50'+ trailer +'.root', 'massPoint': 'scalar_Mchi_1_Mphi_50', 'events': 0},
               {'file': 'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_100'+ trailer +'.root', 'massPoint': 'scalar_Mchi_1_Mphi_100', 'events': 0},
               {'file': 'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_150'+ trailer +'.root', 'massPoint': 'scalar_Mchi_1_Mphi_150', 'events': 0},
               {'file': 'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_200'+ trailer +'.root', 'massPoint': 'scalar_Mchi_1_Mphi_200', 'events': 0},
               {'file': 'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_250'+ trailer +'.root', 'massPoint': 'scalar_Mchi_1_Mphi_250', 'events': 0},
               {'file': 'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_300'+ trailer +'.root', 'massPoint': 'scalar_Mchi_1_Mphi_300', 'events': 0},
               {'file': 'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_350'+ trailer +'.root', 'massPoint': 'scalar_Mchi_1_Mphi_350', 'events': 0},
               {'file': 'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_400'+ trailer +'.root', 'massPoint': 'scalar_Mchi_1_Mphi_400', 'events': 0},
               {'file': 'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_450'+ trailer +'.root', 'massPoint': 'scalar_Mchi_1_Mphi_450', 'events': 0},
               {'file': 'TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_500'+ trailer +'.root', 'massPoint': 'scalar_Mchi_1_Mphi_500', 'events': 0}]

pseudoscalarFiles = [{'file': 'TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_50'+ trailer +'.root', 'massPoint': 'pseudoscalar_Mchi_1_Mphi_50', 'events': 0},
         {'file': 'TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_100'+ trailer +'.root', 'massPoint': 'pseudoscalar_Mchi_1_Mphi_100', 'events': 0},
         {'file': 'TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_150'+ trailer +'.root', 'massPoint': 'pseudoscalar_Mchi_1_Mphi_150', 'events': 0},
         {'file': 'TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_200'+ trailer +'.root', 'massPoint': 'pseudoscalar_Mchi_1_Mphi_200', 'events': 0},
         {'file': 'TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_250'+ trailer +'.root', 'massPoint': 'pseudoscalar_Mchi_1_Mphi_250', 'events': 0},
         {'file': 'TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_300'+ trailer +'.root', 'massPoint': 'pseudoscalar_Mchi_1_Mphi_300', 'events': 0},
         {'file': 'TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_350'+ trailer +'.root', 'massPoint': 'pseudoscalar_Mchi_1_Mphi_350', 'events': 0},
         {'file': 'TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_400'+ trailer +'.root', 'massPoint': 'pseudoscalar_Mchi_1_Mphi_400', 'events': 0},
         {'file': 'TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_450'+ trailer +'.root', 'massPoint': 'pseudoscalar_Mchi_1_Mphi_450', 'events': 0},
         {'file': 'TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_500'+ trailer +'.root', 'massPoint': 'pseudoscalar_Mchi_1_Mphi_500', 'events': 0}]

singleFiles = [{'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi10__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi10', 'events': 0},
               {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi20__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi20', 'events': 0},
               {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi50__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi50', 'events': 0},
               {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi100__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi100', 'events': 0},
               {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi200__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi200', 'events': 0},
               {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi300__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi300', 'events': 0},
               {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi500__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi500', 'events': 0},
               {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi1000', 'events': 0}]

backgroundFiles = [{'file': 'TTTo2L2Nu'+trailer+'.root', 'massPoint': 'TTTo2L2Nu', 'events': 0},
                   {'file': 'ST_s-channel_ext1'+trailer+'.root', 'massPoint': 'singleTop', 'events': 0},
                   {'file': 'ST_t-channel_antitop'+trailer+'.root', 'massPoint': 'singleTop', 'events': 0},
                   {'file': 'ST_t-channel_top'+trailer+'.root', 'massPoint': 'singleTop', 'events': 0},
                   {'file': 'ST_tW-channel_antitop_ext1'+trailer+'.root', 'massPoint': 'singleTop', 'events': 0},
                   {'file': 'ST_tW-channel_top_ext1'+trailer+'.root', 'massPoint': 'singleTop', 'events': 0}]

#=============================================================================
#GET STARTED
#=============================================================================
def fillNumberEvents(files, cut):
    for f, fileDict in enumerate(files):
        filename = fileDict['file']
        massPoint = fileDict['massPoint']
        print('Now considering process... ' + massPoint)
        
        signalChain = TChain("Events")
        for actualFile in fnmatch.filter(os.listdir(signalDir), 'nanoLatino*' + filename + '*'):
            signalChain.AddFile(signalDir+actualFile)
            
        histname = 'hist_'+str(f)
        signalHist = TH1F(histname, 'Mass points distribution', 100, 0, 1000)
        signalChain.Draw('PuppiMET_pt >> ' + histname, cut)
            
        fileDict['events'] = signalHist.Integral(-1, -1)

for icut, cut in enumerate(cuts):
    fillNumberEvents(scalarFiles, cut)
    fillNumberEvents(pseudoscalarFiles, cut)
    fillNumberEvents(singleFiles, cut)
    fillNumberEvents(backgroundFiles, cut)
    print(backgroundFiles)
    print("Signal over background obtained for the cut " + str(icut + 1))
    totalBackground = 0
    for f, fileDict in enumerate(backgroundFiles):
        totalBackground += fileDict['events']

    print("============= SCALAR =============")
    for f, fileDict in enumerate(scalarFiles):
        print(fileDict['massPoint'] + ": " + str(fileDict['events']) + " events and S/sqrt(B) = " + str(fileDict['events']/math.sqrt(totalBackground)))

    print("============= PSEUDOSCALAR =============")

    print("============= SINGLE =============")

#COmpute the signal over sqrt(background) numbers to put in a table
