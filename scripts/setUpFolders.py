year = "2017"

if year == "2018":
    productionName = "Autumn18_102X_nAODv6_Full2018v6loose"
    productionNameSignal = "Autumn18_102X_nAODv7_Full2018v7"
elif year == "2017":
    productionName = "Fall2017_102X_nAODv6_Full2017v6loose"
    productionNameSignal = "Fall2017_102X_nAODv7_Full2017v7"
elif year == "2016":
    productionName = "Summer16_102X_nAODv6_Full2016v6loose"
    productionNameSignal = "Summer16_102X_nAODv7_Full2016v7loose"

for systematic in ["METDo", "METUp", "JESDo", "JESUp"]:
    if "MET" in systematic:
        print("ln -s /eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/" + productionNameSignal + "/MCSusy" + year + "v6loose__MCSusyCorr" + year + "v6loose__MCSusyNomin" + year + "v6loose__susyMT2recoNomin__susyMT2reco" + systematic + "_weighted/* /eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/" + productionName + "/MCSusy" + year + "v6loose__MCSusyCorr" + year + "v6loose__MCSusyNomin" + year + "v6loose__susyMT2reco" + systematic + "_weighted/")
    else:
        print("ln -s /eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/" + productionNameSignal + "/MCSusy" + year + "v6loose__MCSusyCorr" + year + "v6loose__MCSusyNomin" + year + "v6loose__susyMT2recoNomin__susyMT2reco" + systematic + "_weighted/* /eos/user/c/cprieels/work/TopPlusDMRunIILegacyRootfiles/" + productionName + "/MCSusy" + year + "v6loose__MCSusyCorr" + year + "v6loose__MCSusy" + systematic + year + "v6loose__susyMT2reco" + systematic + "_weighted/")
