#rm -r "datacardsCombinedYears"
#mkdir "datacardsCombinedYears"

baseDir="/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/Luca/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Datacards/"
#baseDir="datacardsCombinedModels"
input2016="${baseDir}/2016/"
input2017="${baseDir}/2017/"
input2018="${baseDir}/2018/"
prefix="SmearSR-"
mediator="scalar"
regionName="topCR_ll"

if [ "$mediator" == "scalar" ]
then
mediatorExtended="scalar"
else
mediatorExtended="pseudoscalar"
fi

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
#regiontDM=${regionName}_BDT_tDM${massPoint}
#regionttDM=${regionName}_BDT_ttDM${massPoint}
#regionboth=${regionName}_BDT_both${massPoint}

regiontDM=${regionName}
regionttDM=${regionName}
regionboth=${regionName}

variable=BDT_output_${mediatorExtended}${massPoint}_customBinsAttempt7
#variable=METcorrected_pt_customBins_combine

datacardtDM2016=${input2016}/${prefix}tDM-${mediator}${massPoint}/${mediator}${massPoint}/${regiontDM}/ST_${variable}/datacard.txt
datacardttDM2016=${input2016}/${prefix}ttDM-${mediator}${massPoint}/${mediator}${massPoint}/${regionttDM}/TTbar_${variable}/datacard.txt
datacardtDM2017=${input2017}/${prefix}tDM-${mediator}${massPoint}/${mediator}${massPoint}/${regiontDM}/ST_${variable}/datacard.txt
datacardttDM2017=${input2017}/${prefix}ttDM-${mediator}${massPoint}/${mediator}${massPoint}/${regionttDM}/TTbar_${variable}/datacard.txt
datacardtDM2018=${input2018}/${prefix}tDM-${mediator}${massPoint}/${mediator}${massPoint}/${regiontDM}/ST_${variable}/datacard.txt
datacardttDM2018=${input2018}/${prefix}ttDM-${mediator}${massPoint}/${mediator}${massPoint}/${regionttDM}/TTbar_${variable}/datacard.txt

mkdir datacardsCombinedYears/${prefix}both-${mediator}${massPoint}
mkdir datacardsCombinedYears/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}
mkdir datacardsCombinedYears/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/
mkdir datacardsCombinedYears/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/${variable}
combineCards.py $datacardtDM2016 $datacardttDM2016 $datacardtDM2017 $datacardttDM2017 $datacardtDM2018 $datacardttDM2018 > datacardsCombinedYears/${prefix}both-${mediator}${massPoint}/${mediator}${massPoint}/${regionboth}/${variable}/datacard.txt
done
