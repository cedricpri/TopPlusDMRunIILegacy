#Rin-out method for the DY estimation

import ROOT as r

haddFile = 'rootFile/plots_ttDM2018_DY.root'

#General parameters
year = 2018
channels = ['ee', 'mm', 'll']

#Z window width
xmin = 76
xmax = 106

#Histograms to be considered for the computation
MCObjects = ['histo_DY;1', 'histo_DY;2']
dataObjects = ['histo_DATA;1']

#MET bins used to plot the Routin factor
metbins = ['', '10', '20', '40', '100']

#Let's get started
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

def getYields(obj, channel, category, region, metbin = ''):
    global f, xmin, xmax

    metbinPath = '' if metbin == '' else '_met' + str(metbin)
    objectPath = region + '_' + channel + metbinPath + '/mll/' + obj
    if category == 'in':
        yields = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath), xmin, xmax)
    else: 
        yields = getIntegralBetweenValues(extractHistogramFromFile(f, objectPath), 0, xmin) + getIntegralBetweenValues(extractHistogramFromFile(f, objectPath), xmax, 10000)
    return yields

#Compute all the possible yields we are going to need
yieldsMC = {}
yieldsData = {}

for region in ['0bjet', '1bjet']:
    yieldsMC[region] = {}
    yieldsData[region] = {}

    for category in ['in', 'out']:
        yieldsMC[region][category] = {}
        yieldsData[region][category] = {}

        for channel in channels: 
            yieldsMC[region][category][channel] = {}
            yieldsData[region][category][channel] = {}

            #Yields divided depending on the value of the Pfmet
            for metbin in metbins:
                yieldsMC[region][category][channel][metbin] = 0
                yieldsData[region][category][channel][metbin] = 0

                for MCObject in MCObjects:
                    yieldsMC[region][category][channel][metbin] = yieldsMC[region][category][channel][metbin] + getYields(MCObject, channel, category, region, metbin)

                for dataObject in dataObjects:
                    yieldsData[region][category][channel][metbin] = yieldsData[region][category][channel][metbin] + getYields(dataObject, channel, category, region, metbin)

#Compute the global Routin factor in the different channels
kappa = {}
RoutinMC = {}

for channel in channels:
    RoutinMC0bjet = (yieldsMC['0bjet']['out'][channel]/yieldsMC['0bjet']['in'][channel])
    RoutinData0bjet = (yieldsData['0bjet']['out'][channel]/yieldsData['0bjet']['in'][channel])

    kappa[channel] = RoutinMC0bjet/RoutinData0bjet
    RoutinMC[channel] = kappa[channel] * (yieldsData['1bjet']['out'][channel]/yieldsData['1bjet']['in'][channel])

print(kappa, RoutinMC)

#Plot the Pfmet histogram

"""
#First, get the number of yields in and out of the Z mass window in the 0bjet region
yieldsInMC0bj = getIntegralBetweenValues(extractHistogramFromFile(f, '0bjet/mll/histo_DY;1'), xmin, xmax) + getIntegralBetweenValues(extractHistogramFromFile(f, '0bjet/mll/histo_DY;2'), xmin, xmax)
yieldsOutMC0bj = getIntegralBetweenValues(extractHistogramFromFile(f, '0bjet/mll/histo_DY;1'), 0, xmin) + getIntegralBetweenValues(extractHistogramFromFile(f, '0bjet/mll/histo_DY;1'), xmax, 10000) + getIntegralBetweenValues(extractHistogramFromFile(f, '0bjet/mll/histo_DY;2'), 0, xmin) + getIntegralBetweenValues(extractHistogramFromFile(f, '0bjet/mll/histo_DY;2'), xmax, 10000)
RoutinMC0bj = yieldsOutMC0bj/yieldsInMC0bj

yieldsInData0bj = getIntegralBetweenValues(extractHistogramFromFile(f, '0bjet/mll/histo_DATA;1'), xmin, xmax)
yieldsOutData0bj = getIntegralBetweenValues(extractHistogramFromFile(f, '0bjet/mll/histo_DATA;1'), 0, xmin) + getIntegralBetweenValues(extractHistogramFromFile(f, '0bjet/mll/histo_DATA;1'), xmax, 10000)
RoutinData0bj = yieldsOutData0bj/yieldsInData0bj

kappa = RoutinMC0bj/RoutinData0bj
print("Kappa: " + str(kappa))

#Apply kappa to the 1bj region to get RoutinMC
yieldsInData1bj = getIntegralBetweenValues(extractHistogramFromFile(f, '1bjetOrMore/mll/histo_DATA;1'), xmin, xmax)
yieldsOutData1bj = getIntegralBetweenValues(extractHistogramFromFile(f, '1bjetOrMore/mll/histo_DATA;1'), 0, xmin) + getIntegralBetweenValues(extractHistogramFromFile(f, '1bjetOrMore/mll/histo_DATA;1'), xmax, 10000)
RoutinData1bj = yieldsOutData1bj/yieldsInData1bj

RoutinMC = kappa * RoutinData1bj
print("RoutinMC: " + str(RoutinMC))
"""
