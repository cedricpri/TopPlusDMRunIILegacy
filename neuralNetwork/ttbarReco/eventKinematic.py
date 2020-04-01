import ROOT as r
from ttbarReco import ttbar #ttbar reconstruction

import math, copy
import numpy as np
LinAlgError = np.linalg.linalg.LinAlgError

class EventKinematic():

    def __init__ (self, Tlep1, Tlep2, Tb1, Tb2, Tnu1, Tnu2, TMET):
        self.Tlep1 = Tlep1
        self.Tlep2 = Tlep2
        self.Tb1 = Tb1
        self.Tb2 = Tb2
        self.Tnu1 = Tnu1
        self.Tnu2 = Tnu2
        self.TMET = TMET
        
        #"Constant" variables, only changed by smearing
        self.mW1 = 80.379
        self.mW2 = 80.379
        self.mt1 = 173.0
        self.mt2 = 173.0

        #Computed properties
        #self.truemlb = r.TH1F(r.TFile("mlb.root", "r").Get("mlb")) #Get the generation mlb shape, used to compute the weights and found in mlb.root after running the generateMLB.py script

        #Discriminating variables
        self.overlapping_factor = -99.0
        self.dark_pt = -99.0
        self.weight = -99.0 #Default value if the reco does not work

        self.nuSol = None #Place to keep the optimal nuSol object

    def runSmearingOnce(self, mlbHist):
        """
        Run the smearinby modifying the lepton, jets, masses, angles and MET.
        """
        
        rand = r.TRandom3()
        
        #Update the jets
        OldTb1, OldTb2 = self.Tb1, self.Tb2

        Tb1Uncertainty = rand.Gaus(0, 0.3) * self.Tb1.E() 
        Tb2Uncertainty = rand.Gaus(0, 0.3) * self.Tb2.E()
            
        try:
            ptCorrection1 = math.sqrt((self.Tb1.E() + Tb1Uncertainty)**2 - self.Tb1.M()**2)/self.Tb1.P()
            ptCorrection2 = math.sqrt((self.Tb2.E() + Tb2Uncertainty)**2 - self.Tb2.M()**2)/self.Tb2.P()
        except:
            ptCorrection1 = 1.0
            ptCorrection2 = 1.0

        self.Tb1.SetPtEtaPhiM(self.Tb1.Pt()*ptCorrection1, self.Tb1.Eta(), self.Tb1.Phi(), self.Tb1.M())
        self.Tb2.SetPtEtaPhiM(self.Tb2.Pt()*ptCorrection2, self.Tb2.Eta(), self.Tb2.Phi(), self.Tb2.M())
        
        #TOCHECK: Update the leptons as wel?
        #TODO: Perform the angular smearing
            
        #Update the MET
        deltaP1 = r.TLorentzVector(self.Tb1.Px() - OldTb1.Px(), self.Tb1.Py() - OldTb1.Py(), 0, 0)
        deltaP2 = r.TLorentzVector(self.Tb2.Px() - OldTb2.Px(), self.Tb2.Py() - OldTb2.Py(), 0, 0)
        self.TMET = self.TMET + deltaP1 + deltaP2

        #Update the W mass
        self.mW1 = rand.BreitWigner(80.379, 2.085)
        self.mW2 = rand.BreitWigner(80.379, 2.085)

        self.runReco()
        self.findBestSolution(mlbHist)

        return self

    def runReco(self):
        """
        Function to actually run the top reconstruction using a EventKinematic() object.
        """

        try:
            nuSol = ttbar.solveNeutrino(self.Tb1, self.Tb2, self.Tlep1, self.Tlep2, self.Tnu1, self.Tnu2, self.TMET, self.mW1, self.mW2, self.mt1, self.mt2)
        except:
            #print("An error occured when performing the reconstruction")
            nuSol = None

        self.nuSol = nuSol
        return nuSol

    def findBestSolution(self, mlbHist):
        """
        Find the best solution (minimal invariant mass) from eventual multiple ellipses intersections
        """
    
        minInvMass = 9999999.

        Tnu1 = r.TLorentzVector()
        Tnu2 = r.TLorentzVector()
        bestSol = None

        if self.nuSol is not None:
            try:
                for s, possibleSolution in enumerate(self.nuSol.solution):
                    #TOCHECK: value of the total momentum (=energy) of a neutrino
                    #possibleSolution[0] is the neutrino, possibleSolution[0][0] its momentum along the x-axis
                    Tnu1.SetPxPyPzE(possibleSolution[0][0], possibleSolution[0][1], possibleSolution[0][2], math.sqrt(possibleSolution[0][0]**2 + possibleSolution[0][1]**2 + possibleSolution[0][2]**2)) 
                    Tnu2.SetPxPyPzE(possibleSolution[1][0], possibleSolution[1][1], possibleSolution[1][2], math.sqrt(possibleSolution[1][0]**2 + possibleSolution[1][1]**2 + possibleSolution[1][2]**2)) 

                    invMass = (Tnu1 + self.Tlep1 + self.Tb1).M() + (Tnu2 + self.Tlep2 + self.Tb2).M()
                    if invMass < minInvMass:
                        minInvMass = minInvMass
                        self.Tnu1 = Tnu1
                        self.Tnu2 = Tnu2
            except:
                pass

        self.setWeight(mlbHist)
        self.setDiscriminatingVariables()

        return [Tnu1, Tnu2]
            
    def setWeight(self, mlbHist):
        """
        Set the weight associated to a given (smeared) object.
        """
        
        weight = -99.0
        if self.nuSol is not None:
            try:
                mlb = (self.nuSol.mu1 + self.nuSol.b1).M()
                mlb_ = (self.nuSol.mu2 + self.nuSol.b2).M()

                #Compare these values with the one obtained from generation
                truemlb = mlbHist.GetBinContent(mlbHist.FindBin(mlb))
                truemlb_ = mlbHist.GetBinContent(mlbHist.FindBin(mlb_))
                weight = truemlb * truemlb_
            except:
                weight = -9.0

            self.weight = weight
        return weight

    def setDiscriminatingVariables(self):
        """
        Set the dark pt and the overlapping factor from a nuSol object.
        """

        overlapping_factor = -99.0
        dark_pt = -99.0
        if self.nuSol is not None:
            try:
                overlapping_factor = self.nuSol.overlapingFactor(self.nuSol.N, self.nuSol.n_)
                #if self.nuSol.overlapingFactor(self.nuSol.N, self.nuSol.n_) < 0.2: #TOCHECK: put back this cut and tweak it?
                dark_pt = self.nuSol.darkPt('DarkPt')
            except:
                overlapping_factor = -9.0
                dark_pt = -9.0

            self.overlapping_factor = overlapping_factor
            self.dark_pt = dark_pt
        return [overlapping_factor, dark_pt]
