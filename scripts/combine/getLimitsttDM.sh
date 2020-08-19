datacard=~/work/public/Latinos/TopPlusDMRunIILegacy/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Full2018_v6_limits/datacards/
model="scalar"
training="Mchi_1_Mphi_100_fivemore"
variable="mt2ll"
method="DNN"

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
combine -n ttDM${model} -m ${massPoint} -M AsymptoticLimits ${datacard}topCR_ll_${method}_signal0_${model}_LO_${training}/${variable}/datacard_TTbarDMJets_Dilepton_${model}_LO_Mchi_1_Mphi_${massPoint}.txt
done

combineTool.py -M CollectLimits higgsCombinettDM${model}.AsymptoticLimits.mH*.root --use-dirs -o limits.json

outputDir=limits_ttDM_${model}_${training}_${method}
rm -r "$outputDir"
mkdir "$outputDir"

plotLimits.py limits_default.json --logy --x-title "Mediator [GeV]" --show exp 

mv limits_default.json "$outputDir"/.
mv *.root "$outputDir"/.
cp limit.png limit_tDM_"$model"_"$training"_"$method".png
mv limit.png "$outputDir"/.
mv limit.pdf "$outputDir"/.
