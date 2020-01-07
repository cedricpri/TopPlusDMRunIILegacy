import nuSolutions as n
import ROOT as r
from math import sqrt
import math
import sys
import numpy as np
LinAlgError = np.linalg.linalg.LinAlgError
import matplotlib.pyplot as plt


class solveNeutrino(object):
  '''Class that solves the different variables in tt-->n_nll_bb_ decays'''  
  
  def __init__(self,Tb1, Tb2, Tmu1, Tmu2, Tnu1, Tnu2, TMET, mW1, mW2, mt1, mt2): #Tb,Tmu,Tnu are TLorentzVectors
      #r.gROOT.SetBatch(1)
      #r.gROOT.LoadMacro('vecUtils.h'+'+')
      lv = r.Math.LorentzVector(r.Math.PtEtaPhiE4D('float'))
  
      #Particle vectors
      self.b1  = lv(Tb1.Pt(),Tb1.Eta(),Tb1.Phi(), Tb1.E())
      self.b2  = lv(Tb2.Pt(),Tb2.Eta(),Tb2.Phi(), Tb2.E())
      self.mu1 = lv(Tmu1.Pt(),Tmu1.Eta(),Tmu1.Phi(), Tmu1.E())
      self.mu2 = lv(Tmu2.Pt(),Tmu2.Eta(),Tmu2.Phi(), Tmu2.E())
      self.metX = TMET.Px()
      self.metY = TMET.Py()
      self.mW2_1 = mW1**2
      self.mt2_1 = mt1**2
      self.mt2_2 = mt2**2
      self.mW2_2 = mW2**2
      
      #Ellipse Matrices
      self.N = n.nuSolutionSet(self.b1,self.mu1, self.mW2_1, self.mt2_1).N
      self.N_ = n.nuSolutionSet(self.b2,self.mu2, self.mW2_2, self.mt2_2).N
      self.Gamma = np.outer([self.metX,self.metY,0],[0,0,1])-n.UnitCircle()
      self.n_ = self.Gamma.T.dot(self.N_).dot(self.Gamma)

  @property
  def solution(self):
      '''Solves the neutrino momenta'''
      doubleNeutrinoSolutions = n.doubleNeutrinoSolutions
      dns = doubleNeutrinoSolutions((self.b1, self.b2), (self.mu1, self.mu2), (self.metX, self.metY),self.mW2_2,self.mt2_2) 
      solutions = dns.nunu_s
      return solutions


  def calculateEllipseParameter(self,Matrix,Parameter):
      '''Calculates the center, major and minor semiaxis of ellipse of the given Matrix'''
      A, B, C, D, F, G = Matrix[0][0], Matrix[0][1], Matrix[1][1], Matrix[0][2], Matrix[1][2], Matrix[2][2]

      if Parameter == 'Center':
         #Elipse Center
         x0 = (C*D-B*F)/(B**2-A*C)
         y0 = (A*F-B*D)/(B**2-A*C)
         return (x0,y0)
      elif Parameter == 'Semiaxis': 
         #Semiaxis a (Major), b (Minor)
         a = sqrt((2*(A*F**2+C*D**2+G*B**2-2*B*D*F-A*C*G))/((B**2-A*C)*(sqrt((A-C)**2+4*B**2)-(A+C))))
         b = sqrt((2*(A*F**2+C*D**2+G*B**2-2*B*D*F-A*C*G))/((B**2-A*C)*(-sqrt((A-C)**2+4*B**2)-(A+C)))) 
         return (a,b)  
      elif Parameter == 'Angle':
         #Counterclowise angle rotation from x axis to the major axis 
         #angle = 0
         if (B == 0 and A < C):
             angle = 0    
         elif (B == 0 and A > C):
             angle = math.pi/2
         elif (B != 0 and A < C):
             cotan=1/math.tan((A-C)/(2.*B))
             angle = 0.5*math.atan(cotan)
         elif (B != 0 and A > C):
             cotan=1/math.tan((A-C)/(2.*B))
             angle = 0.5*math.pi+0.5*math.atan(cotan) 
         return angle
      else:
         print 'Wrong Input Name'
         return -1

  def ellipseSeparation(self,Matrix1,Matrix2,Parameter):
      '''Calculates the distance between the the centers of two ellipses, the projection of the line that unites them and the linear parameters'''
      x1,y1 = self.calculateEllipseParameter(Matrix1,'Center')
      x2,y2 = self.calculateEllipseParameter(Matrix2,'Center')
      m = (y2-y1)/(x2-x1)
      b = y1-m*x1 
   
      if Parameter == 'Distance':
         distance = math.sqrt((x1-x2)**2+(y1-y2)**2)
         return distance
      elif Parameter == 'Projections':
         
         A1, B1, C1, D1, F1, G1 = Matrix1[0][0], Matrix1[0][1], Matrix1[1][1], Matrix1[0][2], Matrix1[1][2], Matrix1[2][2]
         A2, B2, C2, D2, F2, G2 = Matrix2[0][0], Matrix2[0][1], Matrix2[1][1], Matrix2[0][2], Matrix2[1][2], Matrix2[2][2]
         
         #The cut between the line and one of the ellipses is given by a two degree polynomial with solution x=-v+-sqrt(v**2-4*u*w)/2*u 
          
         #Matrix 1 Projections
         u1 = A1+2*B1*m+C1*m**2 
         v1 = 2*B1*b+2*m*b*C1+2*D1+2*F1*m 
         w1 = G1+C1*b**2+2*F1*b
         x1cut1 = (-v1+sqrt(v1**2-4*u1*w1))/(2*u1)
         x1cut2 = (-v1-sqrt(v1**2-4*u1*w1))/(2*u1)
         y1cut1 = m*x1cut1+b
         y1cut2 = m*x1cut2+b
         projection1 = sqrt((x1cut1-x1cut2)**2+(y1cut1-y1cut2)**2)/2 
                             
         #Matrix 2 Projections
         u2 = A2+2*B2*m+C2*m**2
         v2 = 2*B2*b+2*m*b*C2+2*D2+2*F2*m
         w2 = G2+C2*b**2+2*F2*b
         x2cut1 = (-v2+sqrt(v2**2-4*u2*w2))/(2*u2)
         x2cut2 = (-v2-sqrt(v2**2-4*u2*w2))/(2*u2)
         y2cut1 = m*x2cut1+b
         y2cut2 = m*x2cut2+b
         projection2 = sqrt((x2cut1-x2cut2)**2+(y2cut1-y2cut2)**2)/2
         #return x1cut1, x1cut2, y1cut1, y1cut2, x2cut1, x2cut2, y2cut1, y2cut2
         return (projection1,projection2)
     
      elif Parameter == 'LineParameters':
           return (m,b) 
     
      else:
        print 'Wrong Input Name'
        return -1 
  
  def overlapingFactor(self, Matrix1, Matrix2):
      d = self.ellipseSeparation(Matrix1,Matrix2,'Distance') 
      l1,l2 = self.ellipseSeparation(Matrix1,Matrix2,'Projections')
      overlap = (l1+l2)/d
      return overlap
  
 
  def getEllipseEquation(self,Matrix):
      '''Gets neutrino equation of the given Matrix'''
      pxnu,pynu = np.linspace(-5,5,100),np.linspace(-5,5,100)
      pnu = np.array([pxnu,pynu,1])
      elipseEquation = pnu.T.dot(Matrix).dot(pnu)
      return elipseEquation

  
  def plotEllipse(self,Matrix,color):
      '''Plots the given ellipse'''
      x0,y0 = self.calculateEllipseParameter(Matrix,'Center')
      a,b = self.calculateEllipseParameter(Matrix,'Semiaxis')
      pxnu,pynu = np.linspace((x0-2*a),(x0+2*a),1000),np.linspace((y0-2*a),(y0+2*a),1000)
      p,q = np.meshgrid(pxnu,pynu)
      f = lambda x, y: np.array([x,y,1]).T.dot(Matrix).dot(np.array([x,y,1]))
      z = f(p,q)
      plt.contour(p,q,z,[0],colors=color)
      plt.xlabel('px/GeV')
      plt.ylabel('py/Gev')

  def darkPt(self,Parameter):
     '''Moves the n_ ellipse to the first point that cuts N in the direction of the line that unites the two centers'''
     
     A,B,C,D,F,G = self.N_[0][0],self.N_[0][1],self.N_[1][1],self.N_[0][2],self.N_[1][2],self.N_[2][2]
     Dp,Fp,Gp = self.n_[0][2],self.n_[1][2],self.n_[2][2]
     m,b = self.ellipseSeparation(self.N, self.n_,'LineParameters')
     d = self.ellipseSeparation(self.N,self.n_,'Distance')
     l1,l2 = self.ellipseSeparation(self.N,self.n_,'Projections')
     x0,y0 = self.calculateEllipseParameter(self.N_,'Center')
     x0p,y0p = self.calculateEllipseParameter(self.n_,'Center')
     x0N, y0N = self.calculateEllipseParameter(self.N,'Center')
     theta = math.atan(abs(m))
     deltax,deltay = 0.0, 0.0    #(d-l1-l2)*math.cos(theta),(d-l1-l2)*math.sin(theta) #dx-l1x-l2x, dy-l1y-l2y

     if y0p<y0N:
        deltay = (d-l1-l2)*math.sin(theta)
     elif y0p>y0N:
        deltay = -(d-l1-l2)*math.sin(theta)
  
     if x0p<x0N:
        deltax = (d-l1-l2)*math.cos(theta)
     elif x0p>x0N:
        deltax = -(d-l1-l2)*math.cos(theta)

     Dpp,Fpp =  -B*(deltay+y0p)-A*(deltax+x0p), -C*(deltay+y0p)-B*(deltax+x0p)  
     x0pp,y0pp = (C*Dpp-B*Fpp)/(B**2-A*C) ,(A*Fpp-B*Dpp)/(B**2-A*C)
     Metxp = x0pp+x0
     Metyp = y0pp+y0
         
     if Parameter == 'DarkPt': #Cambiar
        return abs(d-l1-l2) #abs(d-l1-l2-sqrt((Metxp-self.metX)**2+(Metyp-self.metY)**2))
     elif Parameter == 'ttbarEllipse':
        Gammap = np.outer([Metxp,Metyp,0],[0,0,1])-n.UnitCircle() #np.array([[A,B,Dpp],[B,C,Fpp],[Dpp,Fpp,Gpp]]) 
        n_p = Gammap.T.dot(self.N_).dot(Gammap)
        self.plotEllipse(n_p,'green')   #return n_p
     else:
        print 'Wrong Input Name'
        return -1


 
########################################################
#nameOfFile = sys.argv[1]
#
#f = r.TFile.Open(nameOfFile, "read")
#
##Reads the TTree t
#eventcounter = 0
#noSolution = 0
#h_overlap=r.TH1F('Overlap ttbar','Overlap ttbar',200,0,6)
#for event in f.t:
#
#     #if eventcounter != 0:
#       # eventcounter = eventcounter + 1
#       # continue
#
#     print '---Comienzo de evento---'+str(eventcounter)
#     Tb=r.TLorentzVector()
#     Tb_=r.TLorentzVector()
#     Tlep=r.TLorentzVector()
#     Tlep_=r.TLorentzVector()
#     Tnu=r.TLorentzVector()
#     Tnu_=r.TLorentzVector()
#     TMET=r.TLorentzVector()
#     #Ellipse variation of met
#     for j in range(0,1):
#       #TLorentz Vectors of the particles in ttbar
#       Tb.SetPtEtaPhiM(event.ptb1,event.etab1,event.phib1, event.mb1)
#       Tb_.SetPtEtaPhiM(event.ptb2,event.etab2,event.phib2, event.mb2)
#       Tlep.SetPtEtaPhiM(event.ptlep1,event.etalep1,event.philep1, event.mlep1)
#       Tlep_.SetPtEtaPhiM(event.ptlep2,event.etalep2,event.philep2, event.mlep2)
#       Tnu.SetPtEtaPhiM(event.ptnu1, event.etanu1, event.phinu1, event.mnu1)
#       Tnu_.SetPtEtaPhiM(event.ptnu2, event.etanu2, event.phinu2, event.mnu2)
#       TMET.SetPtEtaPhiM(event.ptMET,event.etaMET,event.phiMET,event.mMET)
#       mW=(Tnu+Tlep_).M()
#       mW_=(Tnu_+Tlep).M()
#       mTOP=(Tnu_+Tlep+Tb).M()
#       mTOP_=(Tnu+Tlep_+Tb_).M()  
#       try:
#         nuSol=solveNeutrino(Tb,Tb_,Tlep,Tlep_,Tnu,Tnu_,TMET,mW,mW_,mTOP,mTOP_)    
#         #Plot the line that passes through the ellipse center
#         #m,b=nuSol.ellipseSeparation(nuSol.N,nuSol.n_,'LineParameters')
#         #x=np.r_[-330:0]
#         #plt.plot(x,m*x+b);
#         #plt.show()
#         #nuSol.plotEllipse(nuSol.N,'r')
#         #nuSol.plotEllipse(nuSol.n_,'b')
#         overlaping= nuSol.overlapingFactor(nuSol.N,nuSol.n_)  
#         h_overlap.Fill(overlaping)
          #print nuSol.N_
          #print nuSol.n_
          #print TMET.Px(),TMET.Py()
#       except LinAlgError :
#        noSolution = noSolution +1
#         print 'No hay solucion'+ str(noSolution)
#         continue
#     print '-------Fin de evento------' 
#     #plt.savefig('Elipsestt/Elipse'+str(eventcounter)+'.png')
#     #plt.savefig('Elipsestt/Elipse'+str(eventcounter)+'.png')
#     #plt.clf()
#     eventcounter+=1
     
#scale=1./h_overlap.Integral()
#canvas=r.TCanvas('Overlap ttbar','Overlaping Factor ttbar')
#canvas.cd()
#h_overlap.Scale(scale)
#h_overlap.Draw()
#h_overlap.GetXaxis().SetTitle('R')
#canvas.SaveAs('Overlapingttbar.png') 

