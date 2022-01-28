year=2018
datacard=/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/Luca/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Datacards/${year}
datacardsCombined=datacardsCombinedModels/${year}
mediator="pseudo"
#prefix="GroupedBkg-SmearSR-"
prefix="SmearSR-"

if [ "$mediator" == "scalar" ]
then
mediatorExtended="scalar"
else
mediatorExtended="pseudoscalar"
fi

for massPoint in 50 100 150 200 250 300 350 400 450 500
do

variable=BDT_output_${mediatorExtended}${massPoint}_customBinsAttempt7
#variable=DNN_output_${mediatorExtended}${massPoint}
#variable=METcorrected_pt_customBins_combine

combine -n Both${mediator} -m ${massPoint} -M AsymptoticLimits ${datacardsCombined}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/${variable}/datacard.txt
#combine -n Both${mediator} -m ${massPoint} -M AsymptoticLimits ${datacardsCombined}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll_BDT_both${massPoint}/${variable}/datacard.txt

combine -n tDM${mediator} -m ${massPoint} -M AsymptoticLimits ${datacard}/${prefix}tDM-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/ST_${variable}/datacard.txt
#combine -n tDM${mediator} -m ${massPoint} -M AsymptoticLimits ${datacard}/${prefix}tDM-${mediator}${massPoint}/${mediator}${massPoint}/ST_topCR_ll_BDT_tDM${massPoint}/ST_${variable}/datacard.txt
combine -n ttDM${mediator} -m ${massPoint} -M AsymptoticLimits ${datacard}/${prefix}ttDM-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/TTbar_${variable}/datacard.txt
#combine -n ttDM${mediator} -m ${massPoint} -M AsymptoticLimits ${datacard}/${prefix}ttDM-${mediator}${massPoint}/${mediator}${massPoint}/TTbar_topCR_ll_BDT_ttDM${massPoint}/TTbar_${variable}/datacard.txt
done

combineTool.py -M CollectLimits higgsCombineBoth${mediator}.AsymptoticLimits.mH*.root --use-dirs -o limits_both.json
combineTool.py -M CollectLimits higgsCombinetDM${mediator}.AsymptoticLimits.mH*.root --use-dirs -o limits_tDM.json
combineTool.py -M CollectLimits higgsCombinettDM${mediator}.AsymptoticLimits.mH*.root --use-dirs -o limits_ttDM.json

outputDir=limits_per_model_${mediator}_${year}
rm -r "$outputDir"
mkdir "$outputDir"

plotLimits.py limits_both_default.json 'limits_tDM_default.json:exp0:Title="tDM Expected",LineStyle=5,LineWidth=3,LineColor=612,MarkerSize=0' 'limits_ttDM_default.json:exp0:Title="ttDM Expected",LineStyle=5,LineWidth=3,LineColor=618,MarkerSize=0' --logy --x-title "Mediator mass [GeV]" # --show exp #--show exp to remove observed line

mv limits*_default.json "$outputDir"/.
mv *.root "$outputDir"/.
cp limit.png limit_${mediator}_${year}.png
mv limit_${mediator}_${year}.png "$outputDir"/.
cp limit.pdf limit_${mediator}_${year}.pdf
mv limit_${mediator}_${year}.pdf "$outputDir"/.
