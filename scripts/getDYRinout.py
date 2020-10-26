#Rin-out method for the DY estimation

import ROOT as r
import math
from array import array

#!!TODO: apply this method to the region of the analysis (mt2ll cut, for example)
haddFile = 'rootFile/plots_ttDM2018_DY.root'

#General parameters
year = 2018
channels = ['ee', 'mm']

#Z window width
xmin = 76
xmax = 106

#Histograms to be considered for the computation
MCObjects = ['histo_DY;1', 'histo_DY;2']
dataObjects = ['histo_DATA;1']

#MET bins used to plot the Routin factor
metBins = ['0', '1', '2', '3', '4', '5'] #Matching the definition of the cuts in the cuts.py file: 0 is the inclusive distribution
metValues = [0, 10, 20, 40, 100, 200]

#Additional options
channelColors = [r.kBlack, r.kRed, r.kBlue] 

#==================================================================
#Let's get started with some functions

f = r.TFile.Open(haddFile, "read")

def extractHistogramFromFile(f, objectName):
    hist = r.TH1D()
    f.GetObject(objectName, hist)

    return hist

def getIntegralBetweenValues(hist, xmin, xmax):
    try:
        xAxis = hist.GetXaxis()        
        bmin = xAxis.FindBin(xmin)
        bmax = xAxis.FindBin(xmax)

        return hist.Integral(bmin, bmax)

    except Exception as e:
        return 0

def getYields(obj, channel, category, region, metBin):
    global f, xmin, xmax

    objectPath = region + '_' + channel + '_met' + metBin + '/mll/' + obj
    if category == 'in':
        yields = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath), xmin, xmax)
    else: 
        yields = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath), 0, xmin) + getIntegralBetweenValues(extractHistogramFromFile(f, objectPath), xmax, 10000)
    return yields

#==================================================================
#Compute all the possible yields we are going to need

yieldsMC = {}
yieldsData = {}

for region in ['0bjet', '1bjetOrMore']:
    yieldsMC[region] = {}
    yieldsData[region] = {}

    for category in ['in', 'out']:
        yieldsMC[region][category] = {}
        yieldsData[region][category] = {}

        for channel in channels: 
            yieldsMC[region][category][channel] = {}
            yieldsData[region][category][channel] = {}

            #Yields divided depending on the value of the Pfmet
            for metBin in metBins:
                yieldsMC[region][category][channel][metBin] = 0
                yieldsData[region][category][channel][metBin] = 0

                for MCObject in MCObjects:
                    yieldsMC[region][category][channel][metBin] = yieldsMC[region][category][channel][metBin] + getYields(MCObject, channel, category, region, metBin)

                for dataObject in dataObjects:
                    yieldsData[region][category][channel][metBin] = yieldsData[region][category][channel][metBin] + getYields(dataObject, channel, category, region, metBin)

#==================================================================
#Compute the global Routin factor and scale factor in the different channels and for different met cuts
kappa = {}
errorKappa = {}
outputKappa = {}
RoutinMC = {}
errorRoutinMC = {}
outputRoutinMC = {}
scaleFactor = {}
errorScaleFactor = {}
outputScaleFactor = {}

for channel in channels:
    kappa[channel] = {}
    errorKappa[channel] = {}
    outputKappa[channel] = {}
    RoutinMC[channel] = {}
    errorRoutinMC[channel] = {}
    outputRoutinMC[channel] = {}
    scaleFactor[channel] = {}
    errorScaleFactor[channel] = {}
    outputScaleFactor[channel] = {}

    for metBin in metBins:
        RoutinMC0bjet = (yieldsMC['0bjet']['out'][channel][metBin]/yieldsMC['0bjet']['in'][channel][metBin])
        errorRoutinMC0bjet = RoutinMC0bjet * math.sqrt((1/yieldsMC['0bjet']['out'][channel][metBin]) + (1/yieldsMC['0bjet']['in'][channel][metBin]))

        RoutinData0bjet = (yieldsData['0bjet']['out'][channel][metBin]/yieldsData['0bjet']['in'][channel][metBin])
        errorRoutinData0bjet = RoutinData0bjet * math.sqrt((1/yieldsData['0bjet']['out'][channel][metBin]) + (1/yieldsData['0bjet']['in'][channel][metBin]))

        #Statistical error only for now
        kappa[channel][metBin] = RoutinMC0bjet/RoutinData0bjet
        errorKappa[channel][metBin] = kappa[channel][metBin] * math.sqrt((errorRoutinMC0bjet/RoutinMC0bjet) ** 2 + (errorRoutinData0bjet/RoutinData0bjet) ** 2)
        outputKappa[channel][metBin] = str(kappa[channel][metBin]) + " +- " + str(errorKappa[channel][metBin])

        RoutinMC[channel][metBin] = kappa[channel][metBin] * (yieldsData['1bjetOrMore']['out'][channel][metBin]/yieldsData['1bjetOrMore']['in'][channel][metBin])
        intermediateError = (yieldsData['1bjetOrMore']['out'][channel][metBin]/yieldsData['1bjetOrMore']['in'][channel][metBin]) * math.sqrt((1/yieldsData['1bjetOrMore']['out'][channel][metBin]) + (1/yieldsData['1bjetOrMore']['in'][channel][metBin]))
        errorRoutinMC[channel][metBin] = RoutinMC[channel][metBin] * math.sqrt((errorKappa[channel][metBin]/kappa[channel][metBin]) ** 2 + (intermediateError/(yieldsData['1bjetOrMore']['out'][channel][metBin]/yieldsData['1bjetOrMore']['in'][channel][metBin])) ** 2)
        outputRoutinMC[channel][metBin] = str(RoutinMC[channel][metBin]) + " +- " + str(errorRoutinMC[channel][metBin])

        numberExpectedOutDYYields = RoutinMC[channel][metBin] * yieldsData['1bjetOrMore']['in'][channel][metBin]
        errorNumberExpectedOutDYYields = numberExpectedOutDYYields * math.sqrt((errorRoutinMC[channel][metBin]/RoutinMC[channel][metBin]) ** 2 + (1/yieldsData['1bjetOrMore']['in'][channel][metBin]))

        scaleFactor[channel][metBin] = yieldsData['1bjetOrMore']['out'][channel][metBin]/numberExpectedOutDYYields
        errorScaleFactor[channel][metBin] = scaleFactor[channel][metBin] * math.sqrt((errorNumberExpectedOutDYYields/numberExpectedOutDYYields) ** 2 + (1/yieldsData['1bjetOrMore']['out'][channel][metBin]))
        outputScaleFactor[channel][metBin] = str(scaleFactor[channel][metBin]) + " +- " + str(errorScaleFactor[channel][metBin])

print("Kappa: ")
print(outputKappa)

print("RoutinMC: ")
print(outputRoutinMC)

print("Scale factor: ")
print(outputScaleFactor)

#==================================================================
#Plot the results

canvas = r.TCanvas("canvas", "canvas")
legend = r.TLegend(0.15, 0.74, 0.35, 0.85)
r.gStyle.SetOptStat(0)

h = []
for i, channel in enumerate(channels):
    h.append(r.TH1D())

    if(i == 0):
        h[i].GetXaxis().SetTitle("Pf MET [GeV]")
        h[i].GetYaxis().SetTitle("R^{out/in} = N^{out} / N^{in}")
        h[i].SetTitle('DY Rin-out scale factor (' + str(year) + ')')

    h[i].SetBins(len(metValues) - 1, array('d', metValues))

    for j in range(1, len(metValues)): #Start at 1 to avoid plotting the inclusive MET bin
        h[i].SetBinContent(j, scaleFactor[channel][str(j)])
        h[i].SetBinError(j, errorScaleFactor[channel][str(j)])
        h[i].SetLineColor(channelColors[i])
        h[i].SetLineWidth(2)
        h[i].SetMarkerStyle(21)
        h[i].GetYaxis().SetRangeUser(1.0, 2.2)
        h[i].SetMarkerColor(channelColors[i])
        h[i].Draw("same")

    legend.AddEntry(h[i], channel)

legend.SetBorderSize(0)
legend.Draw()
canvas.SaveAs("Rinout.png")

"""
    graph = r.TGraph(n, x, y)
    graph.SetTitle(channel)
    graph.SetMinimum(0)
    graph.SetMaximum(2)
    graph.SetMarkerStyle(21)
    graph.SetMarkerColor(channelColors[i])
    graph.SetMarkerSize(1.2)
    #graph.Draw()
    
    multiGraph.Add(graph, "ap")

#multiGraph.GetXaxis().SetTitle("Pf MET [GeV]")
#multiGraph.GetYaxis().SetTitle("R^{out/in} = N^{out} / N^{in}")
#multiGraph.SetTitle('DY Rin-out scale factor (' + str(year) + ')')
multiGraph.Draw()

canvas.BuildLegend(0.78, 0.78, 0.9, 0.9)
canvas.Update()
canvas.SaveAs("Rinout.png")
"""
