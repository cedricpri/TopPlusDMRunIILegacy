inputDir=/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Full2018_v7_blinded/datacards/

method="DNN"
model="pseudo"

# ===================================================================================
#cutLevel="topCR_ll_${method}_signal0_${model}"
#variable="${method}_${category}_shape_${model}"

if [ "$model" == "scalar" ]
then
modelExtended="scalar"
else
modelExtended="pseudoscalar"
fi

outputDir=limits_${model}_${method}

rm -r "datacards"
mkdir "datacards"

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
#Combine the TTbar and ST datacards
mkdir "datacards/${method}_shape_${model}${massPoint}"
combineCards.py ${inputDir}/presel_ST_ll/${method}_ST_shape_${model}${massPoint}/datacard_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt ${inputDir}/presel_TTbar_ll/${method}_TTbar_shape_${model}${massPoint}/datacard_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt > datacards/${method}_shape_${model}${massPoint}/datacard_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt
combine -n tDM${model} -m ${massPoint} -M AsymptoticLimits datacards/${method}_shape_${model}${massPoint}/datacard_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt
done

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
#Combine the TTbar and ST datacards
combineCards.py ${inputDir}/presel_ST_ll/${method}_ST_shape_${model}${massPoint}/datacard_TTbarDMJets_Dilepton_${modelExtended}_LO_Mchi_1_Mphi_${massPoint}.txt ${inputDir}/presel_TTbar_ll/${method}_TTbar_shape_${model}${massPoint}/datacard_TTbarDMJets_Dilepton_${modelExtended}_LO_Mchi_1_Mphi_${massPoint}.txt > datacards/${method}_shape_${model}${massPoint}/datacard_TTbarDMJets_Dilepton_${modelExtended}_LO_Mchi_1_Mphi_${massPoint}.txt
combine -n ttDM${model} -m ${massPoint} -M AsymptoticLimits datacards/${method}_shape_${model}${massPoint}/datacard_TTbarDMJets_Dilepton_${modelExtended}_LO_Mchi_1_Mphi_${massPoint}.txt
done

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
combineCards.py ${inputDir}/presel_ST_ll/${method}_ST_shape_${model}${massPoint}/datacard_SignalMix_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt ${inputDir}/presel_TTbar_ll/${method}_TTbar_shape_${model}${massPoint}/datacard_SignalMix_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt > datacards/${method}_shape_${model}${massPoint}/datacard_SignalMix_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt
combine -n combined${model} -m ${massPoint} -M AsymptoticLimits datacards/${method}_shape_${model}${massPoint}/datacard_SignalMix_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt
done

combineTool.py -M CollectLimits higgsCombinetDM${model}.AsymptoticLimits.mH*.root --use-dirs -o limitstDM.json
combineTool.py -M CollectLimits higgsCombinettDM${model}.AsymptoticLimits.mH*.root --use-dirs -o limitsttDM.json
combineTool.py -M CollectLimits higgsCombinecombined${model}.AsymptoticLimits.mH*.root --use-dirs -o limitsCombined.json

plotLimits.py limitsCombined_default.json 'limitstDM_default.json:exp0:Title="tDM Expected",LineStyle=5,LineWidth=3,LineColor=429,MarkerSize=0' 'limitsttDM_default.json:exp0:Title="ttDM Expected",LineStyle=5,LineWidth=3,LineColor=596,MarkerSize=0' --logy --x-title "Mediator mass [GeV]" --show exp #--show exp to remove observed line

rm -r "$outputDir"
mkdir "$outputDir"

mv limits*_default.json "$outputDir"/.
mv *.root "$outputDir"/.
mv limit.png "$outputDir"/.
mv limit.pdf "$outputDir"/.
