#Rin-out method for the DY estimation

import ROOT as r
import math
from array import array

#General parameters
year = 2018
channels = ['ee', 'mm']

haddFile = 'Shapes/' + str(year) + '/Rinout/plots_Rinout_SM.root'

#Z window width
xmin = 76
xmax = 106

#Histograms to be considered for the computation
DYObjects = ['histo_DY']
MCObjects = ['histo_ttbar', 'histo_ttW', 'histo_STtW', 'histo_VVV', 'histo_ZZ', 'histo_WZ', 'histo_ttSemilep', 'histo_ttZ', 'histo_WW'] #Backgrounds to be substracted to only keep DY-like data events
dataObjects = ['histo_DATA']

#MET bins used to plot the Routin factor
metBins = ['0', '1', '2', '3', '4', '5'] #Matching the definition of the cuts in the cuts.py file: 0 is the inclusive distribution
#metValues = [0, 40, 70, 100, 250]
metValues = [0, 20, 40, 60, 120]

#Additional options
channelColors = [r.kBlack, r.kRed, r.kBlue] 
systematicValue = 0.2

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
    errors = []
    objectPath = region + '_' + channel + '_met' + metBin + '/mll/'
    
    for o in obj:
        if category == 'in':
            yieldsError = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + o), xmin, xmax)
            yields += yieldsError[0]
            errors.append(yieldsError[1])
        else: 
            yieldsError = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + o), 0, xmin) + getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + o), xmax, 10000)
            yields += yieldsError[0]
            errors.append(yieldsError[1])

    if substractObject is not None:
        if category == 'in':
            for s in substractObject:
                yieldsError = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + s), xmin, xmax)
                yields -= yieldsError[0]
                errors.append(yieldsError[1])
        else: 
            for s in substractObject:
                yieldsError = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + s), 0, xmin) + getIntegralBetweenValues(extractHistogramFromFile(f, objectPath + s), xmax, 10000)
                yields -= yieldsError[0]
                errors.append(yieldsError[1])

    return [yields, math.sqrt(sum(map(lambda x:x*x, errors)))]

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

                yieldsError = getYieldsAndError(DYObjects, channel, category, region, metBin)
                yieldsMC[region][category][channel][metBin] = yieldsMC[region][category][channel][metBin] + yieldsError[0]
                errorsMC[region][category][channel][metBin] = yieldsError[1]

                yieldsError = getYieldsAndError(dataObjects, channel, category, region, metBin, MCObjects)
                yieldsData[region][category][channel][metBin] = yieldsData[region][category][channel][metBin] + yieldsError[0]
                errorsData[region][category][channel][metBin] = yieldsError[1]

print("Yields MC:") 
print(yieldsMC)

print("Yields data:")
print(yieldsData)

#==================================================================
#Compute the global Routin factor and scale factor in the different channels and for different met cuts
kappa = {}
errorKappa = {}
outputKappa = {}

RoutinMC = {}
errorRoutinMC = {}
outputRoutinMC = {}
RoutinData = {}
errorRoutinData = {}
outputRoutinData = {}

RoutinMC0bjet = {}
errorRoutinMC0bjet = {}
RoutinData0bjet = {}
errorRoutinData0bjet = {}

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
    RoutinData[channel] = {}
    errorRoutinData[channel] = {}
    outputRoutinData[channel] = {}

    RoutinMC0bjet[channel] = {}
    errorRoutinMC0bjet[channel] = {}
    RoutinData0bjet[channel] = {}
    errorRoutinData0bjet[channel] = {}

    scaleFactor[channel] = {}
    errorScaleFactor[channel] = {}
    outputScaleFactor[channel] = {}

    for metBin in metBins:
        RoutinMC0bjetNumber = (yieldsMC['0bjet']['out'][channel][metBin]/yieldsMC['0bjet']['in'][channel][metBin])
        errorRoutinMC0bjetNumber = RoutinMC0bjetNumber * math.sqrt(((errorsMC['0bjet']['out'][channel][metBin])/(yieldsMC['0bjet']['out'][channel][metBin])) ** 2 + ((errorsMC['0bjet']['in'][channel][metBin])/(yieldsMC['0bjet']['in'][channel][metBin])) ** 2)
        
        RoutinMC0bjet[channel][metBin] = RoutinMC0bjetNumber
        errorRoutinMC0bjet[channel][metBin] = errorRoutinMC0bjetNumber

        RoutinData0bjetNumber = (yieldsData['0bjet']['out'][channel][metBin]/yieldsData['0bjet']['in'][channel][metBin])
        errorRoutinData0bjetNumber = RoutinData0bjetNumber * math.sqrt(((errorsData['0bjet']['out'][channel][metBin])/(yieldsData['0bjet']['out'][channel][metBin])) ** 2 + ((errorsData['0bjet']['in'][channel][metBin])/(yieldsData['0bjet']['in'][channel][metBin])) ** 2)            

        RoutinData0bjet[channel][metBin] = RoutinData0bjetNumber
        errorRoutinData0bjet[channel][metBin] = errorRoutinData0bjetNumber

        #Statistical error only, at least for now
        kappa[channel][metBin] = RoutinMC0bjetNumber/RoutinData0bjetNumber
        errorKappa[channel][metBin] = kappa[channel][metBin] * math.sqrt((errorRoutinMC0bjetNumber/RoutinMC0bjetNumber) ** 2 + (errorRoutinData0bjetNumber/RoutinData0bjetNumber) ** 2)
        outputKappa[channel][metBin] = str(kappa[channel][metBin]) + " +- " + str(errorKappa[channel][metBin])

        RoutinMC[channel][metBin] = kappa[channel][metBin] * (yieldsMC['1bjetOrMore']['out'][channel][metBin]/yieldsMC['1bjetOrMore']['in'][channel][metBin])
        errorRoutinMC[channel][metBin] = RoutinMC[channel][metBin] * math.sqrt((errorKappa[channel][metBin]/kappa[channel][metBin]) + (errorsMC['1bjetOrMore']['out'][channel][metBin]/yieldsMC['1bjetOrMore']['out'][channel][metBin]) ** 2 + (errorsMC['1bjetOrMore']['in'][channel][metBin]/yieldsMC['1bjetOrMore']['in'][channel][metBin]) ** 2)
        outputRoutinMC[channel][metBin] = str(RoutinMC[channel][metBin]) + " +- " + str(errorRoutinMC[channel][metBin])

        RoutinData[channel][metBin] = kappa[channel][metBin] * (yieldsData['1bjetOrMore']['out'][channel][metBin]/yieldsData['1bjetOrMore']['in'][channel][metBin])
        errorRoutinData[channel][metBin] = RoutinData[channel][metBin] * math.sqrt((errorKappa[channel][metBin]/kappa[channel][metBin]) + (errorsData['1bjetOrMore']['out'][channel][metBin]/yieldsData['1bjetOrMore']['out'][channel][metBin]) ** 2 + (errorsData['1bjetOrMore']['in'][channel][metBin]/yieldsData['1bjetOrMore']['in'][channel][metBin]) ** 2)
        outputRoutinData[channel][metBin] = str(RoutinData[channel][metBin]) + " +- " + str(errorRoutinData[channel][metBin])

        numberExpectedOutDYYields = RoutinMC[channel][metBin] * yieldsData['1bjetOrMore']['in'][channel][metBin]
        errorNumberExpectedOutDYYields = numberExpectedOutDYYields * math.sqrt((errorRoutinMC[channel][metBin]/RoutinMC[channel][metBin]) ** 2 + (errorsData['1bjetOrMore']['in'][channel][metBin]/yieldsData['1bjetOrMore']['in'][channel][metBin]) ** 2)

        scaleFactor[channel][metBin] = yieldsData['1bjetOrMore']['out'][channel][metBin]/numberExpectedOutDYYields
        errorScaleFactor[channel][metBin] = scaleFactor[channel][metBin] * math.sqrt((errorNumberExpectedOutDYYields/numberExpectedOutDYYields) ** 2 + (errorsData['1bjetOrMore']['out'][channel][metBin]/yieldsData['1bjetOrMore']['out'][channel][metBin]) ** 2)
        outputScaleFactor[channel][metBin] = str(scaleFactor[channel][metBin]) + " +- " + str(errorScaleFactor[channel][metBin])

print("Kappa: ")
print(outputKappa)

print("RoutinMC: ")
print(outputRoutinMC)

print("RoutinData: ")
print(outputRoutinData)

print("Scale factor: ")
print(outputScaleFactor)

#==================================================================
#Plot the results

canvas = r.TCanvas("canvas", "canvas")
legend = r.TLegend(0.15, 0.74, 0.35, 0.85)
r.gStyle.SetOptStat(0)

allh = []
plots = [
    [RoutinData, errorRoutinData, "data"] 
#    [RoutinMC, errorRoutinMC, "MC"], 
#    [RoutinData0bjet, errorRoutinData0bjet, "data_0bjet"],
#    [RoutinMC0bjet, errorRoutinMC0bjet, "MC_0bjet"]
]

for p, plot in enumerate(plots):
    for i, channel in enumerate(channels):
        h = r.TH1D()
        if(i == 0):
            h.GetXaxis().SetTitle("Pf MET [GeV]")
            h.GetYaxis().SetTitle("R^{out/in} = N^{out} / N^{in}")
            #h.GetYaxis().SetTitle("DY SF")
            h.SetTitle('DY Rin-out (' + str(year) + ')')
            #h.SetTitle('DY Rin-out scale factor (' + str(year) + ')')

        h.SetBins(len(metValues) - 1, array('d', metValues))
        h.SetName(channel + "_" + plot[2])

        for j in range(1, len(metValues)): #Start at 1 to avoid plotting the inclusive MET bin
            h.SetBinContent(j, plot[0][channel][str(j)])
            h.SetBinError(j, plot[1][channel][str(j)])
            h.SetLineColor(channelColors[i])
            h.SetLineWidth(2)
            h.SetMarkerStyle(21)
            h.GetYaxis().SetRangeUser(0.6, 1.4)
            h.SetMarkerColor(channelColors[i])
            h.Draw("same")
        
        if(p == 0): 
            legend.AddEntry(h, channel)
        allh.append(h)

    #Plot the inclusive value
    inputData = plot[0]
    line = r.TLine(0, (inputData["ee"]["0"] + inputData["mm"]["0"])/2, 120, (inputData["ee"]["0"] + inputData["mm"]["0"])/2);
    line.SetLineStyle(9)
    line.Draw()

    if systematicValue > 0.0:
        lineUp = r.TLine(0, (inputData["ee"]["0"] + inputData["mm"]["0"])/2 + systematicValue, 120, (inputData["ee"]["0"] + inputData["mm"]["0"])/2 + systematicValue);
        lineUp.SetLineStyle(4)
        lineUp.Draw()
        
        lineDown = r.TLine(0, (inputData["ee"]["0"] + inputData["mm"]["0"])/2 - systematicValue, 120, (inputData["ee"]["0"] + inputData["mm"]["0"])/2 - systematicValue);
        lineDown.SetLineStyle(4)
        lineDown.Draw()

    legend.SetBorderSize(0)
    legend.Draw()

    legend.SetBorderSize(0)
    legend.Draw()

    canvas.SaveAs("Rinout" + str(year) + "_" + plot[2] + ".png")
    canvas.SaveAs("Rinout" + str(year) + "_" + plot[2] + ".root")

summaryFile = r.TFile.Open("Rinout_summary_" + str(year) + ".root", "RECREATE")
for h in allh:
    h.Write()
summaryFile.Close()
