from ROOT import TCanvas, TLegend, TChain, TFile, TH1F
import fnmatch, os

#=============================================================================
#SETUP
#=============================================================================
variable = ["PuppiMET_pt", 100, 0, 500, "Puppi MET [GeV]"] #Variable name, bins, from, to, xaxis title
#variable = ["dark_pt", 50, 0, 800, "Dark pt [GeV]"] 
#variable = ["overlapingFactor", 40, 0, 4, "Overlapping factor"] 
#variable = ["nbJet", 6, 0, 6, "Loose deepCSV b-jets"] 
#variable = ["mblt", 16, 20, 350, "mblt [GeV]"] 

#signalDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
signalDir = "/eos/user/c/cprieels/work/SignalsPostProcessing/Pablo/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
#signalDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/"
category = "scalar"
trailer = "*"
#cuts = "mt2ll > 100 && (Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13 || (mll < 76 || mll > 106))"
cuts = "baseW * 1"

normalization = False
addBackground = False #Plot the ttbar on this plot as wel?
logy = False

files = [{'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_1_Mphi_50'+ trailer +'.root', 'massPoint': category + '_Mchi_1_Mphi_50'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_1_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_1_Mphi_100'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_1_Mphi_150'+ trailer +'.root', 'massPoint': category + '_Mchi_1_Mphi_150'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_1_Mphi_200'+ trailer +'.root', 'massPoint': category + '_Mchi_1_Mphi_200'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_1_Mphi_250'+ trailer +'.root', 'massPoint': category + '_Mchi_1_Mphi_250'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_1_Mphi_300'+ trailer +'.root', 'massPoint': category + '_Mchi_1_Mphi_300'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_1_Mphi_350'+ trailer +'.root', 'massPoint': category + '_Mchi_1_Mphi_350'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_1_Mphi_400'+ trailer +'.root', 'massPoint': category + '_Mchi_1_Mphi_400'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_1_Mphi_450'+ trailer +'.root', 'massPoint': category + '_Mchi_1_Mphi_450'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_1_Mphi_500'+ trailer +'.root', 'massPoint': category + '_Mchi_1_Mphi_500'}]

"""
files = [{'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_20_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_20_Mphi_100'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_30_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_30_Mphi_100'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_40_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_40_Mphi_100'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_45_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_45_Mphi_100'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_49_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_49_Mphi_100'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_51_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_51_Mphi_100'}]
         #{'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_55_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_55_Mphi_100'}] #Not available for pseudoscalar


files = [{'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi10__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi10'},
         {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi20__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi20'},
         {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi50__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi50'},
         {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi100__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi100'},
         {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi200__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi200'},
         {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi300__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi300'},
         {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi500__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi500'},
         {'file': 'DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000__part' + trailer + '.root', 'massPoint': 'tWChan_scalar_Mchi1_Mphi1000'}]
"""
if addBackground:
    files.append({'file': 'TTTo2L2Nu'+trailer+'.root', 'massPoint': 'TTTo2L2Nu'})

#=============================================================================
#GET STARTED
#=============================================================================
#Create and store the histograms...
massPoints = [] #For the legend
signalHistList = []

if len(files) == 2:
    colors = [632, 600] 
else:
    colors = [636, 635, 634, 633, 632, 807, 802, 801, 800, 798] 

if addBackground:
    colors.append(600)

for f, fileDict in enumerate(files):
    filename = fileDict['file']
    massPoint = fileDict['massPoint']
    print('Now considering mass point... ' + massPoint)

    signalChain = TChain("Events")
    for actualFile in fnmatch.filter(os.listdir(signalDir), 'nanoLatino*' + filename + '*'):
        signalChain.AddFile(signalDir+actualFile)
        
    histname = 'hist_'+str(f)
    signalHist = TH1F(histname, 'Mass points distribution', variable[1], variable[2], variable[3])

    signalChain.Draw(variable[0] + ' >> ' + histname, cuts)
    signalHist.SetDirectory(0)
    if normalization: signalHist.Scale(1./signalHist.Integral()) #Normalize the histo to unity
    signalHist.SetStats(0)
    signalHist.SetLineColor(colors[f])
    if len(files) == 2: signalHist.SetLineWidth(3)
    signalHist.GetXaxis().SetTitle(variable[4])
    
    massPoints.append(massPoint)
    signalHistList.append(signalHist)

#... And plot them
canvas = TCanvas( 'canvas', 'Signal samples', 200, 10, 700, 500)
canvas.SetGrid()
canvas.cd()

if len(files) == 2:
    legend = TLegend(0.60, 0.80, 0.90, 0.90)
else:
    legend = TLegend(0.55, 0.6, 0.75, 0.85) #Scalar high DM mass
    #legend = TLegend(0.46, 0.6, 0.75, 0.85) #Pseudoscalar high DM mass
    #legend = TLegend(0.55, 0.52, 0.75, 0.85) #Scalar high mediator mass
    #legend = TLegend(0.48, 0.52, 0.75, 0.85) #Pseudoscalar high mediator mass
    #legend = TLegend(0.45, 0.55, 0.75, 0.85) #Single top

for i, h in enumerate(signalHistList):
    h.Draw('same')

    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetTextAlign(12)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    legend.AddEntry(h, massPoints[i], "l")

legend.Draw()

if logy: 
    canvas.SetLogy();

canvas.SaveAs(variable[0]+'.png')
