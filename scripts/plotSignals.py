from ROOT import TCanvas, TLegend, TChain, TFile, TH1F
import fnmatch, os

#=============================================================================
#SETUP
#=============================================================================
#variable = ["Puppi_MET", 100, 0, 500, "Puppi MET [GeV]"] #Variable name, bins, from, to, xaxis title
#variable = ["MET_pt", 100, 0, 500, "PfMET [GeV]"]
#variable = ["dark_pt", 50, 0, 800, "Dark pt [GeV]"] 
#variable = ["overlapingFactor", 40, 0, 4, "Overlapping factor"] 
#variable = ["nbJet", 6, 0, 6, "Medium deepCSV b-jets"] 
variable = ["mblt", 50, 0, 350, "mblt [GeV]"] 
#variable = ["massT", 50, 0, 1500, "massT [GeV]"] 

signalDir = "/eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7__MCCorr2018v7__l2loose__l2tightOR2018v7_weighted/"
category = "pseudoscalar"
trailer = "*"
cuts = "baseW * genWeight * (mll > 20.) * (mt2ll > 80.) * (Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13 || (mll < 76 || mll > 106)) * (Sum$(CleanJet_pt >= 30. && abs(CleanJet_eta) < 2.4) > 0) * (nbJet > 0)"
#cuts = "baseW * genWeight"

normalization = False
addBackground = False #Plot the ttbar on this plot as wel?
logy = not normalization

files = [{'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_1_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_1_Mphi_100'},
         {'file': 'DM' + category + '_Dilepton_top_tWChan_Mchi1_Mphi100__part' + trailer + '.root', 'massPoint': 'tWChan_' + category + '_Mchi1_Mphi100'}]

"""
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

files = [{'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_20_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_20_Mphi_100'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_30_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_30_Mphi_100'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_40_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_40_Mphi_100'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_45_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_45_Mphi_100'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_49_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_49_Mphi_100'},
         {'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_51_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_51_Mphi_100'}]
         #{'file': 'TTbarDMJets_Dilepton_' + category + '_LO_Mchi_55_Mphi_100'+ trailer +'.root', 'massPoint': category + '_Mchi_55_Mphi_100'}] #Not available for pseudoscalar"

files = [{'file': 'DM' + category + '_Dilepton_top_tWChan_Mchi1_Mphi50__part' + trailer + '.root', 'massPoint': 'tWChan_' + category + '_Mchi1_Mphi50'},
         {'file': 'DM' + category + '_Dilepton_top_tWChan_Mchi1_Mphi100__part' + trailer + '.root', 'massPoint': 'tWChan_' + category + '_Mchi1_Mphi100'},
         {'file': 'DM' + category + '_Dilepton_top_tWChan_Mchi1_Mphi150__part' + trailer + '.root', 'massPoint': 'tWChan_' + category + '_Mchi1_Mphi150'},
         {'file': 'DM' + category + '_Dilepton_top_tWChan_Mchi1_Mphi200__part' + trailer + '.root', 'massPoint': 'tWChan_' + category + '_Mchi1_Mphi200'},
         {'file': 'DM' + category + '_Dilepton_top_tWChan_Mchi1_Mphi250__part' + trailer + '.root', 'massPoint': 'tWChan_' + category + '_Mchi1_Mphi250'},
         {'file': 'DM' + category + '_Dilepton_top_tWChan_Mchi1_Mphi300__part' + trailer + '.root', 'massPoint': 'tWChan_' + category + '_Mchi1_Mphi300'},
         {'file': 'DM' + category + '_Dilepton_top_tWChan_Mchi1_Mphi350__part' + trailer + '.root', 'massPoint': 'tWChan_' + category + '_Mchi1_Mphi350'},
         {'file': 'DM' + category + '_Dilepton_top_tWChan_Mchi1_Mphi400__part' + trailer + '.root', 'massPoint': 'tWChan_' + category + '_Mchi1_Mphi400'},
         {'file': 'DM' + category + '_Dilepton_top_tWChan_Mchi1_Mphi450__part' + trailer + '.root', 'massPoint': 'tWChan_' + category + '_Mchi1_Mphi450'},
         {'file': 'DM' + category + '_Dilepton_top_tWChan_Mchi1_Mphi500__part' + trailer + '.root', 'massPoint': 'tWChan_' + category + '_Mchi1_Mphi500'}]
"""

if addBackground:
    files.append({'file': 'TTTo2L2Nu'+trailer+'.root', 'massPoint': 'TTTo2L2Nu'})
    #files.append({'file': 'ST_'+trailer+'.root', 'massPoint': 'Single top'})

#=============================================================================
#GET STARTED
#=============================================================================
#Create and store the histograms...
massPoints = [] #For the legend
signalHistList = []

if len(files) == 2:
    colors = [632, 600]
elif len(files) == 3:
    colors = [632, 800, 600]
else:
    colors = [636, 635, 634, 633, 632, 807, 802, 801, 800, 798] 
    colors = colors[:len(files)-1]

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
    if len(files) <= 3: signalHist.SetLineWidth(3)
    signalHist.GetXaxis().SetTitle(variable[4])
    #if logy: signalHist.GetYaxis().SetRangeUser(0.001, 3000)
    #else: signalHist.GetYaxis().SetRangeUser(0.001, 0.06)

    massPoints.append(massPoint)
    signalHistList.append(signalHist)

#... And plot them
canvas = TCanvas( 'canvas', 'Signal samples', 200, 10, 700, 500)
canvas.SetGrid()
canvas.cd()

if len(files) == 2:
    legend = TLegend(0.52, 0.80, 0.72, 0.86)
elif len(files) == 3:
    #legend = TLegend(0.50, 0.75, 0.70, 0.85)
    legend = TLegend(0.20, 0.2, 0.40, 0.3)
else:
    #legend = TLegend(0.55, 0.55, 0.75, 0.85) #Scalar high DM mass
    #legend = TLegend(0.46, 0.55, 0.75, 0.85) #Pseudoscalar high DM mass
    #legend = TLegend(0.55, 0.55, 0.75, 0.85) #Scalar high mediator mass
    #legend = TLegend(0.48, 0.55, 0.75, 0.85) #Pseudoscalar high mediator mass
    
    #legend = TLegend(0.48, 0.55, 0.75, 0.85) #Single top scalar high mediator mass
    legend = TLegend(0.39, 0.55, 0.75, 0.85) #Single top pseudoscalar high mediator mass
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
canvas.SaveAs(variable[0]+'.pdf')
