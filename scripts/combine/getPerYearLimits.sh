inputDir=/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Full2017_v7_blinded/datacards/
inputDirCombined=datacardsCombinedPseudo/

method="DNN"
model="pseudo"

# ===================================================================================
cutLevel="topCR_ll_${method}_signal0_${model}"
variable="var_${method}_signal0_${model}"

if [ "$model" == "scalar" ]
then
modelExtended="scalar"
else
modelExtended="pseudoscalar"
fi

outputDir=limits_${model}_${method}

for massPoint in 50 100 150 200 250 300 350 400 450 500; do
combine -n AllYears -m ${massPoint} -M AsymptoticLimits ${inputDirCombined}/topCR_ll/${variable}${massPoint}/datacard_SignalMix_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt

for year in 2016 2017 2018; do
combine -n ${year} -m ${massPoint} -M AsymptoticLimits "${inputDir/Full201?/Full$year}"/topCR_ll/${variable}${massPoint}/datacard_SignalMix_DM${modelExtended}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt
done
done

combineTool.py -M CollectLimits higgsCombine2016.AsymptoticLimits.mH*.root --use-dirs -o limits2016.json
combineTool.py -M CollectLimits higgsCombine2017.AsymptoticLimits.mH*.root --use-dirs -o limits2017.json
combineTool.py -M CollectLimits higgsCombine2018.AsymptoticLimits.mH*.root --use-dirs -o limits2018.json
combineTool.py -M CollectLimits higgsCombineAllYears.AsymptoticLimits.mH*.root --use-dirs -o limitsAllYears.json

plotLimits.py limitsAllYears_default.json 'limits2016_default.json:exp0:Title="2016 Expected",LineStyle=5,LineWidth=3,LineColor=429,MarkerSize=0' 'limits2017_default.json:exp0:Title="2017 Expected",LineStyle=5,LineWidth=3,LineColor=591,MarkerSize=0' 'limits2018_default.json:exp0:Title="2018 Expected",LineStyle=5,LineWidth=3,LineColor=597,MarkerSize=0' --logy --x-title "Mediator mass [GeV]" --show exp #--show exp to remove observed line

rm -r "$outputDir"
mkdir "$outputDir"

mv limits*_default.json "$outputDir"/.
mv *.root "$outputDir"/.
mv limit.png "$outputDir"/.
mv limit.pdf "$outputDir"/.
