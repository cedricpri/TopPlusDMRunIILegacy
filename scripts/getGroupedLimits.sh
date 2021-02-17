inputDir=/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Full2016_v7_blinded/datacards/

method="DNN"
model="pseudo"

# ===================================================================================
#cutLevel="topCR_ll" #Without MVA applied
cutLevel="topCR_ll_${method}_signal0_${model}"
variable="${method}_category_${model}"

if [ "$model" == "scalar" ]
then
modelExtended="scalar"
else
modelExtended="pseudoscalar"
fi

outputDir=limits_${model}_${method}

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
combine -n tDM${model} -m ${massPoint} -M AsymptoticLimits ${inputDir}/${cutLevel}${massPoint}/${variable}${massPoint}/datacard_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt
done

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
combine -n ttDM${model} -m ${massPoint} -M AsymptoticLimits ${inputDir}/${cutLevel}${massPoint}/${variable}${massPoint}/datacard_TTbarDMJets_Dilepton_${modelExtended}_LO_Mchi_1_Mphi_${massPoint}.txt
done

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
combine -n combined${model} -m ${massPoint} -M AsymptoticLimits ${inputDir}/${cutLevel}${massPoint}/${variable}${massPoint}/datacard_SignalMix_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt
done

combineTool.py -M CollectLimits higgsCombinetDM${model}.AsymptoticLimits.mH*.root --use-dirs -o limitstDM.json
combineTool.py -M CollectLimits higgsCombinettDM${model}.AsymptoticLimits.mH*.root --use-dirs -o limitsttDM.json
combineTool.py -M CollectLimits higgsCombinecombined${model}.AsymptoticLimits.mH*.root --use-dirs -o limitsCombined.json

rm -r "$outputDir"
mkdir "$outputDir"

plotLimits.py limitsCombined_default.json 'limitstDM_default.json:exp0:Title="tDM Expected",LineStyle=5,LineWidth=3,LineColor=429,MarkerSize=0' 'limitsttDM_default.json:exp0:Title="ttDM Expected",LineStyle=5,LineWidth=3,LineColor=596,MarkerSize=0' --logy --x-title "Mediator [GeV]" --show exp #--show exp to remove observed line

mv limits*_default.json "$outputDir"/.
mv *.root "$outputDir"/.
cp limit.png limit.png
mv limit.png "$outputDir"/.
mv limit.pdf "$outputDir"/.
