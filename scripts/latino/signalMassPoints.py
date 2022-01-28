import collections

unorderedSignalMassPoints = {}

mediators = ["scalar", "pseudo"]
for mediator in mediators:
    for mPhi in [50,  100, 150, 200, 250, 300, 350, 400, 450, 500]:
        #tDM
        datasetName = 'DM' + mediator + '_Dilepton_top_tWChan_Mchi1_Mphi' + str(mPhi)
        massPointName = mediator + str(mPhi)
    
        massPoint = {}
        massPoint['dataset'] = datasetName
        if mPhi == 50 and mediator == "pseudo":
            massPoint['weight'] = '0.11706' #Avoid using the inclusive xs
        else:
            massPoint['weight'] = '0.10706' #Avoid using the inclusive xs
        unorderedSignalMassPoints['tDM-' + massPointName] = massPoint

        #ttDM
        datasetName = 'TTbarDMJets_Dilepton_' + mediator + '_LO_Mchi_1_Mphi_' + str(mPhi)
        massPointName = mediator + str(mPhi)
    
        massPoint = {}
        massPoint['dataset'] = datasetName
        massPoint['weight'] = '1'
        unorderedSignalMassPoints['ttDM-' + massPointName] = massPoint

signalMassPoints = collections.OrderedDict(sorted(unorderedSignalMassPoints.items()))

def massPointInSignalSet(massPoint, sigSet, checkModel = True):

    options = sigSet.split("-")
    if len(options) > 1:
        modelSelected = options[1]
        massPointSelected = options[2]

    if massPoint == modelSelected + "-" + massPointSelected:
        return True
    elif modelSelected == "both" and massPoint.split("-")[1] == massPointSelected:
        return True
    elif not checkModel and massPoint.split("-")[1] == massPointSelected:
        return True

    return False
