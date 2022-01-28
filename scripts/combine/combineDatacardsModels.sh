#rm -r "datacardsCombinedModels"
#mkdir "datacardsCombinedModels"

input="/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/Luca/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Datacards/"
prefix="SmearSR-"
mediator="scalar"
regionName="topCR_ll"

if [ "$mediator" == "scalar" ]
then
mediatorExtended="scalar"
else
mediatorExtended="pseudoscalar"
fi

for year in 2016 2017 2018
do
mkdir datacardsCombinedModels/${year}

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
#regiontDM=ST_${regionName}_BDT_tDM${massPoint}
#regionttDM=TTbar_${regionName}_BDT_ttDM${massPoint}
#regionboth=${regionName}_BDT_both${massPoint}

regiontDM=${regionName}
regionttDM=${regionName}
regionboth=${regionName}

variable=BDT_output_${mediatorExtended}${massPoint}_customBinsAttempt7
#variable=DNN_output_${mediatorExtended}${massPoint}
#variable=METcorrected_pt_customBins_combine

datacardtDM=${input}${year}/${prefix}tDM-${mediator}${massPoint}/${mediator}${massPoint}/${regiontDM}/ST_${variable}/datacard.txt
datacardttDM=${input}${year}/${prefix}ttDM-${mediator}${massPoint}/${mediator}${massPoint}/${regionttDM}/TTbar_${variable}/datacard.txt

mkdir datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}
mkdir datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}
mkdir datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/
mkdir datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/${variable}
combineCards.py $datacardtDM $datacardttDM > datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/${variable}/datacard.txt

#rm -r datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/ST_${variable}
mkdir datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/ST_${variable}
cp -r ${input}${year}/${prefix}tDM-${mediator}${massPoint}/${mediator}${massPoint}/${regiontDM}/ST_${variable}/shapes datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/ST_${variable}/.

#rm -r datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/TTbar_${variable}
mkdir datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/TTbar_${variable}
cp -r ${input}${year}/${prefix}ttDM-${mediator}${massPoint}/${mediator}${massPoint}/${regionttDM}/TTbar_${variable}/shapes datacardsCombinedModels/${year}/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/TTbar_${variable}/.
done
done
