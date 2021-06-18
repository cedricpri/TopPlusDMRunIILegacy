years = ["2016","2017","2018"]
for year in years:
    if year == "2016":
        runs=["B", "C", "D", "E", "F", "G", "H"]
    elif year == "2017":
        runs=["B","C","D","E","F"]
    elif year =="2018":
        runs=["A","B","C","D"]

    for run in runs:
        suffix = "-v1"
        if year == "2016" and run == "B":
            suffix = "_ver2-v1"
        elif year == "2018" and run == "D":
            suffix = "_ver2-v1"

        print("python triggerEstimator.py --filename=/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/Run" + year + "_102X_nAODv6_Full" + year + "v6loose/DATASusy" + year + "v6__hadd/nanoLatino_MET_Run" + year + run + "-Nano25Oct2019" + suffix + ".root --year " + year +" --tag " + year + run)
