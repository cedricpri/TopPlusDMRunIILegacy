#Rin-out method for the DY estimation

import ROOT as r
import math
from array import array

#!!TODO: apply this method to the region of the analysis (mt2ll cut, for example)
haddFile = 'rootFile/plots_ttDM2016_DY.root'

#General parameters
year = 2016
channels = ['ee', 'mm']

#Z window width
xmin = 76
xmax = 106

#Histograms to be considered for the computation
DYObjects = ['histo_DY;1', 'histo_DY;2']
MCObjects = ['histo_ttZ;1', 'histo_Vg;1', 'histo_VgS_L;1', 'histo_ttbar;1', 'histo_ttW;1', 'histo_TTToSemiLeptonic;1', 'histo_singleTop;1', 'histo_VVV;1', 'histo_WW;1', 'histo_VgS_H;1', 'histo_VZ;1'] #Backgrounds to be substracted to only keep DY-like data events
dataObjects = ['histo_DATA;1']

#MET bins used to plot the Routin factor
metBins = ['0', '1', '2', '3', '4', '5'] #Matching the definition of the cuts in the cuts.py file: 0 is the inclusive distribution
metValues = [0, 40, 70, 100, 250]

#Additional options
use0bjet = True
channelColors = [r.kBlack, r.kRed, r.kBlue] 
systematicValue = 0.3

#==================================================================
#Let's get started with some functions

f = r.TFile.Open(haddFile, "read")

def extractHistogramFromFile(f, objectName):
    hist = r.TH1D()
    hist.Sumw2() #Deal with errors
    f.GetObject(objectName, hist)

    return hist

def getIntegralBetweenValues(hist, xmin, xmax):
    try:
        xAxis = hist.GetXaxis()        
        bmin = xAxis.FindBin(xmin)
        bmax = xAxis.FindBin(xmax)

        error = r.Double(0)
        integralError = hist.IntegralAndError(bmin, bmax, error)
        return [integralError, error]

    except Exception as e:
        print(e)
        return 0

def getYieldsAndError(obj, channel, category, region, metBin, substractObject = None):
    global f, xmin, xmax

    yields = 0
    error = 0
    objectPath = region + '_' + channel + '_met' + metBin + '/mll/'
    
    for o in obj:
        if category == 'in':
            yieldsError = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + o), xmin, xmax)
            yields += yieldsError[0]
            if substractObject is not None:
                for s in substractObject:
                    yieldsError = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + s), xmin, xmax)
                    yields -= yieldsError[0]

        else: 
            yieldsError = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + o), 0, xmin) + getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + o), xmax, 10000)
            yields += yieldsError[0]
            if substractObject is not None:
                for s in substractObject:
                    yieldsError = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + s), 0, xmin) + getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + s), xmax, 10000)
                    yields -= yieldsError[0]

    return [yields, error]

#==================================================================
#Compute all the possible yields we are going to need

yieldsMC = {}
errorsMC = {}
yieldsData = {}
errorsData = {}

for region in ['0bjet', '1bjetOrMore']:
    yieldsMC[region] = {}
    errorsMC[region] = {}
    yieldsData[region] = {}
    errorsData[region] = {}

    for category in ['in', 'out']:
        yieldsMC[region][category] = {}
        errorsMC[region][category] = {}
        yieldsData[region][category] = {}
        errorsData[region][category] = {}

        for channel in channels: 
            yieldsMC[region][category][channel] = {}
            errorsMC[region][category][channel] = {}
            yieldsData[region][category][channel] = {}
            errorsData[region][category][channel] = {}

            #Yields divided depending on the value of the Pfmet
            for metBin in metBins:
                yieldsMC[region][category][channel][metBin] = 0
                errorsMC[region][category][channel][metBin] = 0
                yieldsData[region][category][channel][metBin] = 0
                errorsData[region][category][channel][metBin] = 0

                errors = []
                for MCObject in MCObjects:
                    yieldsError = getYieldsAndError(DYObjects, channel, category, region, metBin)
                    yieldsMC[region][category][channel][metBin] = yieldsMC[region][category][channel][metBin] + yieldsError[0]
                    errors.append(yieldsError[1])
                errorsMC[region][category][channel][metBin] = sum(map(lambda x:x*x, errors))

                errors = []
                for dataObject in dataObjects:
                    yieldsError = getYieldsAndError(dataObjects, channel, category, region, metBin, MCObjects)
                    yieldsData[region][category][channel][metBin] = yieldsData[region][category][channel][metBin] + yieldsError[0]
                    errors.append(yieldsError[1])
                errorsData[region][category][channel][metBin] = sum(map(lambda x:x*x, errors))

print("Yields MC:") 
print(yieldsMC)
print("Errors MC:") 
print(errorsMC)

print("Yields data:")
print(yieldsData)
print("Errors data:")
print(errorsData)

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
        if use0bjet:
            RoutinMC0bjet = (yieldsMC['0bjet']['out'][channel][metBin]/yieldsMC['0bjet']['in'][channel][metBin])
            errorRoutinMC0bjet = RoutinMC0bjet * math.sqrt((1/yieldsMC['0bjet']['out'][channel][metBin]) + (1/yieldsMC['0bjet']['in'][channel][metBin]))
        
            RoutinData0bjet = (yieldsData['0bjet']['out'][channel][metBin]/yieldsData['0bjet']['in'][channel][metBin])
            errorRoutinData0bjet = RoutinData0bjet * math.sqrt((1/yieldsData['0bjet']['out'][channel][metBin]) + (1/yieldsData['0bjet']['in'][channel][metBin]))

            #Statistical error only, at least for now
            kappa[channel][metBin] = RoutinMC0bjet/RoutinData0bjet
            errorKappa[channel][metBin] = kappa[channel][metBin] * math.sqrt((errorRoutinMC0bjet/RoutinMC0bjet) ** 2 + (errorRoutinData0bjet/RoutinData0bjet) ** 2)
            outputKappa[channel][metBin] = str(kappa[channel][metBin]) + " +- " + str(errorKappa[channel][metBin])

        else:
            kappa[channel][metBin] = 1
            errorKappa[channel][metBin] = 0.0000001
            outputKappa[channel][metBin] = str(kappa[channel][metBin]) + " +- " + str(errorKappa[channel][metBin])

        RoutinMC[channel][metBin] = kappa[channel][metBin] * (yieldsData['1bjetOrMore']['out'][channel][metBin]/yieldsData['1bjetOrMore']['in'][channel][metBin])
        errorRoutinMC[channel][metBin] = RoutinMC[channel][metBin] * math.sqrt((errorKappa[channel][metBin]/kappa[channel][metBin]) + (1/yieldsMC['1bjetOrMore']['out'][channel][metBin]) + (1/yieldsMC['1bjetOrMore']['in'][channel][metBin]))
        outputRoutinMC[channel][metBin] = str(RoutinMC[channel][metBin]) + " +- " + str(errorRoutinMC[channel][metBin])

        numberExpectedOutDYYields = RoutinMC[channel][metBin] * yieldsMC['1bjetOrMore']['in'][channel][metBin]
        errorNumberExpectedOutDYYields = numberExpectedOutDYYields * math.sqrt((errorRoutinMC[channel][metBin]/RoutinMC[channel][metBin]) ** 2 + (1/yieldsMC['1bjetOrMore']['in'][channel][metBin]))

        scaleFactor[channel][metBin] = yieldsMC['1bjetOrMore']['out'][channel][metBin]/numberExpectedOutDYYields
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
        #h[i].GetYaxis().SetTitle("R^{out/in} = N^{out} / N^{in}")
        h[i].GetYaxis().SetTitle("DY SF")
        h[i].SetTitle('DY Rin-out scale factor (' + str(year) + ')')

    h[i].SetBins(len(metValues) - 1, array('d', metValues))

    for j in range(1, len(metValues)): #Start at 1 to avoid plotting the inclusive MET bin
        h[i].SetBinContent(j, scaleFactor[channel][str(j)])
        h[i].SetBinError(j, errorScaleFactor[channel][str(j)])
        h[i].SetLineColor(channelColors[i])
        h[i].SetLineWidth(2)
        h[i].SetMarkerStyle(21)
        #h[i].GetYaxis().SetRangeUser(0.6, 1.6)
        h[i].SetMarkerColor(channelColors[i])
        h[i].Draw("same")
        
    legend.AddEntry(h[i], channel)

#Plot the inclusive value
line = r.TLine(0, (scaleFactor["ee"]["0"] + scaleFactor["mm"]["0"])/2, 250, (scaleFactor["ee"]["0"] + scaleFactor["mm"]["0"])/2);
line.SetLineStyle(9)
line.Draw()

lineUp = r.TLine(0, (scaleFactor["ee"]["0"] + scaleFactor["mm"]["0"])/2 + systematicValue, 250, (scaleFactor["ee"]["0"] + scaleFactor["mm"]["0"])/2 + systematicValue);
lineUp.SetLineStyle(4)
lineUp.Draw()
lineDown = r.TLine(0, (scaleFactor["ee"]["0"] + scaleFactor["mm"]["0"])/2 - systematicValue, 250, (scaleFactor["ee"]["0"] + scaleFactor["mm"]["0"])/2 - systematicValue);
lineDown.SetLineStyle(4)
lineDown.Draw()

legend.SetBorderSize(0)
legend.Draw()
canvas.SaveAs("Rinout.png")
canvas.SaveAs("Rinout.root")

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
