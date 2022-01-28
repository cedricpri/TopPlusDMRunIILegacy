
#

massZ = '91.1876'
vetoZ = 'fabs(mll'+ctrltag+'-'+massZ+')>15.'
Zcut  = 'fabs(mll'+ctrltag+'-'+massZ+')<ZCUT'
SF    = LL+' && '+vetoZ  

#cuts = {}

if opt.tag=='btagefficiencies':

    jetKinSelection = 'CleanJet_pt>=20. && abs(CleanJet_eta)<'+btagEtaMax
    jetTagSelection = 'Jet_'+btagAlgo+'[CleanJet_jetIdx]>='+btagCut
    cuts['taggablejets_b'] = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])==5'
    cuts['taggablejets_c'] = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])==4'
    cuts['taggablejets_l'] = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])<4 '
    cuts[btagAlgo+'_'+btagWP+'_b']  = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])==5 && '+jetTagSelection
    cuts[btagAlgo+'_'+btagWP+'_c']  = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])==4 && '+jetTagSelection
    cuts[btagAlgo+'_'+btagWP+'_l']  = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])<4  && '+jetTagSelection

#if 'Test' in opt.tag:
#
#    cuts['TwoLep_em'] = OC+' && '+DF+' && ptmiss>=80'
#    cuts['TwoLep_em_Tag'] = '(' + OC+' && '+DF+' && ptmiss>=80)*'+btagWeight1tag
#    cuts['TwoLep_em_Veto'] = '(' + OC+' && '+DF+' && ptmiss>=80)*'+btagWeight0tag

if 'TwoLeptons' in opt.tag:

    cuts['TwoLep_em'] = OC+' && '+DF
    cuts['TwoLep_ee'] = OC+' && '+EE 
    cuts['TwoLep_mm'] = OC+' && '+MM
    
if 'PV35' in opt.tag:

    cuts['TwoLep_em_PVm35'] = OC+' && '+DF+' && PV_npvs<35'
    cuts['TwoLep_em_PVp35'] = OC+' && '+DF+' && PV_npvs>=35'
    cuts['TwoLep_sf_PVm35'] = OC+' && '+SF+' && PV_npvs<35'
    cuts['TwoLep_sf_PVp35'] = OC+' && '+SF+' && PV_npvs>=35'

if 'Preselection' in opt.tag:

    cuts['TwoLep_em_nometcut'] = OC+' && '+DF
    cuts['TwoLep_ee_nometcut'] = OC+' && '+EE+' && '+vetoZ
    cuts['TwoLep_mm_nometcut'] = OC+' && '+MM+' && '+vetoZ

    cuts['TwoLep_em'] = OC+' && '+DF+' && ptmiss>=80'
    cuts['TwoLep_ee'] = OC+' && '+EE+' && '+vetoZ+' && ptmiss>=80'
    cuts['TwoLep_mm'] = OC+' && '+MM+' && '+vetoZ+' && ptmiss>=80'

    if 'Data' in opt.sigset:
        cuts['TwoLep_em_Veto'] = OC+' && '+DF             +' && '+bTagVeto
        cuts['TwoLep_ee_Veto'] = OC+' && '+EE+' && '+vetoZ+' && '+bTagVeto
        cuts['TwoLep_mm_Veto'] = OC+' && '+MM+' && '+vetoZ+' && '+bTagVeto

        cuts['TwoLep_em_Tag']  = OC+' && '+DF             +' && '+bTagPass
        cuts['TwoLep_ee_Tag']  = OC+' && '+EE+' && '+vetoZ+' && '+bTagPass
        cuts['TwoLep_mm_Tag']  = OC+' && '+MM+' && '+vetoZ+' && '+bTagPass

    else: #if 'Backgrounds' in opt.sigset:
        cuts['TwoLep_em_Veto'] = '('+OC+' && '+DF             +')*'+btagWeight0tag
        cuts['TwoLep_ee_Veto'] = '('+OC+' && '+EE+' && '+vetoZ+')*'+btagWeight0tag
        cuts['TwoLep_mm_Veto'] = '('+OC+' && '+MM+' && '+vetoZ+')*'+btagWeight0tag

        cuts['TwoLep_em_Tag']  = '('+OC+' && '+DF             +')*'+btagWeight1tag
        cuts['TwoLep_ee_Tag']  = '('+OC+' && '+EE+' && '+vetoZ+')*'+btagWeight1tag
        cuts['TwoLep_mm_Tag']  = '('+OC+' && '+MM+' && '+vetoZ+')*'+btagWeight1tag

if 'METFix' in opt.tag:
  
    if 'Data' in opt.sigset:
        cuts['METFixEE_low_em_Veto'] = OC+' && '+DF             +' && '+bTagVeto
        cuts['METFixEE_low_ee_Veto'] = OC+' && '+EE+' && '+vetoZ+' && '+bTagVeto
        cuts['METFixEE_low_mm_Veto'] = OC+' && '+MM+' && '+vetoZ+' && '+bTagVeto
        cuts['METFixEE_low_sf_Veto'] = OC+' && '+SF+' && '+vetoZ+' && '+bTagVeto
    
        cuts['METFixEE_low_em_Tag']  = OC+' && '+DF             +' && '+bTagPass
        cuts['METFixEE_low_ee_Tag']  = OC+' && '+EE+' && '+vetoZ+' && '+bTagPass
        cuts['METFixEE_low_mm_Tag']  = OC+' && '+MM+' && '+vetoZ+' && '+bTagPass
        cuts['METFixEE_low_sf_Tag']  = OC+' && '+SF+' && '+vetoZ+' && '+bTagPass

        cuts['METFixEE_high_em_Veto'] = OC+' && '+DF             +' && ptmiss>=100 && ptmiss<140 &&'+bTagVeto
        cuts['METFixEE_high_ee_Veto'] = OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+bTagVeto
        cuts['METFixEE_high_mm_Veto'] = OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+bTagVeto
        cuts['METFixEE_high_sf_Veto'] = OC+' && '+SF+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+bTagVeto
    
        cuts['METFixEE_high_em_Tag']  = OC+' && '+DF             +' && ptmiss>=100 && ptmiss<140 && '+bTagPass
        cuts['METFixEE_high_ee_Tag']  = OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+bTagPass
        cuts['METFixEE_high_mm_Tag']  = OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+bTagPass
        cuts['METFixEE_high_sf_Tag']  = OC+' && '+SF+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+bTagPass
    else:
        cuts['METFixEE_low_em_Veto'] = '('+OC+' && '+DF             +')*'+btagWeight0tag
        cuts['METFixEE_low_ee_Veto'] = '('+OC+' && '+EE+' && '+vetoZ+')*'+btagWeight0tag
        cuts['METFixEE_low_mm_Veto'] = '('+OC+' && '+MM+' && '+vetoZ+')*'+btagWeight0tag
        cuts['METFixEE_low_sf_Veto'] = '('+OC+' && '+SF+' && '+vetoZ+')*'+btagWeight0tag

        cuts['METFixEE_low_em_Tag']  = '('+OC+' && '+DF             +')*'+btagWeight1tag
        cuts['METFixEE_low_ee_Tag']  = '('+OC+' && '+EE+' && '+vetoZ+')*'+btagWeight1tag
        cuts['METFixEE_low_mm_Tag']  = '('+OC+' && '+MM+' && '+vetoZ+')*'+btagWeight1tag
        cuts['METFixEE_low_sf_Tag']  = '('+OC+' && '+SF+' && '+vetoZ+')*'+btagWeight1tag

        cuts['METFixEE_high_em_Veto'] = '('+OC+' && '+DF             +' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['METFixEE_high_ee_Veto'] = '('+OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['METFixEE_high_mm_Veto'] = '('+OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['METFixEE_high_sf_Veto'] = '('+OC+' && '+SF+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag

        cuts['METFixEE_high_em_Tag']  = '('+OC+' && '+DF             +' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['METFixEE_high_ee_Tag']  = '('+OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['METFixEE_high_mm_Tag']  = '('+OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['METFixEE_high_sf_Tag']  = '('+OC+' && '+SF+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
    
if 'VetoNoiseEE' in opt.tag:

    channelCut = OC 
    if 'Zveto' in opt.tag:
        channelCut += ' && ('+DF+' || '+SF+')'
 
    EENoiseVeto0 = '(Sum$(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    EENoiseVeto1 = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    EENoiseVeto2 = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    
    ptm = ' && ptmiss > 100. && ptmiss<=140'
    if 'MET' in opt.tag: ptm = ' && MET_pt > 100 && MET_pt < 140 ' # currently unused
      
    if 'Data' in opt.sigset:
        cuts['Veto0_Tag']             = channelCut+' && '+EENoiseVeto0+' && '+bTagPass
        cuts['Veto0_Tag_highptmiss']  = channelCut+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<140. && '+bTagPass
        cuts['Veto1_Tag']             = channelCut+' && '+EENoiseVeto1+' && '+bTagPass
        cuts['Veto1_Tag_highptmiss']  = channelCut+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<140. && '+bTagPass
        cuts['Veto2_Tag']             = channelCut+' && '+EENoiseVeto2+' && '+bTagPass
        cuts['Veto2_Tag_highptmiss']  = channelCut+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<140. && '+bTagPass
        cuts['Veto0_Veto']            = channelCut+' && '+EENoiseVeto0+' && '+bTagVeto
        cuts['Veto0_Veto_highptmiss'] = channelCut+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<140. && '+bTagVeto
        cuts['Veto1_Veto']            = channelCut+' && '+EENoiseVeto1+' && '+bTagVeto
        cuts['Veto1_Veto_highptmiss'] = channelCut+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<140. && '+bTagVeto
        cuts['Veto2_Veto']            = channelCut+' && '+EENoiseVeto2+' && '+bTagVeto
        cuts['Veto2_Veto_highptmiss'] = channelCut+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<140. && '+bTagVeto
        if 'HTF' in opt.tag:
            cuts['Veto0_Tag_HTF']             = OC+' && '+EENoiseVeto0+' && '+ HTForward + '>=60. && '+bTagPass
            cuts['Veto0_Tag_highptmiss_HTF']  = OC+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<=140. && '+ HTForward + '>=60. && '+bTagPass
            cuts['Veto1_Tag_HTF']             = OC+' && '+EENoiseVeto1+' && '+ HTForward + '>=60. && '+bTagPass
            cuts['Veto1_Tag_highptmiss_HTF']  = OC+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<=140. && '+ HTForward + '>=60. && '+bTagPass
            cuts['Veto2_Tag_HTF']             = OC+' && '+EENoiseVeto2+' && '+ HTForward + '>=60. && '+bTagPass
            cuts['Veto2_Tag_highptmiss_HTF']  = OC+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<=140. && '+ HTForward + '>=60. && '+bTagPass
            cuts['Veto0_Veto_HTF']            = OC+' && '+EENoiseVeto0+' && '+ HTForward + '>=60. && '+bTagVeto
            cuts['Veto0_Veto_highptmiss_HTF'] = OC+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<=140. && '+ HTForward + '>=60. && '+bTagVeto
            cuts['Veto1_Veto_HTF']            = OC+' && '+EENoiseVeto1+' && '+ HTForward + '>=60. && '+bTagVeto
            cuts['Veto1_Veto_highptmiss_HTF'] = OC+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<=140. && '+ HTForward + '>=60. && '+bTagVeto
            cuts['Veto2_Veto_HTF']            = OC+' && '+EENoiseVeto2+' && '+ HTForward + '>=60. && '+bTagVeto
            cuts['Veto2_Veto_highptmiss_HTF'] = OC+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<=140. && '+ HTForward + '>=60. && '+bTagVeto
        
    else: #if 'Backgrounds' in opt.sigset:
        cuts['Veto0_Tag']             = '('+channelCut+' && '+EENoiseVeto0+')*'+btagWeight1tag
        cuts['Veto0_Tag_highptmiss']  = '('+channelCut+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<140.)*'+btagWeight1tag
        cuts['Veto1_Tag']             = '('+channelCut+' && '+EENoiseVeto1+')*'+btagWeight1tag
        cuts['Veto1_Tag_highptmiss']  = '('+channelCut+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<140.)*'+btagWeight1tag
        cuts['Veto2_Tag']             = '('+channelCut+' && '+EENoiseVeto2+')*'+btagWeight1tag
        cuts['Veto2_Tag_highptmiss']  = '('+channelCut+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<140.)*'+btagWeight1tag
        cuts['Veto0_Veto']            = '('+channelCut+' && '+EENoiseVeto0+')*'+btagWeight0tag
        cuts['Veto0_Veto_highptmiss'] = '('+channelCut+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<140.)*'+btagWeight0tag
        cuts['Veto1_Veto']            = '('+channelCut+' && '+EENoiseVeto1+')*'+btagWeight0tag
        cuts['Veto1_Veto_highptmiss'] = '('+channelCut+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<140.)*'+btagWeight0tag
        cuts['Veto2_Veto']            = '('+channelCut+' && '+EENoiseVeto2+')*'+btagWeight0tag
        cuts['Veto2_Veto_highptmiss'] = '('+channelCut+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<140.)*'+btagWeight0tag
        if 'HTF' in opt.tag:
            cuts['Veto0_Tag_HTF']             = '('+OC+' && '+EENoiseVeto0+' && ' + HTForward + '>=60.'+')*'+btagWeight1tag
            cuts['Veto0_Tag_highptmiss_HTF']  = '('+OC+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')*'+btagWeight1tag
            cuts['Veto1_Tag_HTF']             = '('+OC+' && '+EENoiseVeto1+' && ' + HTForward + '>=60.' +')*'+btagWeight1tag
            cuts['Veto1_Tag_highptmiss_HTF']  = '('+OC+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')*'+btagWeight1tag
            cuts['Veto2_Tag_HTF']             = '('+OC+' && '+EENoiseVeto2+' && ' + HTForward + '>=60.'+')*'+btagWeight1tag
            cuts['Veto2_Tag_highptmiss_HTF']  = '('+OC+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')*'+btagWeight1tag
            cuts['Veto0_Veto_HTF']            = '('+OC+' && '+EENoiseVeto0+' && ' + HTForward + '>=60.'+')*'+btagWeight0tag
            cuts['Veto0_Veto_highptmiss_HTF'] = '('+OC+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')*'+btagWeight0tag
            cuts['Veto1_Veto_HTF']            = '('+OC+' && '+EENoiseVeto1+' && ' + HTForward + '>=60.'+')*'+btagWeight0tag
            cuts['Veto1_Veto_highptmiss_HTF'] = '('+OC+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')*'+btagWeight0tag
            cuts['Veto2_Veto_HTF']            = '('+OC+' && '+EENoiseVeto2+' && ' + HTForward + '>=60.'+')*'+btagWeight0tag
            cuts['Veto2_Veto_highptmiss_HTF'] = '('+OC+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')*'+btagWeight0tag

if 'DYchecks' in opt.tag:
    if 'nojets' in opt.tag:
        print "nojets"
        cuts['lowMll_sf_nojetcut']  = OC + ' && ' + LL + ' && PuppiMET_pt> 50' 
        cuts['lowMll_ee_nojetcut']  = OC + ' && ' + EE + ' && PuppiMET_pt> 50 '  
        cuts['lowMll_mm_nojetcut']  = OC + ' && ' + MM + ' && PuppiMET_pt> 50 '   
        cuts['highMll_sf_nojetcut'] = OC + ' && ' + LL + ' && PuppiMET_pt> 50 && mll>=76 && mll<106'
        cuts['highMll_ee_nojetcut'] = OC + ' && ' + EE + ' && PuppiMET_pt> 50 && mll>=76 && mll<106'
        cuts['highMll_mm_nojetcut'] = OC + ' && ' + MM + ' && PuppiMET_pt> 50 && mll>=76 && mll<106' 
        cuts['lowMll_sf_noMETcut_nojetcut']  = OC + ' && ' + LL   
        cuts['lowMll_ee_noMETcut_nojetcut']  = OC + ' && ' + EE   
        cuts['lowMll_mm_noMETcut_nojetcut']  = OC + ' && ' + MM    
        cuts['highMll_sf_noMETcut_nojetcut'] = OC + ' && ' + LL + ' && mll>=76 && mll<106'
        cuts['highMll_ee_noMETcut_nojetcut'] = OC + ' && ' + EE + ' && mll>=76 && mll<106' 
        cuts['highMll_mm_noMETcut_nojetcut'] = OC + ' && ' + MM + ' && mll>=76 && mll<106' 

    elif 'Data' in opt.sigset:
        print "DO DATA"
        cuts['lowMll_sf']  = OC + ' && ' + LL + ' && Alt$(CleanJet_pt[1], 0)>=30. && '+ bTagPass
        cuts['lowMll_ee']  = OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt> 50 && '+ bTagPass
        cuts['lowMll_mm']  = OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt> 50 &&  '+ bTagPass
        cuts['highMll_sf'] = OC + ' && ' + LL + ' && Alt$(CleanJet_pt[1],0)>=30. && mll>=76 && mll<106 && ' + bTagPass
        cuts['highMll_ee'] = OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt> 50 &&  mll>=76 && mll<106 && ' + bTagPass
        cuts['highMll_mm'] = OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30. &&  PuppiMET_pt> 50 && mll>=76 && mll<106 && ' + bTagPass
        cuts['lowMll_ee_noMETcut']  = OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30. && '+ bTagPass
        cuts['lowMll_mm_noMETcut']  = OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30. &&  '+ bTagPass
        cuts['highMll_ee_noMETcut'] = OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30. &&  mll>=76 && mll<106 && ' + bTagPass
        cuts['highMll_mm_noMETcut'] = OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30. &&  mll>=76 && mll<106 && ' + bTagPass

    else: #if 'Backgrounds' in opt.sigset:
        cuts['lowMll_sf']  = '(' + OC + ' && ' + LL + ' && Alt$(CleanJet_pt[1],0)>=30.)*'+ btagWeight1tag
        cuts['lowMll_ee']  = '(' + OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt> 50)*'+ btagWeight1tag
        cuts['lowMll_mm']  = '(' + OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt> 50)*'+ btagWeight1tag
        cuts['highMll_sf'] = '(' + OC + ' && ' + LL + ' && Alt$(CleanJet_pt[1],0)>=30. && mll>=76 && mll<106)*' + btagWeight1tag
        cuts['highMll_ee'] = '(' + OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt> 50 &&  mll>=76 && mll<106)*' + btagWeight1tag
        cuts['highMll_mm'] = '(' + OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30. &&  PuppiMET_pt> 50 && mll>=76 && mll<106)*' + btagWeight1tag
        cuts['lowMll_ee_noMETcut']  = '(' + OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30.)*'+ btagWeight1tag
        cuts['lowMll_mm_noMETcut']  = '(' + OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30.)*'+ btagWeight1tag
        cuts['highMll_ee_noMETcut'] = '(' + OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30. &&  mll>=76 && mll<106)*' + btagWeight1tag
        cuts['highMll_mm_noMETcut'] = '(' + OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30. &&  mll>=76 && mll<106)*' + btagWeight1tag
        
if 'TopControlRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['Top_em'] = '(' + OC+' && '+DF+' && ptmiss>=20) && '+bTagPass 
        cuts['Top_ee'] = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=50) && '+bTagPass 
        cuts['Top_mm'] = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=50) && '+bTagPass 
        cuts['Top_cr'] = '(' + OC+' && (('+DF+') || ('+SF+'))  && ptmiss>=50  && CleanJet_pt[1]>=30.) && '+bTagPass 
        cuts['Top_hm'] = '(' + OC+' && (('+DF+') || ('+SF+'))  && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25) && '+bTagPass 
        
    else: #if 'Backgrounds' in opt.sigset:
        cuts['Top_em'] = '(' + OC+' && '+DF+' && ptmiss>=20)*'+btagWeight1tag
        cuts['Top_ee'] = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=50)*'+btagWeight1tag
        cuts['Top_mm'] = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=50)*'+btagWeight1tag
        cuts['Top_cr'] = '(' + OC+' && (('+DF+') || ('+SF+'))  && ptmiss>=50  && CleanJet_pt[1]>=30.)*'+btagWeight1tag
        cuts['Top_hm'] = '(' + OC+' && (('+DF+') || ('+SF+'))  && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25)*'+btagWeight1tag

if 'HMControlRegion' in opt.tag:

    if 'Data' in opt.sigset: 
        cuts['Top_em'] = '(' + OC+' && '+DF+' && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25) && '+bTagPass 
        cuts['Top_sf'] = '(' + OC+' && '+SF+' && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25) && '+bTagPass 
        cuts['Top_hm'] = '(' + OC+' && (('+DF+') || ('+SF+'))  && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25) && '+bTagPass 
        
    else: #if 'Backgrounds' in opt.sigset:
        cuts['Top_em'] = '(' + OC+' && '+DF+' && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25)*'+btagWeight1tag
        cuts['Top_sf'] = '(' + OC+' && '+SF+' && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25)*'+btagWeight1tag
        cuts['Top_hm'] = '(' + OC+' && (('+DF+') || ('+SF+'))  && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25)*'+btagWeight1tag

if 'WWControlRegion' in opt.tag:

    cuts['WW_metcut'] = '(' + OC+' && '+DF+' && ptmiss>=70 && nCleanJet==0)'
    cuts['WW_nometcut'] = '(' + OC+' && '+DF+' && nCleanJet==0)'

if 'DYControlRegion' in opt.tag:

    DY = OC+' && '+LL+' && '+Zcut.replace('ZCUT',  '15.')

    if 'Data' in opt.sigset:
        cuts['DY_ee']     = '(' + DY+' && '+EE+') && '+bTagVeto
        cuts['DY_mm']     = '(' + DY+' && '+MM+') && '+bTagVeto
        cuts['DY_ee_jet'] = '(' + DY+' && '+EE+') && Alt$(CleanJet_pt[1],0)>=30. && '+bTagVeto
        cuts['DY_mm_jet'] = '(' + DY+' && '+MM+') && Alt$(CleanJet_pt[1],0)>=30. && '+bTagVeto

    else: #if 'Backgrounds' in opt.sigset:
        cuts['DY_ee']     = '(' + DY+' && '+EE+')*'+btagWeight0tag
        cuts['DY_mm']     = '(' + DY+' && '+MM+')*'+btagWeight0tag
        cuts['DY_ee_jet'] = '(' + DY+' && '+EE+' && Alt$(CleanJet_pt[1],0)>=30.)*'+btagWeight0tag
        cuts['DY_mm_jet'] = '(' + DY+' && '+MM+' && Alt$(CleanJet_pt[1],0)>=30.)*'+btagWeight0tag

if 'DYDarkMatterControlRegion' in opt.tag:

    DY = OC+' && '+LL+' && '+Zcut.replace('ZCUT',  '15.')

    cuts['DY_ee_puppi'] = '(' + DY+' && '+EE+') && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt>=50.'
    cuts['DY_mm_puppi'] = '(' + DY+' && '+MM+') && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt>=50.'
    cuts['DY_ee_pfmet'] = '(' + DY+' && '+EE+') && Alt$(CleanJet_pt[1],0)>=30. && ptmiss>=50.'
    cuts['DY_mm_pfmet'] = '(' + DY+' && '+MM+') && Alt$(CleanJet_pt[1],0)>=30. && ptmiss>=50.'

if 'HighPtMissControlRegion' in opt.tag or 'HighPtMissValidationRegion' in opt.tag:
    
    if 'Data' in opt.sigset:
        cuts['VR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+bTagPass
        cuts['VR1_Veto_em']  = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+bTagVeto
        cuts['VR1_Tag_sf']   = OC+' && '+SF+' && ptmiss>=100 && ptmiss<140 && '+bTagPass
        cuts['VR1_Veto_sf']  = OC+' && '+SF+' && ptmiss>=100 && ptmiss<140 && '+bTagVeto

    else:
        cuts['VR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['VR1_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['VR1_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['VR1_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag

if 'LatinoControlRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['Top_em'] = OC+' && '+DF+' && ptmiss>=20 && mll<76 && '          +pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40 && '+bTagPass
        cuts['WW_em']  = OC+' && '+DF+' && ptmiss>=20 && mll>76 && '          +pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40 && '+bTagVeto
        cuts['Top_sf'] = OC+' && '+SF+' && ptmiss>=50 && mll>25 && mll<76 && '+pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40 && '+bTagPass
        cuts['DY_sf']  = OC+' && '+LL+' && ptmiss>=50 && '+Zcut.replace('ZCUT','15')+'&& '+pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40 && '+bTagVeto

    else:
        cuts['Top_em'] = '('+OC+' && '+DF+' && ptmiss>=20 && mll<76 && '          +pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40)*'+btagWeight1tag
        cuts['WW_em']  = '('+OC+' && '+DF+' && ptmiss>=20 && mll>76 && '          +pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40)*'+btagWeight0tag
        cuts['Top_sf'] = '('+OC+' && '+SF+' && ptmiss>=50 && mll>25 && mll<76 && '+pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40)*'+btagWeight1tag
        cuts['DY_sf']  = '('+OC+' && '+LL+' && ptmiss>=50 && '+Zcut.replace('ZCUT','15')+'&& '+pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40)*'+btagWeight0tag

if 'HighPtMissOptimisationRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['VR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=100 && '+bTagPass
        cuts['VR1_Veto_em']  = OC+' && '+DF+' && ptmiss>=100 && '+bTagVeto
        cuts['VR1_Tag_sf']   = OC+' && '+SF+' && ptmiss>=100 && '+bTagPass
        cuts['VR1_Veto_sf']  = OC+' && '+SF+' && ptmiss>=100 && '+bTagVeto

    else:
        cuts['VR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=100)*'+btagWeight1tag
        cuts['VR1_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=100)*'+btagWeight0tag
        cuts['VR1_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=100)*'+btagWeight1tag
        cuts['VR1_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=100)*'+btagWeight0tag

if 'TopValidationRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['VR1_Tag_em']      = OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && '+bTagPass
        cuts['VR1_Tag_sf']      = OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140 && '+bTagPass
        cuts['VR1_Tag_mm']      = OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+bTagPass
        cuts['VR1_Tag_ee']      = OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+bTagPass
        cuts['VR1_Tag_em_jets'] = OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30. && '+bTagPass
        cuts['VR1_Tag_sf_jets'] = OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30. && '+bTagPass
        cuts['VR1_Tag_mm_jets'] = OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30. && '+bTagPass
        cuts['VR1_Tag_ee_jets'] = OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30. && '+bTagPass
        if 'More' in opt.tag:
            cuts['VR1_Tag_em_mt2']  = OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && mt2ll>100.          && '+bTagPass
            cuts['VR1_Tag_mm_mt2']  = OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.          && '+bTagPass
            cuts['VR1_Tag_ee_mt2']  = OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.          && '+bTagPass
        cuts['VR1_Tag_jets']    = OC+' && ('+SF+' || '+DF+')  && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30. && '+bTagPass

    else:
        cuts['VR1_Tag_em']        = '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['VR1_Tag_sf']        = '(' + OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['VR1_Tag_mm']        = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['VR1_Tag_ee']        = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['VR1_Tag_em_jets']   = '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)*'+btagWeight1tag
        cuts['VR1_Tag_sf_jets']   = '(' + OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)*'+btagWeight1tag
        cuts['VR1_Tag_mm_jets']   = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)*'+btagWeight1tag
        cuts['VR1_Tag_ee_jets']   = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)*'+btagWeight1tag
        if 'More' in opt.tag:
            cuts['VR1_Tag_em_mt2']    = '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && mt2ll>100.         )*'+btagWeight1tag
            cuts['VR1_Tag_mm_mt2']    = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.         )*'+btagWeight1tag
            cuts['VR1_Tag_ee_mt2']    = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.         )*'+btagWeight1tag
        cuts['VR1_Tag_jets']      = '(' + OC+' && ('+SF+' || '+DF+')  && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)*'+btagWeight1tag

if 'WWValidationRegion' in opt.tag and 'WZtoWWValidationRegion' not in opt.tag:

    if 'Data' in opt.sigset:
        cuts['VR1_Veto_em']        = OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && '+bTagVeto
        cuts['VR1_Veto_sf']        = OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140 && '+bTagVeto
        cuts['VR1_Veto_mm']        = OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+bTagVeto
        cuts['VR1_Veto_ee']        = OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+bTagVeto
        cuts['VR1_Veto_em_0jet']   = OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0'
        cuts['VR1_Veto_sf_0jet']   = OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0'
        cuts['VR1_Veto_mm_0jet']   = OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && nCleanJet==0'
        cuts['VR1_Veto_ee_0jet']   = OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && nCleanJet==0'
        if 'More' in opt.tag:
            cuts['VR1_Veto_em_mt2']    = OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && mt2ll>100.'
            cuts['VR1_Veto_mm_mt2']    = OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.'
            cuts['VR1_Veto_ee_mt2']    = OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.'
        cuts['VR1_Veto_0jet']      = OC+' && ('+SF+' || '+DF+')  && ptmiss>=100 && ptmiss<140 && nCleanJet==0'

    else:
        cuts['VR1_Veto_em']        = '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['VR1_Veto_sf']        = '(' + OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['VR1_Veto_mm']        = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['VR1_Veto_ee']        = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['VR1_Veto_em_0jet']   = '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
        cuts['VR1_Veto_sf_0jet']   = '(' + OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
        cuts['VR1_Veto_mm_0jet']   = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
        cuts['VR1_Veto_ee_0jet']   = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
        if 'More' in opt.tag:
            cuts['VR1_Veto_em_mt2']    = '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && mt2ll>100.)'
            cuts['VR1_Veto_mm_mt2']    = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.)'
            cuts['VR1_Veto_ee_mt2']    = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.)'
        cuts['VR1_Veto_0jet']      = '(' + OC+' && ('+SF+' || '+DF+')  && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'

if 'SameSignValidationRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['SS_ptmiss']           = SSM+' && ptmiss'+ctrltag+'>=0   && '                         +bTagPass
        cuts['SS_ptmiss-100to140']  = SS +' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140 && '+bTagPass
        cuts['SS_ptmiss-140']       = SS +' && ptmiss'+ctrltag+'>=140 && '                         +bTagPass
        cuts['SS_ptmiss-160']       = SS +' && ptmiss'+ctrltag+'>=160 && '                         +bTagPass
        cuts['SS_ptmiss-160_plus']  = SSP+' && ptmiss'+ctrltag+'>=160 && '                         +bTagPass
        cuts['SS_ptmiss-160_minus'] = SSM+' && ptmiss'+ctrltag+'>=160 && '                         +bTagPass

    else:
        cuts['SS_ptmiss']            = '('+SSM+' && ptmiss'+ctrltag+'>=0  )*'+btagWeight1tag
        cuts['SS_ptmiss-100to140']   = '('+SS +' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140)*'+btagWeight1tag
        cuts['SS_ptmiss-140']        = '('+SS +' && ptmiss'+ctrltag+'>=140)*'+btagWeight1tag
        cuts['SS_ptmiss-160']        = '('+SS +' && ptmiss'+ctrltag+'>=160)*'+btagWeight1tag
        cuts['SS_ptmiss-160_plus']   = '('+SSP+' && ptmiss'+ctrltag+'>=160)*'+btagWeight1tag
        cuts['SS_ptmiss-160_minus']  = '('+SSM+' && ptmiss'+ctrltag+'>=160)*'+btagWeight1tag

if 'FakeValidationRegion' in opt.tag:
    
    Fake = LepId2of3 + ' && ' + OCT

    if 'Data' in opt.sigset:
        cuts['Fake']                  = Fake+' && ptmiss'+ctrltag+'>=0   && '                         +bTagPass
        cuts['Fake_ptmiss-100to140']  = Fake+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140 && '+bTagPass
        cuts['Fake_ptmiss-140']       = Fake+' && ptmiss'+ctrltag+'>=140 && '                         +bTagPass
        cuts['Fake_ptmiss-160']       = Fake+' && ptmiss'+ctrltag+'>=160 && '                         +bTagPass

    else:
        cuts['Fake']                   = '('+Fake+' && ptmiss'+ctrltag+'>=0  )*'+btagWeight1tag
        cuts['Fake_ptmiss-100to140']   = '('+Fake+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140)*'+btagWeight1tag
        cuts['Fake_ptmiss-140']        = '('+Fake+' && ptmiss'+ctrltag+'>=140)*'+btagWeight1tag
        cuts['Fake_ptmiss-160']        = '('+Fake+' && ptmiss'+ctrltag+'>=160)*'+btagWeight1tag

if 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag:

    WZselection = nLooseLepton+'==3 && ' + nTightLepton + '==3 && deltaMassZ'+ctrltag+'<ZCUT && ptmiss'+ctrltag+'>=METCUT'

    if 'WZValidationRegion' in opt.tag:

        if 'Data' in opt.sigset:
            cuts['WZ_3Lep_ptmiss-140']  = WZselection.replace('ZCUT', '999.').replace('METCUT', '140') + ' && ' + bTagVeto
            cuts['WZ_3LepZ_ptmiss-140'] = WZselection.replace('ZCUT',  '15.').replace('METCUT', '140') + ' && ' + bTagVeto
            cuts['WZ_3Lep_ptmiss-160']  = WZselection.replace('ZCUT', '999.').replace('METCUT', '160') + ' && ' + bTagVeto
            cuts['WZ_3LepZ_ptmiss-160'] = WZselection.replace('ZCUT',  '15.').replace('METCUT', '160') + ' && ' + bTagVeto

        else:
            cuts['WZ_3Lep_ptmiss-140']  = '(' + WZselection.replace('ZCUT', '999.').replace('METCUT', '140') + ')*'+btagWeight0tag
            cuts['WZ_3LepZ_ptmiss-140'] = '(' + WZselection.replace('ZCUT',  '15.').replace('METCUT', '140') + ')*'+btagWeight0tag
            cuts['WZ_3Lep_ptmiss-160']  = '(' + WZselection.replace('ZCUT', '999.').replace('METCUT', '160') + ')*'+btagWeight0tag
            cuts['WZ_3LepZ_ptmiss-160'] = '(' + WZselection.replace('ZCUT',  '15.').replace('METCUT', '160') + ')*'+btagWeight0tag

    elif 'WZtoWWValidationRegion' in opt.tag:

        if 'Data' in opt.sigset:
            cuts['WZtoWW_Zcut10_ptmiss-140'] = WZselection.replace('ZCUT', '10.').replace('METCUT', '140') + ' && ' + bTagVeto
            cuts['WZtoWW_Zcut15_ptmiss-140'] = WZselection.replace('ZCUT', '15.').replace('METCUT', '140') + ' && ' + bTagVeto
            cuts['WZtoWW_Zcut10_ptmiss-160'] = WZselection.replace('ZCUT', '10.').replace('METCUT', '160') + ' && ' + bTagVeto
            cuts['WZtoWW_Zcut15_ptmiss-160'] = WZselection.replace('ZCUT', '15.').replace('METCUT', '160') + ' && ' + bTagVeto

        else:
            cuts['WZtoWW_Zcut10_ptmiss-140'] = '('+WZselection.replace('ZCUT','10.').replace('METCUT','140')+')*'+btagWeight0tag
            cuts['WZtoWW_Zcut15_ptmiss-140'] = '('+WZselection.replace('ZCUT','15.').replace('METCUT','140')+')*'+btagWeight0tag
            cuts['WZtoWW_Zcut10_ptmiss-160'] = '('+WZselection.replace('ZCUT','10.').replace('METCUT','160')+')*'+btagWeight0tag
            cuts['WZtoWW_Zcut15_ptmiss-160'] = '('+WZselection.replace('ZCUT','15.').replace('METCUT','160')+')*'+btagWeight0tag

if 'ttZValidationRegion' in opt.tag or 'ZZValidationRegion' in opt.tag:

    sel4Lep = nLooseLepton+'==4 && ' + nTightLepton + '>=3'

    if 'ttZValidationRegion' in opt.tag:

        ttZselection = sel4Lep + ' && deltaMassZ'+ctrltag+'<10. && ptmiss'+ctrltag+'>=METCUT && nCleanJet>=2 && CleanJet_pt[1]>=20.'

        if 'Data' in opt.sigset:
            cuts['ttZ']            = ttZselection.replace('METCUT',   '0') + ' && ' + bTagPass
            cuts['ttZ_ptmiss-140'] = ttZselection.replace('METCUT', '140') + ' && ' + bTagPass
            cuts['ttZ_ptmiss-160'] = ttZselection.replace('METCUT', '160') + ' && ' + bTagPass
        else:
            cuts['ttZ']            = '(' + ttZselection.replace('METCUT',   '0') + ')*'+btagWeight1tag
            cuts['ttZ_ptmiss-140'] = '(' + ttZselection.replace('METCUT', '140') + ')*'+btagWeight1tag
            cuts['ttZ_ptmiss-160'] = '(' + ttZselection.replace('METCUT', '160') + ')*'+btagWeight1tag

    elif 'ZZValidationRegion' in opt.tag:

        ZZselection = sel4Lep + ' && deltaMassZ'+ctrltag+'<15. && ptmiss'+ctrltag+'>=METCUT'

        if 'Data' in opt.sigset:
            cuts['ZZ']            = ZZselection.replace('METCUT',   '0') + ' && ' + bTagVeto
            cuts['ZZ_ptmiss-140'] = ZZselection.replace('METCUT', '140') + ' && ' + bTagVeto
            cuts['ZZ_ptmiss-160'] = ZZselection.replace('METCUT', '160') + ' && ' + bTagVeto

        else:
            cuts['ZZ']            = '(' + ZZselection.replace('METCUT',   '0') + ')*'+btagWeight0tag
            cuts['ZZ_ptmiss-140'] = '(' + ZZselection.replace('METCUT', '140') + ')*'+btagWeight0tag
            cuts['ZZ_ptmiss-160'] = '(' + ZZselection.replace('METCUT', '160') + ')*'+btagWeight0tag

if 'DYValidationRegion' in opt.tag:

    DY = OC + ' && ' + LL + ' && ' + Zcut.replace('ZCUT',  '15.')

    if 'Data' in opt.sigset:
        cuts['Zpeak_ptmiss-100to140']       = DY + ' && ptmiss>=100 && ptmiss<140 && ' + bTagVeto
        cuts['Zpeak_ptmiss-140']            = DY + ' && ptmiss>=140 && '               + bTagVeto
        cuts['Zpeak_ptmiss-160']            = DY + ' && ptmiss>=160 && '               + bTagVeto
        cuts['Zpeak_ptmiss-100to140_nojet'] = DY + ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0'
        cuts['Zpeak_ptmiss-140_nojet']      = DY + ' && ptmiss>=140 && nCleanJet==0'            
        cuts['Zpeak_ptmiss-160_nojet']      = DY + ' && ptmiss>=160 && nCleanJet==0'            
        
    else:
        cuts['Zpeak_ptmiss-100to140']       = '(' + DY + ' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['Zpeak_ptmiss-140']            = '(' + DY + ' && ptmiss>=140)' +          '*'+btagWeight0tag
        cuts['Zpeak_ptmiss-160']            = '(' + DY + ' && ptmiss>=160)' +          '*'+btagWeight0tag
        cuts['Zpeak_ptmiss-100to140_nojet'] = '(' + DY + ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
        cuts['Zpeak_ptmiss-140_nojet']      = '(' + DY + ' && ptmiss>=140 && nCleanJet==0)' 
        cuts['Zpeak_ptmiss-160_nojet']      = '(' + DY + ' && ptmiss>=160 && nCleanJet==0)' 

if 'SignalRegion' in opt.tag:

    nojetcutSR1 = 'nCleanJet==0'
    jetscutSR1  = 'nCleanJet>0'
    nojetcutSR2 = nojetcutSR1
    jetscutSR2  = jetscutSR1

    if 'VisHT' in opt.tag:
        if 'VisHTv1' in opt.tag:
            visht = '('+sumLeptonPt+'+Sum$(CleanJet_pt))'
            nojetcutSR1 = visht+'<200'
            jetscutSR1  = visht+'>=200'
            nojetcutSR2 = visht+'<300'
            jetscutSR2  = visht+'>=300'
        elif 'VisHTv2' in opt.tag:
            visht = '(Sum$(CleanJet_pt))'
            nojetcutSR1 = visht+'<50'
            jetscutSR1  = visht+'>=50'
            nojetcutSR2 = visht+'<50'
            jetscutSR2  = visht+'>=50'
        elif 'VisHTv3' in opt.tag:
            visht = '('+sumLeptonPt+')'
            nojetcutSR1 = visht+'<100'
            jetscutSR1  = visht+'>=100'
            nojetcutSR2 = visht+'<100'
            jetscutSR2  = visht+'>=100'

    splitjets=False  
    if 'CharginoSignalRegions' in opt.tag or 'VisHT' in opt.tag: splitjets=True

    ptmiss_cuts={"SR1": ' && ptmiss>=140 && ptmiss<200 ',
                 "SR2": ' && ptmiss>=200 && ptmiss<300 ',
                 "SR3": ' && ptmiss>=300 '}
    if 'Optim' in opt.tag and 'Ptm' in opt.tag:
        ptmiss_cuts={"SR1": ' && ptmiss>=160 && ptmiss<220 ',
                     "SR2": ' && ptmiss>=220 && ptmiss<280 ',
                     "SR3": ' && ptmiss>=280 && ptmiss<380 ',
                     "SR4": ' && ptmiss>=380 '}

    for SR in ptmiss_cuts:

        isrcut = ''
        doISR  = False
        if "ISR" in opt. tag:
            if "ISR4" in opt.tag:
                if SR in ["SR4"]: doISR = True
            else:
                if SR in ["SR3","SR4"]:
                    doISR = True

        if doISR: isrcut=' && '+ISRCut

        if splitjets is True:
            if   SR == "SR1":
                jetscut  = ' && '+jetscutSR1
                nojetcut = ' && '+nojetcutSR1
            elif SR == "SR2":
                jetscut  = ' && '+jetscutSR2
                nojetcut = ' && '+nojetcutSR2

        if 'Data' in opt.sigset:
            btagcut=' && '+bTagPass
            vetocut=' && '+bTagVeto

            cuts[SR+'_Tag_em' ] = OC+' && '+DF+ptmiss_cuts[SR]+btagcut+isrcut
            cuts[SR+'_Tag_sf' ] = OC+' && '+SF+ptmiss_cuts[SR]+btagcut+isrcut

            if splitjets is True and SR in ["SR1","SR2"]:
                cuts[SR+'_NoTag_em'] = OC+' && '+DF+ptmiss_cuts[SR]+vetocut+jetscut+isrcut
                cuts[SR+'_NoTag_sf'] = OC+' && '+SF+ptmiss_cuts[SR]+vetocut+jetscut+isrcut

                cuts[SR+'_NoJet_em'] = OC+' && '+DF+ptmiss_cuts[SR]+vetocut+nojetcut+isrcut
                cuts[SR+'_NoJet_sf'] = OC+' && '+SF+ptmiss_cuts[SR]+vetocut+nojetcut+isrcut

            else:
                cuts[SR+'_Veto_em'] = OC+' && '+DF+ptmiss_cuts[SR]+vetocut+isrcut
                cuts[SR+'_Veto_sf'] = OC+' && '+SF+ptmiss_cuts[SR]+vetocut+isrcut

        else:
            btagcut=''
            vetocut=''

            cuts[SR+'_Tag_em' ]  = '(' + OC+' && '+DF+ptmiss_cuts[SR]+isrcut+btagcut+')*'+btagWeight1tag
            cuts[SR+'_Tag_sf' ]  = '(' + OC+' && '+SF+ptmiss_cuts[SR]+isrcut+btagcut+')*'+btagWeight1tag

            if splitjets is True and SR in ["SR1","SR2"]:
                cuts[SR+'_NoTag_em'] = '(' + OC+' && '+DF+ptmiss_cuts[SR]+isrcut+vetocut+jetscut +')*'+btagWeight0tag
                cuts[SR+'_NoTag_sf'] = '(' + OC+' && '+SF+ptmiss_cuts[SR]+isrcut+vetocut+jetscut +')*'+btagWeight0tag

                cuts[SR+'_NoJet_em'] = '(' + OC+' && '+DF+ptmiss_cuts[SR]+isrcut+vetocut+nojetcut+')*'+btagWeight0tag
                cuts[SR+'_NoJet_sf'] = '(' + OC+' && '+SF+ptmiss_cuts[SR]+isrcut+vetocut+nojetcut+')*'+btagWeight0tag

            else:
                cuts[SR+'_Veto_em']  = '(' + OC+' && '+DF+ptmiss_cuts[SR]+isrcut+vetocut+')*'+btagWeight0tag
                cuts[SR+'_Veto_sf']  = '(' + OC+' && '+SF+ptmiss_cuts[SR]+isrcut+vetocut+')*'+btagWeight0tag
    

# apply background scale factors
 
try:
    normBackgrounds
except NameError:
    normBackgrounds = None
   
if 'SignalRegions' in opt.tag and normBackgrounds is not None:
        
    for background in normBackgrounds:
        if background in samples:
            for region in normBackgrounds[background]:
                
                selections = [ ] 

                regionScaleFactor = normBackgrounds[background][region]['scalefactor'].keys()[0]

                for selection in normBackgrounds[background][region]['selections']:

                    usedSelection = False

                    for cut in cuts:
                        if selection=='_All' or selection in cut: 
                            normBackgrounds[background][region]['cuts'].append(cut)
                            usedSelection = True

                    if usedSelection:

                        selections.append(selection)

                        #if float(regionScaleFactor)!=1.:
                        #
                        #    selectionCut = normBackgrounds[background][region]['selections'][selection]
                        #    selectionWeight = '(!'+selectionCut+')+'+selectionCut+'*'+regionScaleFactor
                        #    samples[background]['weight'] += '*('+selectionWeight+')'
                
                if selections and float(regionScaleFactor)!=1.:

                    regionCut = '1.'

                    if len(selections)==1:
                        regionCut = normBackgrounds[background][region]['selections'][selections[0]]
                    else:
                        if '_Tag' in selections and '_NoTag' in selections and '_NoJet' not in selections:
                            regionCut = 'nCleanJet>=1'
                        elif '_Tag' in selections and '_Veto' in selections:
                            regionCut = '1.'

                    # Patches for ZZ veto
                    if '_Tag' in selections and '_Veto' not in selections and '_NoTag' not in selections:
                        regionCut = 'nCleanJet>=1'
                    if '_Veto' in selections and '_Tag' not in selections:
                        regionCut = 'nCleanJet==0'
                        regionScaleFactor = normBackgrounds[background]['nojet']['scalefactor'].keys()[0]

                    regionWeight = '(!'+regionCut+')+('+regionCut+')*'+regionScaleFactor
                    samples[background]['weight'] += '*('+regionWeight+')'
                    
