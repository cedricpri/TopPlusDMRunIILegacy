from ROOT import TCanvas, TLegend, TFile, TH1F

#=============================================================================
#SETUP
#=============================================================================
normalization = True
variable = ["PuppiMET_pt", 100, 0, 500, "Puppi MET [GeV]"] #Variable name, bins, from, to, xaxis title
signalDir = "/eos/user/c/cprieels/work/SignalsPostProcessing/Pablo/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"
category = "scalar"
"""
files = ['nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_1_Mphi_50.root', 
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_1_Mphi_100.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_1_Mphi_150.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_1_Mphi_200.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_1_Mphi_250.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_1_Mphi_300.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_1_Mphi_350.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_1_Mphi_400.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_1_Mphi_450.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_1_Mphi_500.root']
"""
files = ['nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_20_Mphi_100.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_30_Mphi_100.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_40_Mphi_100.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_45_Mphi_100.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_49_Mphi_100.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_51_Mphi_100.root',
         'nanoLatino_TTbarDMJets_Dilepton_'+category+'_LO_Mchi_55_Mphi_100.root']

#=============================================================================
#GET STARTED
#=============================================================================
#Create and store the histograms...
massPoints = [] #For the legend
signalHistList = []
colors = [636, 635, 634, 633, 632, 807, 802, 801, 800, 798] 

for f, filename in enumerate(files):
    print('Now reading file... ' + filename)

    massPoint = "_".join(filename.split("_")[5:9]).replace('.root', '')
    signalFile = TFile.Open(signalDir+filename, "read")
    signalTree = signalFile.Get("Events")
        
    histname = 'hist_'+str(f)
    signalHist = TH1F(histname, 'Mass points distribution ('+category+')', variable[1], variable[2], variable[3])

    signalTree.Draw(variable[0] + ' >> ' + histname)
    signalHist.SetDirectory(0)
    if normalization: signalHist.Scale(1./signalHist.Integral()) #Normalize the histo to unity
    signalHist.SetStats(0)
    signalHist.SetLineColor(colors[f])
    signalHist.GetXaxis().SetTitle(variable[4])
    
    massPoints.append(massPoint)
    signalHistList.append(signalHist)

#... And plot them
canvas = TCanvas( 'canvas', 'Signal samples', 200, 10, 700, 500 )
canvas.cd()

legend = TLegend(0.62, 0.55, 0.8, 0.8)

for i, h in enumerate(signalHistList):
    h.Draw('same')
    legend.AddEntry(h, massPoints[i])

legend.Draw()
canvas.SaveAs(category+'.png')
