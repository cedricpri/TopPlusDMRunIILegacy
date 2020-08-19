datacard=~/work/public/Latinos/TopPlusDMRunIILegacy/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Full2018_v6_limits/datacards/
model="scalar"
training="Mchi_1_Mphi_100_fivemore"
variable="mt2ll"
method="DNN"

for massPoint in 50 #100 150 200 250 300 350 400 450 500
do

outputDir=impacts_tDM_"$model"_"$training"_"$method"_Mchi_1_Mphi_"$massPoint"
rm -r "$outputDir"
mkdir "$outputDir"

#text2workspace
text2workspace.py ${datacard}topCR_ll_${method}_signal0_${model}_LO_${training}/${variable}/datacard_DM{$model}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.txt
mv ${datacard}topCR_ll_${method}_signal0_${model}_LO_${training}/${variable}/datacard_DM{$model}_Dilepton_top_tWChan_Mchi1_Mphi${massPoint}.root "$outputDir"/"$outputDir".root

#combineTool
combineTool.py -M Impacts -d "$outputDir"/"$outputDir".root -m $massPoint --doInitialFit --robustFit 1 -t -1 --expectSignal=1
combineTool.py -M Impacts -d "$outputDir"/"$outputDir".root -m $massPoint --robustFit 1 --doFits --parallel 5 -t -1 --expectSignal=1
combineTool.py -M Impacts -d "$outputDir"/"$outputDir".root -m $massPoint -o "$outputDir"/impacts_tDM_"$model"_"$training"_"$method"_Mchi_1_Mphi_"$massPoint".json
mv *.MultiDimFit.mH${massPoint}.root "$outputDir$"/.

#And plot!
plotImpacts.py -i "$outputDir"/impacts_tDM_"$model"_"$training"_"$method"_Mchi_1_Mphi_"$massPoint".json -o "$outputDir"/impacts_tDM_"$model"_"$training"_"$method"_Mchi_1_Mphi_"$massPoint"
done
