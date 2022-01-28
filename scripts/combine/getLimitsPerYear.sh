#datacard=/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/Luca/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Datacards/
datacard=datacardsCombinedModels/
datacardsCombined=datacardsCombinedYears/
model="both"
mediator="pseudo"
prefix="SmearSR-"
regionName="topCR_ll"

if [ "$mediator" == "scalar" ]
then
mediatorExtended="scalar"
else
mediatorExtended="pseudoscalar"
fi

for massPoint in 50 100 150 200 250 300 350 400 450 500
do

#region=${regionName}_BDT_both${massPoint}
region=${regionName}

variable="BDT_output_"${mediatorExtended}${massPoint}"_customBinsAttempt7"
#variable="METcorrected_pt_customBinsAttempt2"

combine -n AllYears -m ${massPoint} -M AsymptoticLimits ${datacardsCombined}/${prefix}${model}-${mediator}${massPoint}/${mediator}${massPoint}/${region}/${variable}/datacard.txt
for year in 2016 2017 2018
do
combine -n ${year}${mediator} -m ${massPoint} -M AsymptoticLimits ${datacard}${year}/${prefix}${model}-${mediator}${massPoint}/${mediator}${massPoint}/${region}/${variable}/datacard.txt
done
done

combineTool.py -M CollectLimits higgsCombineAllYears.AsymptoticLimits.mH*.root --use-dirs -o limits_all.json
combineTool.py -M CollectLimits higgsCombine2016${mediator}.AsymptoticLimits.mH*.root --use-dirs -o limits_2016.json
combineTool.py -M CollectLimits higgsCombine2017${mediator}.AsymptoticLimits.mH*.root --use-dirs -o limits_2017.json
combineTool.py -M CollectLimits higgsCombine2018${mediator}.AsymptoticLimits.mH*.root --use-dirs -o limits_2018.json

outputDir=limits_per_year_${mediator}
rm -r "$outputDir"
mkdir "$outputDir"

plotLimits.py limits_all_default.json 'limits_2016_default.json:exp0:Title="2016 Expected",LineStyle=5,LineWidth=3,LineColor=610,MarkerSize=0' 'limits_2017_default.json:exp0:Title="2017 Expected",LineStyle=5,LineWidth=3,LineColor=612,MarkerSize=0' 'limits_2018_default.json:exp0:Title="2018 Expected",LineStyle=5,LineWidth=3,LineColor=618,MarkerSize=0' --logy --x-title "Mediator mass [GeV]" # --show exp #--show exp to remove observed line

mv limits*_default.json "$outputDir"/.
mv *.root "$outputDir"/.
cp limit.png limit_${mediator}.png
mv limit_${mediator}.png "$outputDir"/.
cp limit.png limit_${mediator}.pdf
mv limit_${mediator}.pdf "$outputDir"/.
