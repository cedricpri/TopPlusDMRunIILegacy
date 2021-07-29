year = "2016"
for massPoint in (50, 100, 150, 200, 250, 300, 350, 400, 450, 500):
    print("python createJobsTrainMVA.py -y " + str(year) + " -s _Mphi_" + str(massPoint) + "_,Mphi" + str(massPoint) + "_ -m scalar")
    print("python createJobsTrainMVA.py -y " + str(year) + " -s _Mphi_" + str(massPoint) + "_,Mphi" + str(massPoint) + "_ -m pseudo")

    print("python createJobsTrainMVA.py -y " + str(year) + " -r -s _Mphi_" + str(massPoint) + "_,Mphi" + str(massPoint) + "_ -m scalar")
    print("python createJobsTrainMVA.py -y " + str(year) + " -r -s _Mphi_" + str(massPoint) + "_,Mphi" + str(massPoint) + "_ -m pseudo")
