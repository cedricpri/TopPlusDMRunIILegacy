rm -r "datacardsCombinedModels"
mkdir "datacardsCombinedModels"

input="/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/Luca/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Datacards/"
prefix="GroupedBkg-SmearSR-"
mediator="pseudo"

if [ "$mediator" == "scalar" ]
then
mediatorExtended="scalar"
else
mediatorExtended="pseudoscalar"
fi

for year in 2018 #2017 2018
do
mkdir datacardsCombinedModels/${year}

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
datacardtDM=${input}${year}/${prefix}tDM-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_${mediatorExtended}${massPoint}_customBins/datacard.txt
datacardttDM=${input}${year}/${prefix}ttDM-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_${mediatorExtended}${massPoint}_customBins/datacard.txt

mkdir datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}
mkdir datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}
mkdir datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/
mkdir datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_both${massPoint}_customBins
combineCards.py $datacardtDM $datacardttDM > datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_both${massPoint}_customBins/datacard.txt

cp -r ${input}${year}/${prefix}ttDM-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_${mediatorExtended}${massPoint}_customBins/shapes datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/topCR_ll/BDT_output_both${massPoint}_customBins/.
done
done
