import ttbar
import sys
import nuSolutions as n
import ROOT as r
from math import sqrt
import math
import sys
import numpy as np
LinAlgError = np.linalg.linalg.LinAlgError
import matplotlib.pyplot as plt
from progress.bar import IncrementalBar
#######################################################
nameOfFile1 = sys.argv[1]
nameOfFile2 =  sys.argv[2]
nameOfFile3 = sys.argv[3]
f = r.TFile.Open(nameOfFile1, "read")
g = r.TFile.Open(nameOfFile2,"read")
h = r.TFile.Open(nameOfFile3,"read")
r.gROOT.SetBatch(1)
r.gROOT.LoadMacro('vecUtils.h'+'+')
#gStyle.SetOptStat(0)
#Reads the TTree t

eventcounter = 0
h_overlapingFactorttbar = r.TH1F('overlapingFactorttbar','Overlaping Factor ttbar',200,0, 5)
h_overlapingFactorttDM10 = r.TH1F('overlapingFactorttDM10','Overlaping Factor ttDM10',200,0,5)
h_overlapingFactorttDM100 = r.TH1F('overlapingFactorttDM100','Overlaping Factor ttDM100',200,0,5)
h_darkptt = r.TH1F('darkptt','Dark Pt ttbar',200,0,600)
h_darkptDM10 = r.TH1F('darkptDM10','Dark Pt 10 GeV',50,0,600)
h_darkptDM100 = r.TH1F('darkptDM100','Dark Pt 100 GeV',50,0,600)
h_darkptChiDM10 = r.TH1F('darkptChiDM10','(Dark Pt-Chi(Pt))/Chi(Pt) 10 GeV',200,0,6)
h_darkptChiDM100 = r.TH1F('darkptChiDM100','(Dark Pt-Chi(Pt))/Chi(Pt) 100 GeV',200,0,6)

r.gStyle.SetOptStat(0)
bar1 = IncrementalBar('ttbar',max=f.t.GetEntriesFast())
i=0
for event in f.t:

     #if eventcounter != 1:
        #eventcounter = eventcounter + 1
        #continue

     #print '---Comienzo de evento ttbar---'+str(eventcounter)
     Tb1   = r.TLorentzVector()
     Tb2   = r.TLorentzVector()
     Tlep1 = r.TLorentzVector()
     Tlep2 = r.TLorentzVector()
     Tnu1  = r.TLorentzVector()
     Tnu2  = r.TLorentzVector()
     TMET  = r.TLorentzVector()
     #Ellipse variation of met
     for j in range(0,1):
       #TLorentz Vectors of the particles in ttbar
       Tb1.SetPtEtaPhiM(event.ptb1,event.etab1,event.phib1, event.mb1)
       Tb2.SetPtEtaPhiM(event.ptb2,event.etab2,event.phib2, event.mb2)
       Tlep1.SetPtEtaPhiM(event.ptlep1,event.etalep1,event.philep1, event.mlep1)
       Tlep2.SetPtEtaPhiM(event.ptlep2,event.etalep2,event.philep2, event.mlep2)
       Tnu1.SetPtEtaPhiM(event.ptnu1, event.etanu1, event.phinu1, event.mnu1)
       Tnu2.SetPtEtaPhiM(event.ptnu2, event.etanu2, event.phinu2, event.mnu2)
       TMET.SetPtEtaPhiM(event.ptMET,event.etaMET,event.phiMET,event.mMET)
       mW1   = (Tnu1+Tlep1).M()
       mW2   = (Tnu2+Tlep2).M()
       mTOP1 = (Tnu1+Tlep1+Tb1).M()
       mTOP2 = (Tnu2+Tlep2+Tb2).M()
       try:
         nuSol=ttbar.solveNeutrino(Tb1, Tb2, Tlep1, Tlep2, Tnu1, Tnu2, TMET, mW1, mW2, mTOP1, mTOP2)
         h_overlapingFactorttbar.Fill(nuSol.overlapingFactor(nuSol.N,nuSol.n_))
         if nuSol.overlapingFactor(nuSol.N,nuSol.n_)<0.2:
            darkPt = nuSol.darkPt('DarkPt')
            h_darkptt.Fill(darkPt) 
            #m,b=nuSol.ellipseSeparation(nuSol.N,nuSol.n_,'LineParameters')
            #x=np.r_[-600:600]
            #plt.plot(x,m*x+b);
            #plt.show()
            #nuSol.darkPt('ttbarEllipse')
            #nuSol.plotEllipse(nuSol.N,'black')
            #nuSol.plotEllipse(nuSol.n_,'red') 
               
       except LinAlgError :
      #   print 'No hay solucion'
         continue
     #print '-------Fin de evento------'
     eventcounter+=1
     #plt.savefig('ElipsesDARKPT/Elipse'+str(i)+'.png')
     #plt.clf()
     i=i+1
     bar1.next()
bar1.finish()


scaleOverlapingttbar = 1./h_overlapingFactorttbar.Integral()
scaledarkptt = 1./h_darkptt.Integral()


eventcounter1=0
#print '10 GeV'
bar2 = IncrementalBar('ttDM10',max=g.t.GetEntriesFast())
for event in g.t:

     #if eventcounter1 != 1:
        #eventcounter1 = eventcounter1 + 1
        #continue

     #print '---Comienzo de evento 10 GeV---'+str(eventcounter1)
     Tb1   = r.TLorentzVector()
     Tb2   = r.TLorentzVector()
     Tlep1 = r.TLorentzVector()
     Tlep2 = r.TLorentzVector()
     Tnu1  = r.TLorentzVector()
     Tnu2  = r.TLorentzVector()
     TMET  = r.TLorentzVector()
     #Ellipse variation of met
     for j in range(0,1):
       #TLorentz Vectors of the particles in ttbar
       Tb1.SetPtEtaPhiM(event.ptb1,event.etab1,event.phib1, event.mb1)
       Tb2.SetPtEtaPhiM(event.ptb2,event.etab2,event.phib2, event.mb2)
       Tlep1.SetPtEtaPhiM(event.ptlep1,event.etalep1,event.philep1, event.mlep1)
       Tlep2.SetPtEtaPhiM(event.ptlep2,event.etalep2,event.philep2, event.mlep2)
       Tnu1.SetPtEtaPhiM(event.ptnu1, event.etanu1, event.phinu1, event.mnu1)
       Tnu2.SetPtEtaPhiM(event.ptnu2, event.etanu2, event.phinu2, event.mnu2)
       TMET.SetPtEtaPhiM(event.ptMET,event.etaMET,event.phiMET,event.mMET)
       mW1   = (Tnu1+Tlep1).M()
       mW2   = (Tnu2+Tlep2).M()
       mTOP1 = (Tnu1+Tlep1+Tb1).M()
       mTOP2 = (Tnu2+Tlep2+Tb2).M()
       try:
         nuSol=ttbar.solveNeutrino(Tb1, Tb2, Tlep1, Tlep2, Tnu1, Tnu2, TMET, mW1, mW2, mTOP1, mTOP2)
         h_overlapingFactorttDM10.Fill(nuSol.overlapingFactor(nuSol.N,nuSol.n_))
         if nuSol.overlapingFactor(nuSol.N,nuSol.n_)<0.2:
           darkPt=nuSol.darkPt('DarkPt')
           h_darkptDM10.Fill(darkPt)
           h_darkptChiDM10.Fill(abs(darkPt-event.ptChi1)/event.ptChi1)
       except LinAlgError :
      #   print 'No hay solucion'
         continue
     #print '-------Fin de evento------'
     eventcounter1+=1
     bar2.next()  
bar2.finish() 
scaledarkptDM10=1./h_darkptDM10.Integral()
scaledarkptChiDM10=1./h_darkptChiDM10.Integral()
scaleOverlapingttDM10=1./h_overlapingFactorttDM10.Integral()


eventcounter2=0
bar3 = IncrementalBar('ttDM100',max=h.t.GetEntriesFast())
for event in h.t:

     #if eventcounter2 != 1:
        #eventcounter2 = eventcounter2 + 1
        #continue

     #print '---Comienzo de evento 100 GeV---'+str(eventcounter2)
     Tb1   = r.TLorentzVector()
     Tb2   = r.TLorentzVector()
     Tlep1 = r.TLorentzVector()
     Tlep2 = r.TLorentzVector()
     Tnu1  = r.TLorentzVector()
     Tnu2  = r.TLorentzVector()
     TMET  = r.TLorentzVector()
     #Ellipse variation of met
     for j in range(0,1):
       #TLorentz Vectors of the particles in ttbar
       Tb1.SetPtEtaPhiM(event.ptb1,event.etab1,event.phib1, event.mb1)
       Tb2.SetPtEtaPhiM(event.ptb2,event.etab2,event.phib2, event.mb2)
       Tlep1.SetPtEtaPhiM(event.ptlep1,event.etalep1,event.philep1, event.mlep1)
       Tlep2.SetPtEtaPhiM(event.ptlep2,event.etalep2,event.philep2, event.mlep2)
       Tnu1.SetPtEtaPhiM(event.ptnu1, event.etanu1, event.phinu1, event.mnu1)
       Tnu2.SetPtEtaPhiM(event.ptnu2, event.etanu2, event.phinu2, event.mnu2)
       TMET.SetPtEtaPhiM(event.ptMET,event.etaMET,event.phiMET,event.mMET)
       mW1   = (Tnu1+Tlep1).M()
       mW2   = (Tnu2+Tlep2).M()
       mTOP1 = (Tnu1+Tlep1+Tb1).M()
       mTOP2 = (Tnu2+Tlep2+Tb2).M()
       try:
           nuSol=ttbar.solveNeutrino(Tb1, Tb2, Tlep1, Tlep2, Tnu1, Tnu2, TMET, mW1, mW2, mTOP1, mTOP2)
           h_overlapingFactorttDM100.Fill(nuSol.overlapingFactor(nuSol.N,nuSol.n_))
           if nuSol.overlapingFactor(nuSol.N,nuSol.n_)<0.2:
             darkpt = nuSol.darkPt('DarkPt')
             h_darkptDM100.Fill(darkpt)
             h_darkptChiDM100.Fill(abs(darkPt-event.ptChi1)/event.ptChi1)
       except LinAlgError :
      #   print 'No hay solucion'
         continue
     #print '-------Fin de evento------'
     bar3.next()
     eventcounter2+=1
bar3.finish()

scaledarkptDM100=1./h_darkptDM100.Integral()
scaledarkptChiDM100=1./h_darkptChiDM100.Integral()
scaleOverlapingttDM100=1./h_overlapingFactorttDM100.Integral()
#Save histograms

h_overlapingFactorttbar.SetLineColor(1)
h_overlapingFactorttDM10.SetLineColor(2)
h_overlapingFactorttDM100.SetLineColor(4)


h_darkptt.SetLineColor(1)
h_darkptDM10.SetLineColor(2)
h_darkptDM100.SetLineColor(4)


c_overlapingFactor=r.TCanvas('Dark Pt','Dark Pt')
c_overlapingFactor.cd()
leg_overlap = r.TLegend(0.6,0.6,0.8,0.8)
leg_overlap.AddEntry(h_overlapingFactorttbar,"ttbar","L")
leg_overlap.AddEntry(h_overlapingFactorttDM10,"ttDM10","L")
leg_overlap.AddEntry(h_overlapingFactorttDM100,"ttDM100","L")

h_overlapingFactorttbar.Scale(scaleOverlapingttbar)
h_overlapingFactorttbar.Draw()
h_overlapingFactorttbar.GetXaxis().SetTitle('R')
h_overlapingFactorttDM10.Scale(scaleOverlapingttDM10)
h_overlapingFactorttDM10.Draw("SAME")
h_overlapingFactorttDM100.Scale(scaleOverlapingttDM100)
h_overlapingFactorttDM100.Draw("SAME")
leg_overlap.Draw()
c_overlapingFactor.SaveAs('OverlapingFactorComparePseudoscalar.png')


c_darkPt=r.TCanvas('Dark Pt','Dark Pt')
c_darkPt.cd()
leg = r.TLegend(0.6,0.6,0.8,0.8)
leg.AddEntry(h_darkptt,"ttbar","L")
leg.AddEntry(h_darkptDM10,"ttDM10","L")
leg.AddEntry(h_darkptDM100,"ttDM100","L")
h_darkptt.Scale(scaledarkptt)
h_darkptt.Draw()
h_darkptt.GetXaxis().SetTitle('darkPt [GeV]')
h_darkptDM10.Scale(scaledarkptDM10)
h_darkptDM10.Draw("SAME")
h_darkptDM100.Scale(scaledarkptDM100)
h_darkptDM100.Draw("SAME")
leg.Draw()
c_darkPt.SaveAs('DarkPtR02ComparePseudoscalar.png')


h_darkptChiDM10.SetLineColor(1)
h_darkptChiDM100.SetLineColor(2)

c_darkPtDiscrepancy=r.TCanvas('Dark Pt/Pt(Chi)','Dark Pt/Pt(Chi)')
c_darkPtDiscrepancy.cd()
leg2 = r.TLegend(0.6,0.6,0.8,0.8)
leg2.AddEntry(h_darkptChiDM10,"ttDM10","L")
leg2.AddEntry(h_darkptChiDM100,"ttDM100","L")
h_darkptChiDM10.Scale(scaledarkptDM10)
h_darkptChiDM10.Draw()
h_darkptChiDM10.GetXaxis().SetTitle('|DarkPt-Pt(Chi)|/Pt(Chi)')
h_darkptChiDM100.Scale(scaledarkptDM10)
h_darkptChiDM100.Draw("SAME")
leg2.Draw()
c_darkPtDiscrepancy.SaveAs('DarkPtChiR02ComparePseudoscalar.png')
