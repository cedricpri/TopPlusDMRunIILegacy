from optparse import OptionParser
import ROOT as ROOT
import fnmatch

from array import * 
from os import walk

#------------------------------------- MAIN --------------------------------------------
if __name__ == '__main__':

    parser = OptionParser(usage="%prog --help")
    parser.add_option("-f","--filename",   dest="filename",    help="File name",       default='file.root',             type='string')
    parser.add_option("-i","--inputDir",   dest="inputDir",    help="Input directory", default='',                      type='string')
    parser.add_option("-m","--ismc",       dest="ismc",        help="Is Montecarlo?",  default=0,                       type=int)
    parser.add_option("-l","--isLatino",   dest="isLatino",    help="Is Latino tree?", default=0,                       type=int)
    parser.add_option("-y","--year",       dest="year",        help="Year",            default='2016',                  type='string')
    parser.add_option("-t","--tag",        dest="tag",         help="Tag",             default='runB',                  type='string')

    (options, args) = parser.parse_args()
    filename = options.filename
    inputDir = options.inputDir
    ismc = options.ismc
    isLatino = options.isLatino
    year = options.year
    tag = options.tag 
    if ismc == 1:
        tag = "MC"

    plots2D = False

    ##########################List of weights that have to be applied to MC###############################
    mcweights  = 'baseW*genWeight*puWeight*TriggerEffWeight_2l'

    leptonGen = '(Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1] + (1. - Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1])*1.30)'

    vetoEENoise = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==0)'
    #vetoHEMele = '(((Sum$(Electron_pt>30. && Electron_eta>-3.0 && Electron_eta<-1.4 && Electron_phi>-1.57 && Electron_phi<-0.87)==0) && (Sum$(Jet_pt>30. && Jet_eta>-3.2 && Jet_eta<-1.2 && Jet_phi>-1.77 && Jet_phi<-0.67)==0)) + (1.-((Sum$(Electron_pt>30. && Electron_eta>-3.0 && Electron_eta<-1.4 && Electron_phi>-1.57 && Electron_phi<-0.87)==0) && (Sum$(Jet_pt>30. && Jet_eta>-3.2 && Jet_eta<-1.2 && Jet_phi>-1.77 && Jet_phi<-0.67)==0)))*0.35225285)'
    vetoHEMele = '1'

    flags = '(Flag_goodVertices*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter*Flag_globalSuperTightHalo2016Filter)'
    if year == '2017':
        flags = flags + '*(Flag_ecalBadCalibFilterV2)'
    elif year == '2018':
        flags = flags + '*(Flag_ecalBadCalibFilter)'
    flagsmc = flags

    #ptreweighting = '((TMath::Sqrt( TMath::Exp(0.0615-0.0005*topGenPt) * TMath::Exp(0.0615-0.0005*antitopGenPt))'

    if year == '2016':
        leptonReco = '(((abs(Lepton_pdgId[0])==13)+(Lepton_RecoSF[0]*(abs(Lepton_pdgId[0])==11)))*((abs(Lepton_pdgId[1])==13)+(Lepton_RecoSF[1]*(abs(Lepton_pdgId[1])==11))))'
    else:
        leptonReco = 'Lepton_RecoSF[0]*Lepton_RecoSF[1]' 

    if isLatino == 0:
        leptonIDIso = '(Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[0]*Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[1]*Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[0]*Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[1])'
        if ismc == 0:
            leptonIDIso = leptonIDIso + '*zerohitLeptonWeight'
    else:
        if year == "2016":
            leptonIDIso = 'LepSF2l__ele_mva_90p_Iso2016__mu_cut_Tight80x'
        else:
            leptonIDIso = 'LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW'

    ##########################List of weights that have to be applied to data#############################
    flagsdata = flags + '*(Flag_eeBadScFilter)'
    
    #vetoHEMeleData = '((run<319077 || ((Sum$(Electron_pt>30. && Electron_eta>-3.0 && Electron_eta<-1.4 && Electron_phi>-1.57 && Electron_phi<-0.87)==0) && (Sum$(Jet_pt>30. && Jet_eta>-3.2 && Jet_eta<-1.2 && Jet_phi>-1.77 && Jet_phi<-0.67)==0)))*1.)'
    vetoHEMeleData = '1'

    weight = ''
    if ismc == 0:
        weight = flagsdata + '*' + vetoHEMeleData
    else:
        weight = mcweights + '*' + leptonGen + '*' + flagsmc + '*' + leptonReco + '*' + leptonIDIso 
        if year =='2016' or year == '2017':
            weight = weight + '*' + 'PrefireWeight'
        if year == '2017':
            weight = weight + '*' + vetoEENoise
        if year == '2018':
            weight = weight + '*' + vetoHEMele


    ####################################### Selection cuts ###############################################
    leptonAcc = '(Lepton_pt[0] > 25 && Lepton_pt[1] > 20 && abs(Lepton_eta[0]) < 2.4 && abs(Lepton_eta[1]) < 2.4) * MET_pt > 100.' #TOCHECK
    if isLatino == 0:
        ee = leptonAcc + '&& ((Lepton_pdgId[0]*Lepton_pdgId[1] == -121) && (Lepton_isTightElectron_cutBasedMediumPOG[0] > 0 &&  Lepton_isTightElectron_cutBasedMediumPOG[1] > 0))'
        mm = leptonAcc + '&& ((Lepton_pdgId[0]*Lepton_pdgId[1] == -169) && (Lepton_isTightMuon_mediumRelIsoTight[0] > 0 &&  Lepton_isTightMuon_mediumRelIsoTight[1] > 0))'
        em = leptonAcc + '&& ((Lepton_pdgId[0]*Lepton_pdgId[1] == -143) && ((abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_cutBasedMediumPOG[0] > 0 && abs(Lepton_pdgId[1]) == 13 && Lepton_isTightMuon_mediumRelIsoTight[1] > 0) || (abs(Lepton_pdgId[0]) == 13 && Lepton_isTightMuon_mediumRelIsoTight[0] > 0 && abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_cutBasedMediumPOG[1] > 0)))'
    else:
        if year == "2016":
            ee = leptonAcc + '&& ((Lepton_pdgId[0]*Lepton_pdgId[1] == -121) && (Lepton_isTightElectron_mva_90p_Iso2016[0] > 0 &&  Lepton_isTightElectron_mva_90p_Iso2016[1] > 0))'
            mm = leptonAcc + '&& ((Lepton_pdgId[0]*Lepton_pdgId[1] == -169) && (Lepton_isTightMuon_cut_Tight80x[0] > 0 &&  Lepton_isTightMuon_cut_Tight80x[1] > 0))'
            em = leptonAcc + '&& ((Lepton_pdgId[0]*Lepton_pdgId[1] == -143) && ((abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_mva_90p_Iso2016[0] > 0 && abs(Lepton_pdgId[1]) == 13 && Lepton_isTightMuon_cut_Tight80x[1] > 0) || (abs(Lepton_pdgId[0]) == 13 && Lepton_isTightMuon_cut_Tight80x[0] > 0 && abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_mva_90p_Iso2016[1] > 0)))'
        else:
            ee = leptonAcc + '&& ((Lepton_pdgId[0]*Lepton_pdgId[1] == -121) && (Lepton_isTightElectron_mvaFall17V1Iso_WP90[0] > 0 &&  Lepton_isTightElectron_mvaFall17V1Iso_WP90[1] > 0))'
            mm = leptonAcc + '&& ((Lepton_pdgId[0]*Lepton_pdgId[1] == -169) && (Lepton_isTightMuon_cut_Tight_HWWW[0] > 0 &&  Lepton_isTightMuon_cut_Tight_HWWW[1] > 0))'
            em = leptonAcc + '&& ((Lepton_pdgId[0]*Lepton_pdgId[1] == -143) && ((abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_mvaFall17V1Iso_WP90[0] > 0 && abs(Lepton_pdgId[1]) == 13 && Lepton_isTightMuon_cut_Tight_HWWW[1] > 0) || (abs(Lepton_pdgId[0]) == 13 && Lepton_isTightMuon_cut_Tight_HWWW[0] > 0 && abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_mvaFall17V1Iso_WP90[1] > 0)))'


    ###################################### Trigger cuts #################################################
    ##### MET triggers
    #trig_MET_2016 = '(HLT_PFMET90_PFMHT90_IDTight > 0 || HLT_PFMET100_PFMHT100_IDTight > 0 || HLT_PFMET110_PFMHT110_IDTight > 0 || HLT_PFMET120_PFMHT120_IDTight > 0)'
    trig_MET_2016 = '(HLT_PFMET300 > 0 || HLT_MET200 > 0 || HLT_PFHT300_PFMET110 > 0 || HLT_PFMET170_HBHECleaned > 0 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight > 0 || HLT_PFMET120_PFMHT120_IDTight > 0)'
    #trig_MET_2017 = '(HLT_PFMET120_PFMHT120_IDTight > 0 || HLT_PFMET110_PFMHT110_IDTight || HLT_PFMET130_PFMHT130_IDTight || HLT_PFMET140_PFMHT140_IDTight)'
    trig_MET_2017 = '( HLT_PFMETNoMu120_PFMHTNoMu120_IDTight > 0 || HLT_PFMET120_PFMHT120_IDTight > 0 || HLT_PFHT500_PFMET100_PFMHT100_IDTight > 0 || HLT_PFHT700_PFMET85_PFMHT85_IDTight > 0 || HLT_PFHT800_PFMET75_PFMHT75_IDTight > 0)'
    #trig_MET_2018 = '(HLT_PFMET120_PFMHT120_IDTight > 0 || HLT_PFMET110_PFMHT110_IDTight || HLT_PFMET130_PFMHT130_IDTight || HLT_PFMET140_PFMHT140_IDTight)'
    trig_MET_2018 = '(HLT_PFMET200_HBHECleaned > 0 || HLT_PFMET200_HBHE_BeamHaloCleaned > 0 || HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned > 0 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight > 0 || HLT_PFMET120_PFMHT120_IDTight > 0 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60 > 0 || HLT_PFMET120_PFMHT120_IDTight_PFHT60 > 0 || HLT_PFHT500_PFMET100_PFMHT100_IDTight > 0 || HLT_PFHT700_PFMET85_PFMHT85_IDTight > 0 || HLT_PFHT800_PFMET75_PFMHT75_IDTight > 0)'

    trig_MET = ''
    if year == '2016':
        trig_MET = trig_MET_2016
    if year == '2017':
        trig_MET = trig_MET_2017
    if year == '2018':
        trig_MET = trig_MET_2018

    ##### lepton triggers
    trig_mm = '(Trigger_dblMu > 0 || Trigger_sngMu > 0)'
    trig_ee = '(Trigger_dblEl > 0 || Trigger_sngEl > 0)'
    trig_em = '(Trigger_ElMu > 0 || Trigger_sngEl > 0 || Trigger_sngMu > 0)'


    ###################################### Final cuts #################################################
    general_cut = '1'
    cut_num_ee = general_cut + ' && ' + trig_MET + ' && ' + ee + ' && ' + trig_ee
    cut_den_ee = general_cut + ' && ' + trig_MET + ' && ' + ee
    cut_num_mm = general_cut + ' && ' + trig_MET + ' && ' + mm + ' && ' + trig_mm
    cut_den_mm = general_cut + ' && ' + trig_MET + ' && ' + mm
    cut_num_em = general_cut + ' && ' + trig_MET + ' && ' + em + ' && ' + trig_em
    cut_den_em = general_cut + ' && ' + trig_MET + ' && ' + em
 

    ###################################### Open file ##################################################
    #f = ROOT.TFile(options.filename)
    #ev = f.Get('Events')
    
    #if ismc:
    #Find all the MC files in the inputdir
    filesToConsider = []
    for (dirpath, dirnames, filenames) in walk(inputDir):
        for filename in filenames:
            if not ismc or ("TTTo2" in filename or "ST" in filename or "DYToLL" in filename):
                filesToConsider.append(ROOT.TFile(inputDir + filename))
    #else:
    #    filesToConsider = [ROOT.TFile(options.filename)]

    ####################################### Binning ###################################################
    #pt_bin = array('f', [20, 40, 60, 80, 120, 180, 240, 300])
    pt_bin = array('f', [25, 40, 60, 80, 100, 150, 500])

    suffix = ""
    if plots2D:
        h_ee_pt_num = ROOT.TH2F("h_ee_pt_num" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
        h_ee_pt_num.Sumw2()
        h_ee_pt_den = ROOT.TH2F("h_ee_pt_den" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
        h_ee_pt_den.Sumw2()
    
        h_mm_pt_num = ROOT.TH2F("h_mm_pt_num" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
        h_mm_pt_num.Sumw2()
        h_mm_pt_den = ROOT.TH2F("h_mm_pt_den" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
        h_mm_pt_den.Sumw2()
    
        h_em_pt_num = ROOT.TH2F("h_em_pt_num" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
        h_em_pt_num.Sumw2()
        h_em_pt_den = ROOT.TH2F("h_em_pt_den" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
        h_em_pt_den.Sumw2()
    else:
        h_ee_pt_num = ROOT.TH1F("h_ee_pt_num" + suffix, "", len(pt_bin)-1, pt_bin)
        h_ee_pt_num.Sumw2()
        h_ee_pt_den = ROOT.TH1F("h_ee_pt_den" + suffix, "", len(pt_bin)-1, pt_bin)
        h_ee_pt_den.Sumw2()
        
        h_mm_pt_num = ROOT.TH1F("h_mm_pt_num" + suffix, "", len(pt_bin)-1, pt_bin)
        h_mm_pt_num.Sumw2()
        h_mm_pt_den = ROOT.TH1F("h_mm_pt_den" + suffix, "", len(pt_bin)-1, pt_bin)
        h_mm_pt_den.Sumw2()
            
        h_em_pt_num = ROOT.TH1F("h_em_pt_num" + suffix, "", len(pt_bin)-1, pt_bin)
        h_em_pt_num.Sumw2()
        h_em_pt_den = ROOT.TH1F("h_em_pt_den" + suffix, "", len(pt_bin)-1, pt_bin)
        h_em_pt_den.Sumw2()
        

    ####################################### Histograms ################################################
    index = 0
    for i, fileToConsider in enumerate(filesToConsider):
        ev = fileToConsider.Get("Events")

        print("--> Reading file number " + str(i))
        
        index = index + 1
        #if index > 5:
        #    break

        suffix = str(index)
        if plots2D:
            h_ee_pt_file_num = ROOT.TH2F("h_ee_pt_file_num" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
            h_ee_pt_file_num.Sumw2()
            h_ee_pt_file_den = ROOT.TH2F("h_ee_pt_file_den" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
            h_ee_pt_file_den.Sumw2()
        
            h_mm_pt_file_num = ROOT.TH2F("h_mm_pt_file_num" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
            h_mm_pt_file_num.Sumw2()
            h_mm_pt_file_den = ROOT.TH2F("h_mm_pt_file_den" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
            h_mm_pt_file_den.Sumw2()

            h_em_pt_file_num = ROOT.TH2F("h_em_pt_file_num" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
            h_em_pt_file_num.Sumw2()
            h_em_pt_file_den = ROOT.TH2F("h_em_pt_file_den" + suffix, "", len(pt_bin)-1, pt_bin, len(pt_bin)-1, pt_bin)
            h_em_pt_file_den.Sumw2()
        else:
            h_ee_pt_file_num = ROOT.TH1F("h_ee_pt_file_num" + suffix, "", len(pt_bin)-1, pt_bin)
            h_ee_pt_file_num.Sumw2()
            h_ee_pt_file_den = ROOT.TH1F("h_ee_pt_file_den" + suffix, "", len(pt_bin)-1, pt_bin)
            h_ee_pt_file_den.Sumw2()
        
            h_mm_pt_file_num = ROOT.TH1F("h_mm_pt_file_num" + suffix, "", len(pt_bin)-1, pt_bin)
            h_mm_pt_file_num.Sumw2()
            h_mm_pt_file_den = ROOT.TH1F("h_mm_pt_file_den" + suffix, "", len(pt_bin)-1, pt_bin)
            h_mm_pt_file_den.Sumw2()

            h_em_pt_file_num = ROOT.TH1F("h_em_pt_file_num" + suffix, "", len(pt_bin)-1, pt_bin)
            h_em_pt_file_num.Sumw2()
            h_em_pt_file_den = ROOT.TH1F("h_em_pt_file_den" + suffix, "", len(pt_bin)-1, pt_bin)
            h_em_pt_file_den.Sumw2()


        ################################## Projecting histograms ##########################################
        if plots2D:
            #ev.Draw("Lepton_pt[0]:Lepton_pt[1]", cut_num_ee + '*' + weight)
            print(cut_num_ee + '*' + weight)
            try:
                ev.Project("h_ee_pt_file_num" + suffix, 'Lepton_pt[1]:Lepton_pt[0]', cut_num_ee + '*' + weight) 
                ev.Project("h_ee_pt_file_den" + suffix, 'Lepton_pt[1]:Lepton_pt[0]', cut_den_ee + '*' + weight) 
                ev.Project("h_mm_pt_file_num" + suffix, 'Lepton_pt[1]:Lepton_pt[0]', cut_num_mm + '*' + weight) 
                ev.Project("h_mm_pt_file_den" + suffix, 'Lepton_pt[1]:Lepton_pt[0]', cut_den_mm + '*' + weight) 
                ev.Project("h_em_pt_file_num" + suffix, 'Electron_pt[0]:Muon_pt[0]', cut_num_em + '*' + weight) #Take into account the difference in effienciency between electrons and muons
                ev.Project("h_em_pt_file_den" + suffix, 'Electron_pt[0]:Muon_pt[0]', cut_den_em + '*' + weight) 
            except Exception as e:
                print(e)
                continue
        else:
            try:
                ev.Project("h_ee_pt_file_num" + suffix, 'Lepton_pt[0]', cut_num_ee + '*' + weight) 
                ev.Project("h_ee_pt_file_den" + suffix, 'Lepton_pt[0]', cut_den_ee + '*' + weight) 
                ev.Project("h_mm_pt_file_num" + suffix, 'Lepton_pt[0]', cut_num_mm + '*' + weight) 
                ev.Project("h_mm_pt_file_den" + suffix, 'Lepton_pt[0]', cut_den_mm + '*' + weight) 
                ev.Project("h_em_pt_file_num" + suffix, 'Electron_pt[0]', cut_num_em + '*' + weight) 
                ev.Project("h_em_pt_file_den" + suffix, 'Electron_pt[0]', cut_den_em + '*' + weight) 
            except Exception as e:
                print(e)
                continue

            
        ################################## Making efficiencies ###########################################
        eff_ee_partial = ROOT.TEfficiency(h_ee_pt_file_num, h_ee_pt_file_den)
        eff_mm_partial = ROOT.TEfficiency(h_mm_pt_file_num, h_mm_pt_file_den)
        eff_em_partial = ROOT.TEfficiency(h_em_pt_file_num, h_em_pt_file_den)


        ################################## Add efficiencies ##########################################
        try:
            eff_ee.Add(eff_ee_partial)
            eff_mm.Add(eff_mm_partial)
            eff_em.Add(eff_em_partial)
        except NameError: #First pass in the loop
            eff_ee = eff_ee_partial
            eff_ee.SetLineColor(632)
            eff_ee.SetLineWidth(1)
            eff_ee.SetName("Efficiency_ee_pt_" + options.year + "_" + options.tag)
        
            eff_mm = eff_mm_partial #ROOT.TEfficiency(h_mm_pt_file_num, h_mm_pt_file_den)
            eff_mm.SetLineColor(634)
            eff_mm.SetLineWidth(1)
            eff_mm.SetName("Efficiency_mm_pt_" + options.year + "_" + options.tag)
    
            eff_em = eff_em_partial
            eff_em.SetLineColor(636)
            eff_em.SetLineWidth(1)
            eff_em.SetName("Efficiency_em_pt_" + options.year + "_" + options.tag)


        ################################## Add histograms ##########################################
        h_ee_pt_num.Add(h_ee_pt_file_num)
        h_ee_pt_den.Add(h_ee_pt_file_den)
        h_mm_pt_num.Add(h_mm_pt_file_num)
        h_mm_pt_den.Add(h_mm_pt_file_den)
        h_em_pt_num.Add(h_em_pt_file_num)
        h_em_pt_den.Add(h_em_pt_file_den)
        

    ########################################## DrAwing ###############################################
    if not plots2D:
        can = ROOT.TCanvas("eff", "")
        can.cd()

        eff_ee.SetTitle("Trigger efficiences (" + options.tag + ")")
        eff_ee.Draw()
        eff_mm.Draw("SAME")
        eff_em.Draw("SAME")
        
        ROOT.gPad.Update() 
        eff_ee.GetPaintedGraph().GetHistogram().SetMinimum(0)
        eff_mm.GetPaintedGraph().GetHistogram().SetMinimum(0)
        eff_em.GetPaintedGraph().GetHistogram().SetMinimum(0)
        eff_ee.GetPaintedGraph().GetHistogram().SetMaximum(1.2)
        eff_mm.GetPaintedGraph().GetHistogram().SetMaximum(1.2)
        eff_em.GetPaintedGraph().GetHistogram().SetMaximum(1.2)

        legend = ROOT.TLegend(0.70, 0.20, 0.90, 0.30)
        legend.SetBorderSize(0)
        legend.SetFillColor(0)
        legend.SetTextAlign(12)
        legend.SetTextFont(42)
        legend.SetTextSize(0.035)
        legend.AddEntry(eff_ee, "ee", "l")
        legend.AddEntry(eff_mm, "mm", "l")
        legend.AddEntry(eff_em, "em", "l")
        legend.Draw("SAME")

        print("ee numerator yields: " + str(h_ee_pt_num.Integral(-1, -1)))
        print("ee denominator yields: " + str(h_ee_pt_den.Integral(-1, -1)))
        print("em numerator yields: " + str(h_em_pt_num.Integral(-1, -1)))
        print("em denominator yields: " + str(h_em_pt_den.Integral(-1, -1)))
        print("mm numerator yields: " + str(h_mm_pt_num.Integral(-1, -1)))
        print("mm denominator yields: " + str(h_mm_pt_den.Integral(-1, -1)))

        can.SaveAs("Efficiency_pt_" + options.year + "_" + options.tag + ".png")
    else:
        h_eff = {}
        for channel in ["ee", "em", "mm"]:
            can = ROOT.TCanvas("eff_" + channel, "")
            can.cd()

            if channel == "ee":
                eff = eff_ee
            elif channel == "em":
                eff = eff_em
            else:
                eff = eff_mm
            eff.SetTitle("Trigger efficiency (" + channel + ", " + options.tag + ")")
            eff.Draw("COLZ,TEXT45,ERROR")

            ROOT.gPad.Update() 
            ROOT.gStyle.SetPaintTextFormat("4.2f")
            eff.GetPaintedHistogram().SetMinimum(0.8)
            #eff.GetPaintedHistogram().SetMaximum(1.02)
            
            paintedHist = eff.GetPaintedHistogram()
            for x in range(len(pt_bin)):
                for y in range(len(pt_bin)):
                    paintedHist.SetBinContent(x, y, eff.GetEfficiency(eff.GetPaintedHistogram().GetBin(x,y)))
                    paintedHist.SetBinError(x, y, max(eff.GetEfficiencyErrorLow(eff.GetPaintedHistogram().GetBin(x,y)), eff.GetEfficiencyErrorUp(eff.GetPaintedHistogram().GetBin(x,y))))
            h_eff[channel] = paintedHist

            for x in range(len(pt_bin)):
                for y in range(len(pt_bin)):
                    print(channel + " bin(" + str(x) + ", " + str(y) + ") : " + str(eff.GetEfficiency(eff.GetPaintedHistogram().GetBin(x,y))) + " - " + str(eff.GetEfficiencyErrorLow(eff.GetPaintedHistogram().GetBin(x,y))) + " + " + str(eff.GetEfficiencyErrorUp(eff.GetPaintedHistogram().GetBin(x,y))))

            print("ee numerator yields: " + str(h_ee_pt_num.Integral(-1, -1, -1, -1)))
            print("ee denominator yields: " + str(h_ee_pt_den.Integral(-1, -1, -1, -1)))
            print("ee numerator yields last bin: " + str(h_ee_pt_num.Integral(len(pt_bin)-1, len(pt_bin)-1, len(pt_bin)-1, len(pt_bin)-1)))
            print("ee denominator yields last bin: " + str(h_ee_pt_den.Integral(len(pt_bin)-1, len(pt_bin)-1, len(pt_bin)-1, len(pt_bin)-1)))

            can.SaveAs("Efficiency_pt_" + channel + "_" + options.year + "_" + options.tag + ".png")

    suffix = ""
    if isLatino == 1:
        suffix = "_latino"

    eff_ee.SaveAs("Efficiency_pt_ee_" + options.year + "_" + options.tag + suffix + ".root")
    eff_mm.SaveAs("Efficiency_pt_mm_" + options.year + "_" + options.tag + suffix + ".root")
    eff_em.SaveAs("Efficiency_pt_em_" + options.year + "_" + options.tag + suffix + ".root")

    eeFile = ROOT.TFile.Open("Efficiency_pt_ee_" + options.year + "_" + options.tag + suffix + ".root", "UPDATE")
    if plots2D:
        h_eff["ee"].Write()
    h_ee_pt_num.Write()
    h_ee_pt_den.Write()
    eeFile.Close()

    mmFile = ROOT.TFile.Open("Efficiency_pt_mm_" + options.year + "_" + options.tag + suffix + ".root", "UPDATE")
    if plots2D:
        h_eff["mm"].Write()
    h_mm_pt_num.Write()
    h_mm_pt_den.Write()
    mmFile.Close()

    emFile = ROOT.TFile.Open("Efficiency_pt_em_" + options.year + "_" + options.tag + suffix + ".root", "UPDATE")
    if plots2D:
        h_eff["em"].Write()
    h_em_pt_num.Write()
    h_em_pt_den.Write()
    emFile.Close()
