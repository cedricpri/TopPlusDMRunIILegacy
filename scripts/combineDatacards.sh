rm -r "datacardsCombined"
mkdir "datacardsCombined"
mkdir "datacardsCombined/topCR_ll/"

baseDir="/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/"
input2016="${baseDir}/Full2016_v7_blinded/datacardsHighXS/topCR_ll/"
input2017="${baseDir}/Full2017_v7_blinded/datacardsHighXS/topCR_ll/"
input2018="${baseDir}/Full2018_v7_blinded/datacardsHighXS/topCR_ll/"

method="DNN"
model="scalar"

# ===================================================================================
cutLevel="topCR_ll_${method}_signal0_${model}"
variable="${method}_category_${model}"

if [ "$model" == "scalar" ]
then
modelExtended="scalar"
else
modelExtended="pseudoscalar"
fi

outputDir=limits_${model}_${method}

for massPoint in 50 100 150 200 250 300 350 400 450 500
do
for datacard in ${input2016}/${method}_category_${model}${massPoint}/*.txt; do
mkdir datacardsCombined/topCR_ll/${method}_category_${model}${massPoint}
combineCards.py $datacard "${datacard/Full2016/Full2017}" "${datacard/Full2016/Full2018}" > datacardsCombined/topCR_ll/${method}_category_${model}${massPoint}/$(basename $datacard)
done
done
