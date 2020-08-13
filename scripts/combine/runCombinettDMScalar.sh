combine -n ttDMScalar -m 50 -M AsymptoticLimits datacards/topCR_ll_DNN_signal0/mt2ll/datacard_TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_50.txt
combine -n ttDMScalar -m 100 -M AsymptoticLimits datacards/topCR_ll_DNN_signal0/mt2ll/datacard_TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_100.txt
combine -n ttDMScalar -m 150 -M AsymptoticLimits datacards/topCR_ll_DNN_signal0/mt2ll/datacard_TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_150.txt
combine -n ttDMScalar -m 200 -M AsymptoticLimits datacards/topCR_ll_DNN_signal0/mt2ll/datacard_TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_200.txt
combine -n ttDMScalar -m 250 -M AsymptoticLimits datacards/topCR_ll_DNN_signal0/mt2ll/datacard_TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_250.txt
combine -n ttDMScalar -m 300 -M AsymptoticLimits datacards/topCR_ll_DNN_signal0/mt2ll/datacard_TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_300.txt
combine -n ttDMScalar -m 350 -M AsymptoticLimits datacards/topCR_ll_DNN_signal0/mt2ll/datacard_TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_350.txt
combine -n ttDMScalar -m 400 -M AsymptoticLimits datacards/topCR_ll_DNN_signal0/mt2ll/datacard_TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_400.txt
combine -n ttDMScalar -m 450 -M AsymptoticLimits datacards/topCR_ll_DNN_signal0/mt2ll/datacard_TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_450.txt
combine -n ttDMScalar -m 500 -M AsymptoticLimits datacards/topCR_ll_DNN_signal0/mt2ll/datacard_TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_500.txt

combineTool.py -M CollectLimits higgsCombinettDMScalar.AsymptoticLimits.mH*.root --use-dirs -o limitsttDMScalar.json
