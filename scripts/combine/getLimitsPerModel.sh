year=2018
datacard=/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/Luca/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Datacards/${year}
datacardsCombined=datacardsCombinedModels/${year}
mediator="pseudo"
variable="BDT_output"
prefix="GroupedBkg-SmearSR-"

if [ "$model" == "scalar" ]
then
mediatorExtended="scalar"
else
mediatorExtended="pseudoscalar"
fi

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
combine -n Both${mediator} -m ${massPoint} -M AsymptoticLimits ${datacardsCombined}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/${variable}_both${massPoint}_customBins/datacard.txt
for model in "tDM" "ttDM"
do
combine -n ${model}${mediator} -m ${massPoint} -M AsymptoticLimits ${datacard}/${prefix}${model}-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/${variable}_${mediatorExtended}${massPoint}_customBins/datacard.txt
done
done

combineTool.py -M CollectLimits higgsCombineBoth${mediator}.AsymptoticLimits.mH*.root --use-dirs -o limits_both.json
combineTool.py -M CollectLimits higgsCombinetDM${mediator}.AsymptoticLimits.mH*.root --use-dirs -o limits_tDM.json
combineTool.py -M CollectLimits higgsCombinettDM${mediator}.AsymptoticLimits.mH*.root --use-dirs -o limits_ttDM.json

outputDir=limits_per_model_${mediator}_${year}
rm -r "$outputDir"
mkdir "$outputDir"

plotLimits.py limits_both_default.json 'limits_tDM_default.json:exp0:Title="tDM Expected",LineStyle=5,LineWidth=3,LineColor=612,MarkerSize=0' 'limits_ttDM_default.json:exp0:Title="ttDM Expected",LineStyle=5,LineWidth=3,LineColor=618,MarkerSize=0' --logy --x-title "Mediator mass [GeV]" --show exp #--show exp to remove observed line

mv limits*_default.json "$outputDir"/.
mv *.root "$outputDir"/.
cp limit.png limit_${mediator}_${year}.png
mv limit_${mediator}_${year}.png "$outputDir"/.
cp limit.pdf limit_${mediator}_${year}.pdf
mv limit_${mediator}_${year}.pdf "$outputDir"/.
