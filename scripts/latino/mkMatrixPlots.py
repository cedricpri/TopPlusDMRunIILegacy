#!/usr/bin/env python

import json
import sys
import ROOT
import optparse
import LatinoAnalysis.Gardener.hwwtools as hwwtools
import logging
import os
import math

def makeMatrixPlot(outputHisto, outputFile, outputDir) :
        
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetPaintTextFormat("1.3f")
    ROOT.gStyle.SetPalette(1)

    canvas = ROOT.TCanvas("canvas", "", 550, 550)
    
    canvas.Divide(1, 1)
    canvas.SetFillColor(10)
    canvas.SetBorderMode(0)
    canvas.SetBorderSize(2)
    canvas.SetFrameFillColor(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)

    pad = canvas.GetPad(1)

    #pad.SetGridx()
    #pad.SetGridy()
    if "Cov" in outputHisto.GetName() :
        pad.SetLogz()
    pad.SetLeftMargin(0.13);
    pad.SetRightMargin(0.13);
    pad.SetTopMargin(0.08);
    pad.SetBottomMargin(0.13);

    pad.cd()

    if 'Covariance' in outputFile :
        outputHisto.SetMinimum(0.01);
    #outputHisto.SetMaximum(+1.);

    outputHisto.GetXaxis().SetLabelFont(42)
    outputHisto.GetXaxis().SetLabelSize(0.02)
    #outputHisto.GetXaxis().SetLabelOffset(1.)
    outputHisto.GetYaxis().SetLabelFont(42)
    outputHisto.GetYaxis().SetLabelSize(0.02)
    #outputHisto.GetYaxis().SetLabelOffset(1.)

    outputHisto.GetXaxis().SetTitle("")
    outputHisto.GetYaxis().SetTitle("")

    outputHisto.Draw("colz")

    scaleLeg = outputHisto.GetNbinsX()/(6.*7.*2.)

    T1 = ROOT.TLatex(scaleLeg*0.220, scaleLeg*86., "CMS")
    T1.SetTextAlign(11)
    T1.SetTextFont(61)
    T1.SetTextSize(0.042)
    T1.Draw()

    T2 = ROOT.TLatex(scaleLeg*11., scaleLeg*86., "Supplementary")
    T2.SetTextAlign(11)
    T2.SetTextFont(52)
    T2.SetTextSize(0.034)
    T2.Draw()
    T1.Draw()

    arXiv = "" #"arXiv"
    T4 = ROOT.TLatex(scaleLeg*62., scaleLeg*86., arXiv)
    T4.SetTextAlign(31)
    T4.SetTextFont(42)
    T4.SetTextSize(0.032)
    T4.Draw()
    
    lumi = 0
    if '2016' in outputDir: lumi += 35.9
    if '2017' in outputDir: lumi += 41.5
    if '2018' in outputDir: lumi += 59.7

    #T3 = ROOT.TLatex(scaleLeg*84., scaleLeg*86., str(lumi)+' fb^{-1} (13 TeV)')
    T3 = ROOT.TLatex(scaleLeg*89., scaleLeg*86., str(lumi)+' fb^{-1} (13 TeV)')
    T3.SetTextAlign(31)
    T3.SetTextFont(42)
    T3.SetTextSize(0.032)
    T3.Draw()

    canvas.Print(outputDir + "/" + outputFile + ".pdf")
    canvas.Print(outputDir + "/" + outputFile + ".root")

def convertTitle(yTitle) :

    ptmissBin = [ '_SR1', '_SR2', '_SR3', '_SR4' ]
    
    for ptmb in ptmissBin :
        if ptmb in yTitle :
    
            yTitle = yTitle.replace(ptmb, '')
            yTitle = ptmb.replace('_', '') + '_' + yTitle

    yTitle = yTitle.replace("_NoTag", "_jets")
    yTitle = yTitle.replace("_Veto",  "_0tag")
    yTitle = yTitle.replace("_Tag",   "_tags")
    yTitle = yTitle.replace("_NoJet", "_0jet")

    yTitle = yTitle.replace("_sf", "_SF")
    yTitle = yTitle.replace("_em", "_DF")

    return yTitle

def isRegionToRemove(label, regionsToRemove) :

    for region in regionsToRemove.split(','):
        if region in label:
           return True

    return False 

def makeHistoCopy(inputHisto, regionsToRemove, fillContent) :

    nBinsX = 0
    for xb in range(inputHisto.GetNbinsX()) :
        if not isRegionToRemove(inputHisto.GetXaxis().GetBinLabel(xb+1), regionsToRemove) :
            nBinsX += 1

    outputHisto = ROOT.TH2D("CovarianceMatrix", "", nBinsX, 0., nBinsX, nBinsX, 0., nBinsX)

    nBinsX = 0
    for xb in range(inputHisto.GetNbinsX()) :
        if not isRegionToRemove(inputHisto.GetXaxis().GetBinLabel(xb+1), regionsToRemove) :

            nBinsY = 0
            for yb in range(inputHisto.GetNbinsY()) :
                if not isRegionToRemove(inputHisto.GetYaxis().GetBinLabel(yb+1), regionsToRemove) :

                    if fillContent:
                        outputHisto.SetBinContent(nBinsX+1, nBinsY+1, inputHisto.GetBinContent(xb+1, yb+1))
                                                  
                    if nBinsX==0 :
                        outputHisto.GetYaxis().SetBinLabel(nBinsY+1, convertTitle(inputHisto.GetYaxis().GetBinLabel(yb+1)))

                    nBinsY += 1

            outputHisto.GetXaxis().SetBinLabel(nBinsX+1, convertTitle(inputHisto.GetXaxis().GetBinLabel(xb+1)))
            nBinsX += 1
                    
    return outputHisto

##Main body of the analysis
if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--verbose'        , dest='verbose'        , help='verbose'        , default=0                     , type='int'   )
    parser.add_option('--inputDir'       , dest='inputDir'       , help='inputDir'       , default='./MaxLikelihoodFits' , type='string')
    parser.add_option('--years'          , dest='years'          , help='years'          , default='-1'                  , type='string')
    parser.add_option('--tag'            , dest='tag'            , help='tag'            , default='SR'                  , type='string')
    parser.add_option('--inputFile'      , dest='inputFile'      , help='inputFile'      , default='fitDiagnostics'      , type='string')
    parser.add_option('--histogramDir'   , dest='histogramDir'   , help='histogramDir'   , default='shapes_fit_b'        , type='string')
    parser.add_option('--covarianceHisto', dest='covarianceHisto', help='covarianceHisto', default='overall_total_covar' , type='string')
    parser.add_option('--saveCovariance' , dest='saveCovariance' , help='saveCovariance' , default=0                     , type='int'   )
    parser.add_option('--removeCRs'      , dest='removeCRs'      , help='removeCRs'      , default='CR'                  , type='string')
    parser.add_option('--outputDir'      , dest='outputDir'      , help='outputDir'      , default='./Plots/'            , type='string')
    parser.add_option('--masspoint'      , dest='masspoint'      , help='masspoint'      , default=''                    , type='string')

    (opt, args) = parser.parse_args()

    if opt.masspoint=='':
        print 'Please, choose a signal mass point'
        exit()

    #print 'Convert covariance to correlation matrix for ',opt.masspoint 
 
    if opt.years=='-1':
        year = '2016-2017-2018'
    elif opt.years=='0':
        year = '2016'
    elif opt.years=='1':
        year = '2017'
    elif opt.years=='2':
        year = '2018' 
    else:
        year = opt.years

    inputDir = opt.inputDir + '/' + year + '/' + opt.tag + '/' + opt.masspoint + '/'
    outputDir = opt.outputDir + '/' + year + '/Matrix/' 
    os.system('mkdir -p '+outputDir)

    fileIn = ROOT.TFile.Open(inputDir + opt.inputFile + opt.tag + '.root', 'READ')

    covariance = fileIn.Get(opt.histogramDir + '/' + opt.covarianceHisto)
    covariance.SetDirectory(0)
    fileIn.Close()

    covariance = makeHistoCopy(covariance, opt.removeCRs, True)

    if opt.saveCovariance :

        covariance.SetName('CovarianceMatrix')
        makeMatrixPlot(covariance, 'CovarianceMatrix_' + opt.masspoint, outputDir)

    CovarianceMatrix = ROOT.TMatrixD(covariance.GetNbinsX(), covariance.GetNbinsY())
    DiagonalMatrix = ROOT.TMatrixD(covariance.GetNbinsX(), covariance.GetNbinsY())
    
    for xb in range(covariance.GetNbinsX()) :
        for yb in range(covariance.GetNbinsY()) :

            CovarianceMatrix[xb][yb] = covariance.GetBinContent(xb+1, yb+1)

            if xb==yb :
                DiagonalMatrix[xb][yb] = 1./math.sqrt(covariance.GetBinContent(xb+1, yb+1))
            else :
                DiagonalMatrix[xb][yb] = 0.

    AuxiliaryMatrix = ROOT.TMatrixD(covariance.GetNbinsX(), covariance.GetNbinsY())
    AuxiliaryMatrix.Mult(DiagonalMatrix, CovarianceMatrix)

    CorrelationMatrix = ROOT.TMatrixD(covariance.GetNbinsX(), covariance.GetNbinsY())
    CorrelationMatrix.Mult(AuxiliaryMatrix, DiagonalMatrix)
    
    correlation = makeHistoCopy(covariance, 'XXX', False)
    correlation.SetName("CorrelationMatrix")
    
    for xb in range(covariance.GetNbinsX()) :
        for yb in range(covariance.GetNbinsY()) :

            correlation.SetBinContent(xb+1, yb+1, CorrelationMatrix(xb, yb))

    outputFileName = 'CorrelationMatrix' + opt.histogramDir.replace('shapes', '') + '_' + opt.tag
    if 'fit_s' in opt.histogramDir: outputFileName += '_' + opt.masspoint 
    makeMatrixPlot(correlation, outputFileName, outputDir)

