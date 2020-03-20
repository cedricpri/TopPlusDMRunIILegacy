import nuSolutions as n
import ROOT as r
from math import sqrt
import math
import sys
import numpy as np
LinAlgError = np.linalg.linalg.LinAlgError
import matplotlib.pyplot as plt


class solveNeutrino(object):
  '''Solves the neutrino momenta in tt-->n_nll_bb_'''  
  
  def __init__(self,Tb,Tb_,Tmu,Tmu_,Tnu,Tnu_,TMET,TChi,mW,mW_,mt,mt_): #Tb,Tmu,Tnu are TLorentzVectors
      r.gROOT.SetBatch(1)
      r.gROOT.LoadMacro('vecUtils.h'+'+')
      lv = r.Math.LorentzVector(r.Math.PtEtaPhiE4D('float'))
  
      #Particle vectors
      self.b=lv(Tb.Pt(),Tb.Eta(),Tb.Phi(), Tb.E())
      self.b_=lv(Tb_.Pt(),Tb_.Eta(),Tb_.Phi(), Tb_.E())
      self.mu=lv(Tmu.Pt(),Tmu.Eta(),Tmu.Phi(), Tmu.E())
      self.mu_=lv(Tmu_.Pt(),Tmu_.Eta(),Tmu_.Phi(), Tmu_.E())
      self.TMET=lv(TMET.Pt(),TMET.Eta(),TMET.Phi(), TMET.E())
      self.TChi=lv(TChi.Pt(),TChi.Eta(),TChi.Phi(), TChi.E())
      #self.metX=(TMET-TChi).Px()
      #self.metY=(TMET-TChi).Py()
      self.metX=TMET.Px()
      self.metY=TMET.Py()
      self.mW2=mW**2
      self.mt2=mt**2
      self.mt_2=mt_**2
      self.mW_2=mW_**2
      
      #Ellipse Matrices
      self.N=n.nuSolutionSet(self.b,self.mu, self.mW2, self.mt2).N
      self.N_=n.nuSolutionSet(self.b_,self.mu_, self.mW_2, self.mt_2).N
      self.Gamma=np.outer([self.metX,self.metY,0],[0,0,1])-n.UnitCircle()
      self.n_=self.Gamma.T.dot(self.N_).dot(self.Gamma)
      
 
      #DM Ellipse Matrix
      #ADM,BDM,CDM,DDM,FDM,GDM=self.n_[0][0], self.n_[0][1], self.n_[1][1], self.n_[0][2], self.n_[1][2],self.n_[2][2] 
      #Dp=DDM+ADM*TChi.Px()+BDM*TChi.Py()
      #Fp=FDM+BDM*TChi.Px()+CDM*TChi.Py()
      #Gp=GDM+2*DDM*TChi.Px()+2*FDM*TChi.Py()+ADM*TChi.Px()**2+BDM*TChi.Py()*TChi.Px()+CDM*TChi.Py()**2
      #self.DM=np.array([[ADM,BDM,Dp],[BDM,CDM,Fp],[Dp,Fp,Gp]])
  @property
  def solution(self):
      '''Solves the neutrino momenta'''
      doubleNeutrinoSolutions = n.doubleNeutrinoSolutions
      dns = doubleNeutrinoSolutions((self.b, self.b_), (self.mu, self.mu_), (self.metX, self.metY),self.mW2,self.mt2) 
      solutions = dns.nunu_s
      return solutions


  def calculateEllipseParameter(self,Matrix,Parameter):
      '''Calculates the center, major and minor semiaxis of ellipse of the given Matrix'''
      A, B, C, D, F, G=Matrix[0][0], Matrix[0][1], Matrix[1][1], Matrix[0][2], Matrix[1][2], Matrix[2][2]

      if Parameter == 'Center':
         #Elipse Center
         x0=(C*D-B*F)/(B**2-A*C)
         y0=(A*F-B*D)/(B**2-A*C)
         return (x0,y0)
      elif Parameter == 'Semiaxis': 
         #Semiaxis
         a=sqrt((2*(A*F**2+C*D**2+G*B**2-2*B*D*F-A*C*G))/((B**2-A*C)*(sqrt((A-C)**2+4*B**2)-(A+C))))
         b=sqrt((2*(A*F**2+C*D**2+G*B**2-2*B*D*F-A*C*G))/((B**2-A*C)*(-sqrt((A-C)**2+4*B**2)-(A+C)))) 
         return (a,b)  
      elif Parameter == 'Angle':
         #Counterclowise angle rotation from x axis to the major axis 
         if (B == 0 and A < C):
             angle=0    
         elif (B == 0 and A > C):
             angle=math.pi/2
         elif (B != 0 and A < C):
             cotan=1/math.tan((A-C)/(2.*B))
             angle=0.5*math.atan(cotan)
         elif (B != 0 and A > C):
             cotan=1/math.tan((A-C)/(2.*B))
             angle=0.5*math.pi+0.5*math.atan(cotan) 
         return angle
      else:
         print 'Wrong Input Name'
         return -1

  def ellipseSeparation(self,Matrix1,Matrix2,Parameter):
      '''Calculates the distance between the the centers of two ellipses'''
      x1,y1=self.calculateEllipseParameter(Matrix1,'Center')
      x2,y2=self.calculateEllipseParameter(Matrix2,'Center')
      m=(y2-y1)/(x2-x1)
      b=y1-m*x1 
      if Parameter == 'Distance':
         distance=math.sqrt((x1-x2)**2+(y1-y2)**2)
         return distance
      elif Parameter == 'Projections':
         A1, B1, C1, D1, F1, G1 = Matrix1[0][0], Matrix1[0][1], Matrix1[1][1], Matrix1[0][2], Matrix1[1][2], Matrix1[2][2]
         A2, B2, C2, D2, F2, G2 = Matrix2[0][0], Matrix2[0][1], Matrix2[1][1], Matrix2[0][2], Matrix2[1][2], Matrix2[2][2]
      
         #Matrix 1 Projections
         u1=A1+2*B1*m+C1*m**2 
         v1=2*B1*b+2*m*b*C1+2*D1+2*F1*m 
         w1=G1+C1*b**2+2*F1*b
         x1cut1=(-v1+sqrt(v1**2-4*u1*w1))/(2*u1)
         x1cut2=(-v1-sqrt(v1**2-4*u1*w1))/(2*u1)
         y1cut1=m*x1cut1+b
         y1cut2=m*x1cut2+b
         projection1=sqrt((x1cut1-x1cut2)**2+(y1cut1-y1cut2)**2)/2 
                             
         #Matrix 2 Projections
         u2=A2+2*B2*m+C2*m**2
         v2=2*B2*b+2*m*b*C2+2*D2+2*F2*m
         w2=G2+C2*b**2+2*F2*b
         x2cut1=(-v2+sqrt(v2**2-4*u2*w2))/(2*u2)
         x2cut2=(-v2-sqrt(v2**2-4*u2*w2))/(2*u2)
         print x2cut1, x2cut2
         y2cut1=m*x2cut1+b
         y2cut2=m*x2cut2+b
         projection2=sqrt((x2cut1-x2cut2)**2+(y2cut1-y2cut2)**2)/2
         return (projection1,projection2)
      elif Parameter == 'LineParameters':
           return (m,b) 
      else:
       print 'Wrong Input Name'
       return -1 
  
  def overlapingFactor(self, Matrix1, Matrix2):
      d=self.ellipseSeparation(Matrix1,Matrix2,'Distance') 
      l1,l2=self.ellipseSeparation(Matrix1,Matrix2,'Projections')
      #overlap=l1*l2/d**2
      overlap=(l1+l2)/d
      return overlap
  
  
  def plotEllipse(self,Matrix,Color):
      '''Plots the ellipse given by Matrix'''
      x0,y0=self.calculateEllipseParameter(Matrix,'Center')
      a,b=self.calculateEllipseParameter(Matrix,'Semiaxis')
      pxnu,pynu=np.linspace((x0-2*a),(x0+2*a),1000),np.linspace((y0-2*a),(y0+2*a),1000)
      p,q=np.meshgrid(pxnu,pynu)
      f = lambda x, y: np.array([x,y,1]).T.dot(Matrix).dot(np.array([x,y,1]))
      z=f(p,q)
      plt.contour(p,q,z,[0],colors=Color)
      plt.xlabel('px/GeV')
      plt.ylabel('py/Gev')
  
  @property
  def plotDMEllipse(self):
      '''Gets DM ellipse equation'''
      pxnu,pynu =np.linspace(-1000,1000,1000),np.linspace(-1000,1000,100)
      p,q=np.meshgrid(pxnu,pynu)
      pxphi, pyphi =TChi.Px(),TChi.Py()
      phi=np.array([pxphi,pyphi,0])
      f = lambda x,y: (np.array([x,y,1])+phi).T.dot(self.n_).dot(np.array([x,y,1])+phi)
      #g = lambda u,v: (self.Gamma.dot(np.array([u,v,1])-phi)).T.dot(self.N_).dot(np.array([u,v,1]).dot(self.Gamma)-phi)
      z=f(p,q)
      #h=g(p,q)
      plt.contour(p,q,z,[0])
      #plt.contour(p,q,h,[0],colors='r')
      plt.xlabel('px/GeV')
      plt.ylabel('py/Gev')
  
  
#######################################################
nameOfFile = sys.argv[1]

f = r.TFile.Open(nameOfFile, "read")

#Reads the TTree t
eventcounter = 0
h_overlap=r.TH1F('Overlap DM 10 GeV Pseudoscalar','Overlap DM 10 GeV Pseudoscalar',200,0,8)
noSolution=0;

for event in f.t:

     #if eventcounter != 0:
       # eventcounter = eventcounter + 1
       # continue

     print '---Comienzo de evento---' + str(eventcounter)
     Tb=r.TLorentzVector()
     Tb_=r.TLorentzVector()
     Tlep=r.TLorentzVector()
     Tlep_=r.TLorentzVector()
     Tnu=r.TLorentzVector()
     Tnu_=r.TLorentzVector()
     TChi=r.TLorentzVector()
     TMET=r.TLorentzVector()
     #Ellipse variation of met
     for j in range(0, 1):
       #TLorentz Vectors of the particles in ttbarDM
       Tb.SetPtEtaPhiM(event.ptb1,event.etab1,event.phib1, event.mb1)
       Tb_.SetPtEtaPhiM(event.ptb2,event.etab2,event.phib2, event.mb2)
       Tlep.SetPtEtaPhiM(event.ptlep1,event.etalep1,event.philep1, event.mlep1)
       Tlep_.SetPtEtaPhiM(event.ptlep2,event.etalep2,event.philep2, event.mlep2)
       Tnu.SetPtEtaPhiM(event.ptnu1, event.etanu1, event.phinu1, event.mnu1)
       Tnu_.SetPtEtaPhiM(event.ptnu2, event.etanu2, event.phinu2, event.mnu2) 
       TChi.SetPtEtaPhiM(event.ptChi1,event.etaChi1,event.phiChi1, event.mChi1)
       TMET.SetPtEtaPhiM(event.ptMET,event.etaMET,event.phiMET, event.mMET)
      
       mW=(Tnu+Tlep_).M() 
       mW_=(Tnu_+Tlep).M()
       mTOP=(Tnu_+Tlep+Tb).M()
       mTOP_=(Tnu+Tlep_+Tb_).M()   
       try:
         nuSol=solveNeutrino(Tb,Tb_,Tlep,Tlep_,Tnu,Tnu_,TMET,TChi,mW,mW_,mTOP,mTOP_)     
         #Plot the line that passes through the ellipse center
         #m,b=nuSol.ellipseSeparation(nuSol.N,nuSol.n_,'LineParameters')
         #x=np.r_[-330:0]
         #plt.plot(x,m*x+b);
         #plt.show()
         #nuSol.plotEllipse(nuSol.N,'r')
         #nuSol.plotEllipse(nuSol.n_,'b')
         #nuSol.plotEllipse(nuSol.DM,'b')
         #nuSol.plotDMEllipse
         #print 'OVERLAP FACTOR'
         overlaping= nuSol.overlapingFactor(nuSol.N,nuSol.n_)  
         h_overlap.Fill(overlaping)         
       except LinAlgError :
         print 'No hay solucion'
         noSolution=noSolution+1
         continue
       
     print '-------Fin de evento------'
     #plt.savefig('ElipsesDM/ElipseDM'+str(eventcounter)+'.png')
     #plt.clf()
     eventcounter+=1
     print noSolution
print "EVENTOS SIN SOLUCION=" + str(noSolution)
scale=1./(h_overlap.Integral())
canvas=r.TCanvas('Dark Matter 10 GeV Overlap Pseudoscalar','Overlaping Factor 10 GeV Pseudoscalar')
canvas.cd()
h_overlap.Scale(scale)
h_overlap.Draw()
h_overlap.GetXaxis().SetTitle('R')
canvas.SaveAs('OverlapingDM_10_GeV_Pseudo.png') 
