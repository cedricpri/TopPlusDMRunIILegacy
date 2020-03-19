import os, fnmatch, sys
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F

#=============================================================================
#SETUP
#=============================================================================
#Directory where the signal samples can be found
signalDir = "/eos/user/c/cprieels/work/SignalsPostProcessing/Pablo/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6/"

#Categorios and variables to be plotted
categories = ["scalar"] #Add the single top once available
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
    for v, variable in enumerate(variables):
        canvas = TCanvas( 'canvas_'+str(category)+'_'+str(variable[0]), 'Signal samples', 200, 10, 700, 500 )
        canvas.cd()

    filenames = fnmatch.filter(os.listdir(signalDir), '*_'+category+'*Mchi_*')
    for f, filename in enumerate(filenames):
        print('Now reading file... ' + filename)
        signalFile = TFile.Open(signalDir+filename, "read")
        signalTree = signalFile.Get("Events")

        for v, variable in enumerate(variables):
            signalHist = TH1F('hist_'+str(category)+'_'+str(variable[0])+'_'+str(filename), 'Mass points ' + variable[0] + ' distribution (' + category + ")", variable[3], variable[1], variable[2])
            signalTree.Draw('PuppiMET_pt >> signalHist')
            
            print("Integral: " + str(signalHist.Integral()))
            #signalHist.Scale(1./signalHist.Integral()) #Normalize the histo to unity
            signalHist.SetLineWidth(2)
            signalHist.SetLineColor(632+f)
            signalHist.GetXaxis().SetTitle(variable[4])
            signalHist.Draw('same')
            
    canvas.SaveAs(category+'.png')
