
import ROOT as r
import os,  sys, fnmatch
import math

#===============================================================================0
#MAIN FUNCTION
#===============================================================================0

#Define the histogram
bwhist = r.TH1F("bw", "Breit-Wigner W boson distribution", 40, 60, 100)

rand = r.TRandom3()
for i in range(10000):
    value = rand.BreitWigner(80.379, 2.085)
    bwhist.Fill(value)

bwhist.Scale(1.0/bwhist.Integral())
bwhist.SetTitle("Breit-Wigner W boson distribution")
bwhist.GetXaxis().SetTitle("W mass [GeV]")

#Keep the histogram in a new file
outputFile = r.TFile.Open("bw.root", "recreate")
bwhist.Write()
outputFile.Close()
