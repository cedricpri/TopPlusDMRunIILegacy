datacard=/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/Luca/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Datacards/2018/
model="ttDM"
mediator="pseudo"
variable="BDT_output"
#variable="mt2ll"
prefix="GroupedBkg-Smear"
suffix=""

if [ "$mediator" == "scalar" ]
then
mediatorExtended="scalar"
else
mediatorExtended="pseudoscalar"
fi

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
combine -n ${model}${mediator} -m ${massPoint} -M AsymptoticLimits ${datacard}/${prefix}SR${suffix}-${model}-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/${variable}_${mediatorExtended}${massPoint}_customBins/datacard.txt
#combine -n ${model}${mediator} -m ${massPoint} -M AsymptoticLimits ${datacard}/${prefix}SR${suffix}-${model}-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll_BDT_${model}${massPoint}/${variable}_${mediator}${massPoint}_customBins/datacard.txt
#combine -n ${model}${mediator} -m ${massPoint} -M AsymptoticLimits ${datacard}/${prefix}SR${suffix}-${model}-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/${variable}/datacard.txt #For mt2ll
done

combineTool.py -M CollectLimits higgsCombine${model}${mediator}.AsymptoticLimits.mH*.root --use-dirs -o limits.json

outputDir=limits_${model}_${mediator}
rm -r "$outputDir"
mkdir "$outputDir"


plotLimits.py limits_default.json --logy --x-title "Mediator [GeV]" --show exp --auto-style
#plotLimits.py 'limits_default.json:exp0:LineStyle=10' --logy --x-title "Mediator mass [GeV]" --show exp #--show exp to remove observed line
#--show exp to remove observed line

mv limits_default.json "$outputDir"/.
mv *.root "$outputDir"/.
cp limit.png limit_"$model"_"$mediator".png
mv limit.png "$outputDir"/.
mv limit.pdf "$outputDir"/.
