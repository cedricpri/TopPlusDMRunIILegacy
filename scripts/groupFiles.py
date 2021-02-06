import glob

inputFolder = "SignalsPostProcessing/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7A/"
outputFolder = "SignalsPostProcessing/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7/"
model = "scalar"
massPoint = "1000"

for i in range(0, 20):

    #Check that there are enough files to hadd
    numberFilesFound = len(glob.glob1(inputFolder, "nanoLatino_DM" + model +  "_Dilepton_top_tWChan_Mchi1_Mphi" + massPoint + "__part" + str(i+1) + "?.root"))

    if(numberFilesFound > 0):
        command= "hadd -fk " + outputFolder + "nanoLatino_DM" + model + "_Dilepton_top_tWChan_Mchi1_Mphi" + massPoint + "__part" + str(i) + ".root"
        command = command + " " + inputFolder + "nanoLatino_DM" + model +  "_Dilepton_top_tWChan_Mchi1_Mphi" + massPoint + "__part" + str(i+1) + "?.root"
        print command
