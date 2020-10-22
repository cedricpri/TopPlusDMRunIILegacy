#Rin-out method for the DY estimation

import ROOT as r
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
metValues = [-1, 10, 20, 40, 100, -1]

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
RoutinMC = {}

for channel in channels:
    kappa[channel] = {}
    RoutinMC[channel] = {}

    for metBin in metBins:
        RoutinMC0bjet = (yieldsMC['0bjet']['out'][channel][metBin]/yieldsMC['0bjet']['in'][channel][metBin])
        RoutinData0bjet = (yieldsData['0bjet']['out'][channel][metBin]/yieldsData['0bjet']['in'][channel][metBin])

        kappa[channel][metBin] = RoutinMC0bjet/RoutinData0bjet
        RoutinMC[channel][metBin] = kappa[channel][metBin] * (yieldsData['1bjetOrMore']['out'][channel][metBin]/yieldsData['1bjetOrMore']['in'][channel][metBin])

print(kappa)
print(RoutinMC)

#==================================================================
#Plot the results

n = len(metBins)
canvas = r.TCanvas("canvas", "canvas")
multiGraph = r.TMultiGraph()

for i, channel in enumerate(channels):
    x, y = array( 'd' ), array( 'd' )

    for j, metBin in enumerate(metBins):
        if j == 0 or j == len(metBins):
            continue ## Don't plot the inclusive met cut and the last met cut

        x.append(int(metValues[j]))
        y.append(RoutinMC[channel][metBin])

    graph = r.TGraph(n, x, y)
    graph.SetTitle(channel)
    graph.SetMinimum(0)
    graph.SetMaximum(2)
    graph.SetMarkerStyle(21)
    graph.SetMarkerColor(channelColors[i])
    graph.SetMarkerSize(1.2)
    #graph.Draw()
    
    multiGraph.Add(graph, "ap")

multiGraph.GetXaxis().SetTitle("Pf MET [GeV]")
multiGraph.GetYaxis().SetTitle("R^{out/in} = N^{out} / N^{in}")
multiGraph.SetTitle('DY Rin-out scale factor (' + str(year) + ')')
multiGraph.Draw()

canvas.BuildLegend(0.78, 0.78, 0.9, 0.9)
canvas.Update()
canvas.SaveAs("Rinout.png")
