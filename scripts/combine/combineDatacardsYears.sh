rm -r "datacardsCombinedYears"
mkdir "datacardsCombinedYears"

baseDir="/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/Luca/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Datacards/"
#baseDir="datacardsCombinedModels"
input2016="${baseDir}/2016/"
input2017="${baseDir}/2017/"
input2018="${baseDir}/2018/"

for mediator in "scalar" "pseudo"
do
for massPoint in 50 100 150 200 250 300 350 400 450 500
do
datacardtDM2016=${input2016}/SR-tDM-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_tDM${massPoint}_customBins/datacard.txt
datacardttDM2016=${input2016}/SR-ttDM-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_ttDM${massPoint}_customBins/datacard.txt
datacardtDM2017=${input2017}/SR-tDM-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_tDM${massPoint}_customBins/datacard.txt
datacardttDM2017=${input2017}/SR-ttDM-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_ttDM${massPoint}_customBins/datacard.txt
datacardtDM2018=${input2018}/SR-tDM-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_tDM${massPoint}_customBins/datacard.txt
datacardttDM2018=${input2018}/SR-ttDM-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_ttDM${massPoint}_customBins/datacard.txt

mkdir datacardsCombinedYears/SR-both-${mediator}${massPoint}
mkdir datacardsCombinedYears/SR-both-${mediator}${massPoint}/${mediator}${massPoint}
mkdir datacardsCombinedYears/SR-both-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/
mkdir datacardsCombinedYears/SR-both-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_both${massPoint}_customBins
combineCards.py $datacardtDM2016 $datacardttDM2016 $datacardtDM2017 $datacardttDM2017 $datacardtDM2018 $datacardttDM2018 > datacardsCombinedYears/SR-both-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_both${massPoint}_customBins/datacard.txt
done
done
