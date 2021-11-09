inputDir=/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Full2016_v7_blinded/datacards/

method="DNN"
model="scalar"

# ===================================================================================
#cutLevel="topCR_ll_${method}_signal0_${model}"
variable="var_${method}_signal0_${model}"

if [ "$model" == "scalar" ]
then
modelExtended="scalar"
else
modelExtended="pseudoscalar"
fi

for massPoint in 50 100 150 200 250 300 350 400 450 500
do

outputDir=impacts_${model}_${method}${massPoint}
rm -r "$outputDir"
mkdir "$outputDir"

#text2workspace
text2workspace.py ${inputDir}/topCR_ll/${variable}${massPoint}/datacard_SignalMix_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt
mv ${inputDir}/topCR_ll/${variable}${massPoint}/datacard_SignalMix_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.root ${outputDir}/${outputDir}.root

#combineTool
combineTool.py -M Impacts -d ${outputDir}/${outputDir}.root -m $massPoint --doInitialFit --robustFit 1 -t -1 --expectSignal=1
combineTool.py -M Impacts -d ${outputDir}/${outputDir}.root -m $massPoint --robustFit 1 --doFits --parallel 5 -t -1 --expectSignal=1
combineTool.py -M Impacts -d ${outputDir}/${outputDir}.root -m $massPoint -o ${outputDir}/impacts_${model}_${method}${massPoint}.json
mv *.MultiDimFit.mH${massPoint}.root ${outputDir}/.

#And plot!
plotImpacts.py -i ${outputDir}/impacts_${model}_${method}${massPoint}.json -o ${outputDir}/impacts_${model}_${method}${massPoint}
done
