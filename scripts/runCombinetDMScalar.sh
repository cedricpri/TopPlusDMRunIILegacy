combine -n tDMScalar -m 10 -M AsymptoticLimits datacards/topCR_ll_DNN_signal1/mt2ll/datacard_DMscalar_Dilepton_top_tWChan_Mchi1_Mphi10.txt
combine -n tDMScalar -m 20 -M AsymptoticLimits datacards/topCR_ll_DNN_signal1/mt2ll/datacard_DMscalar_Dilepton_top_tWChan_Mchi1_Mphi20.txt
combine -n tDMScalar -m 50 -M AsymptoticLimits datacards/topCR_ll_DNN_signal1/mt2ll/datacard_DMscalar_Dilepton_top_tWChan_Mchi1_Mphi50.txt
combine -n tDMScalar -m 100 -M AsymptoticLimits datacards/topCR_ll_DNN_signal1/mt2ll/datacard_DMscalar_Dilepton_top_tWChan_Mchi1_Mphi100.txt
combine -n tDMScalar -m 200 -M AsymptoticLimits datacards/topCR_ll_DNN_signal1/mt2ll/datacard_DMscalar_Dilepton_top_tWChan_Mchi1_Mphi200.txt
combine -n tDMScalar -m 300 -M AsymptoticLimits datacards/topCR_ll_DNN_signal1/mt2ll/datacard_DMscalar_Dilepton_top_tWChan_Mchi1_Mphi300.txt
combine -n tDMScalar -m 500 -M AsymptoticLimits datacards/topCR_ll_DNN_signal1/mt2ll/datacard_DMscalar_Dilepton_top_tWChan_Mchi1_Mphi500.txt
combine -n tDMScalar -m 1000 -M AsymptoticLimits datacards/topCR_ll_DNN_signal1/mt2ll/datacard_DMscalar_Dilepton_top_tWChan_Mchi1_Mphi1000.txt

combineTool.py -M CollectLimits higgsCombinetDMScalar.AsymptoticLimits.mH*.root --use-dirs -o limitstDMScalar.json
