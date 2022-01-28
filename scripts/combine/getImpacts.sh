year="2016"
datacard=/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/Luca/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Datacards/${year}
datacardsCombined=datacardsCombinedModels/${year}
mediator="scalar"
model="both"
SR="SR"
prefix="Smear"
suffix=""

if [ "$mediator" == "scalar" ]
then
mediatorExtended="scalar"
else
mediatorExtended="pseudoscalar"
fi

outputDir=impacts_${year}_${model}_${mediator}
rm -r "$outputDir"
mkdir "$outputDir"

for massPoint in 100 500 # 150 200 250 300 350 400 450
do

variable=BDT_output_${mediatorExtended}${massPoint}_customBinsAttempt7
#variable="METcorrected_pt_customBins"

#text2workspace
text2workspace.py ${datacardsCombined}/${prefix}${SR}-${model}-${mediator}${massPoint}${suffix}/${mediator}${massPoint}/topCR_ll/${variable}/datacard.txt
mv ${datacardsCombined}/${prefix}${SR}-${model}-${mediator}${massPoint}${suffix}/${mediator}${massPoint}/topCR_ll/${variable}/datacard.root "$outputDir"/"$outputDir""$massPoint".root

#combineTool
combineTool.py -M Impacts -d ${outputDir}/${outputDir}${massPoint}.root -m $massPoint --doInitialFit --robustFit 1 -t -1 --expectSignal=1
combineTool.py -M Impacts -d ${outputDir}/${outputDir}${massPoint}.root -m $massPoint --robustFit 1 --doFits --parallel 10 -t -1 --expectSignal=1
combineTool.py -M Impacts -d ${outputDir}/${outputDir}${massPoint}.root -m $massPoint -o ${outputDir}/impacts_${year}_${model}_${massPoint}.json
mv *.MultiDimFit.mH${massPoint}.root ${outputDir}/.

#And plot!
plotImpacts.py -i "$outputDir"/impacts_${year}_${model}_${massPoint}.json -o "$outputDir"/impacts_${year}_${model}_${mediator}_${massPoint}
done
