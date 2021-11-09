year="2018"
datacard=/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/Luca/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Datacards/${year}
model="ttDM"
mediator="scalar"
variable="BDT_output"
#variable="METcorrected_pt"
#SR="SRFullSystNoJER"
SR="SR"
prefix="GroupedBkg-Smear"
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

for massPoint in 100 500 #150 200 250 300 350 400 450 500
do

#text2workspace
text2workspace.py ${datacard}/${prefix}${SR}-${model}-${mediator}${massPoint}${suffix}/${mediator}${massPoint}/topCR_ll/${variable}_${mediatorExtended}${massPoint}_customBins/datacard.txt
mv ${datacard}/${prefix}${SR}-${model}-${mediator}${massPoint}${suffix}/${mediator}${massPoint}/topCR_ll/${variable}_${mediatorExtended}${massPoint}_customBins/datacard.root "$outputDir"/"$outputDir""$massPoint".root
#text2workspace.py ${datacard}/${prefix}${SR}-${model}-${mediator}${massPoint}${suffix}/${mediator}${massPoint}/topCR_ll/${variable}/datacard.txt
#mv ${datacard}/${prefix}${SR}-${model}-${mediator}${massPoint}${suffix}/${mediator}${massPoint}/topCR_ll/${variable}/datacard.root "$outputDir"/"$outputDir""$massPoint".root

#combineTool
combineTool.py -M Impacts -d ${outputDir}/${outputDir}${massPoint}.root -m $massPoint --doInitialFit --robustFit 1 -t -1 --expectSignal=1
combineTool.py -M Impacts -d ${outputDir}/${outputDir}${massPoint}.root -m $massPoint --robustFit 1 --doFits --parallel 10 -t -1 --expectSignal=1
combineTool.py -M Impacts -d ${outputDir}/${outputDir}${massPoint}.root -m $massPoint -o ${outputDir}/impacts_${year}_${model}_${massPoint}.json
mv *.MultiDimFit.mH${massPoint}.root ${outputDir}/.

#And plot!
plotImpacts.py -i "$outputDir"/impacts_${year}_${model}_${massPoint}.json -o "$outputDir"/impacts_${year}_${model}_${mediator}_${massPoint}
done
