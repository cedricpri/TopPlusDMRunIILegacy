for massPoint in (50, 100, 150, 200, 250, 300, 350, 400, 450, 500):
    #print("python createJobsTrainMVA.py -b TTTo2L2Nu__part,ST_s-channel_ext1,ST_t-channel_antitop,ST_t-channel_top,ST_tW_antitop_ext1,ST_tW_top_ext1,TTWJetsToLNu,TTWjets,TTZToLLNuNu_M-10,TTZjets -s TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_" + str(massPoint) + "_,DMscalar_Dilepton_top_tWChan_Mchi1_Mphi" + str(massPoint) + "_ --tag training11")
    #print("python createJobsTrainMVA.py -b TTTo2L2Nu__part,ST_s-channel_ext1,ST_t-channel_antitop,ST_t-channel_top,ST_tW_antitop_ext1,ST_tW_top_ext1 -s TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_" + str(massPoint) + "_,DMscalar_Dilepton_top_tWChan_Mchi1_Mphi" + str(massPoint) + "_ -y 2016")
    #print("python createJobsTrainMVA.py -b TTTo2L2Nu__part,ST_s-channel_ext1,ST_t-channel_antitop,ST_t-channel_top,ST_tW_antitop_ext1,ST_tW_top_ext1 -s TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_" + str(massPoint) + "_,DMpseudoscalar_Dilepton_top_tWChan_Mchi1_Mphi" + str(massPoint) + "_ -y 2016")

    print("python createJobsTrainMVA.py -y 2016 -b TTTo2L2Nu__part -s TTbarDMJets_Dilepton_scalar_LO_Mchi_1_Mphi_" + str(massPoint) + "_")
    print("python createJobsTrainMVA.py -y 2016 -b TTTo2L2Nu__part -s TTbarDMJets_Dilepton_pseudoscalar_LO_Mchi_1_Mphi_" + str(massPoint) + "_")

    #print("python createJobsTrainMVA.py -y 2016 -s DMscalar_Dilepton_top_tWChan_Mchi1_Mphi" + str(massPoint) + "_ -b TTTo2L2Nu__part,ST_s-channel_ext1,ST_t-channel_antitop,ST_t-channel_top,ST_tW_antitop_ext1,ST_tW_top_ext1")
    #print("python createJobsTrainMVA.py -y 2016 -s DMpseudoscalar_Dilepton_top_tWChan_Mchi1_Mphi" + str(massPoint) + "_ -b TTTo2L2Nu__part,ST_s-channel_ext1,ST_t-channel_antitop,ST_t-channel_top,ST_tW_antitop_ext1,ST_tW_top_ext1")
