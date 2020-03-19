import os, fnmatch, sys
from ROOT import TCanvas, TLegend, TFile, TProfile, TNtuple, TH1F, TH2F

#=============================================================================
#SETUP
#=============================================================================
#Directory where the signal samples can be found
signalDir = "/eos/user/c/cprieels/work/SignalsPostProcessing/Pablo/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"

#Categorios and variables to be plotted
categories = ["scalar", "pseudoscalar"] #Add the single top once available
variables = [["PuppiMET_pt", 0, 200, 20, "Puppi MET [GeV]"]] #Variable name, from, to, bins, xaxis

#=============================================================================
# HELPERS
#=============================================================================
#Progress bar
def updateProgress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done!\r\n"
    block = int(round(barLength*progress))
    text = "\rProgress: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

#=============================================================================
#GET STARTED
#=============================================================================
for c, category in enumerate(categories):
    legend = TLegend(0.1, 0.65, 0.25, 0.9)

    for v, variable in enumerate(variables):
        canvas = TCanvas( 'canvas_'+str(category)+'_'+str(variable[0]), 'Signal samples', 200, 10, 700, 500 )
        canvas.cd()

    filenames = fnmatch.filter(os.listdir(signalDir), '*_'+category+'*Mchi_1_*') #For now, only mChi 1 GeV
    for f, filename in enumerate(filenames):
        print('Now reading file... ' + filename)
        massPoint = "_".join(filename.split("_")[5:9]).replace('.root', '')

        signalFile = TFile.Open(signalDir+filename, "read")
        signalTree = signalFile.Get("Events")

        for v, variable in enumerate(variables):
            histname = 'hist_'+str(category)+'_'+str(variable[0])+'_'+str(filename)
            signalHist = TH1F(histname, 'Mass points ' + variable[0] + ' distribution (' + category + ")", variable[3], variable[1], variable[2])
            
            signalTree.Draw(variable[0] + ' >> ' + histname)
            signalHist.Scale(1./signalHist.Integral()) #Normalize the histo to unity
            signalHist.SetLineWidth(4)
            signalHist.SetLineColor(632+f)
            signalHist.SetStats(0)
            signalHist.GetXaxis().SetTitle(variable[4])
            signalHist.Draw('same')

            legend.AddEntry(signalHist, massPoint)
            legend.Draw()
            
    canvas.SaveAs(category+'.png')
