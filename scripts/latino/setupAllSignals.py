year = 2018
blinded = False
hadd = True
plot = True
datacard = False
smear = True
onlySome = True

models = ["tDM", "ttDM"]
mediators = ["scalar", "pseudo"]

if blinded:
    year = "Blinded" + str(year)

for model in models:
    for mediator in mediators:
        massPoints = ["100", "500"] if onlySome else ["50", "100", "150", "200", "250", "300", "350", "400", "450", "500"]
        for massPoint in massPoints:
            if blinded:
                SR = "SRBlinded"
            else:
                SR = "SR"
            if smear:
                SR = "Smear" + SR
            #SR = "GroupedBkg-" + SR + "-" + model + "-" + mediator + massPoint
            SR = "" + SR + "-" + model + "-" + mediator + massPoint

            if plot:
                print("./run_mkPlot.sh " + str(year) + " " + SR + " SM-" + model + "-" + mediator + massPoint)
            elif datacard:
                print("./run_mkDatacards.py " + str(year) + " " + SR + " SM-" + model + "-" + mediator + massPoint)
            else:
                haddString = "1" if hadd else "0"
                print("./run_mkShapesMulti.sh " + str(year) + " " + SR + " " + haddString + " SM-" + model + "-" + mediator + massPoint + " AsMuchAsPossible")
