from optparse import OptionParser
import ROOT as ROOT
import math, os
from array import * 

def divideEfficiencies(eff1, eff2, plots2D, channel,year):
    #pt_bin = array('f', [20, 40, 60, 80, 120, 180, 240, 300])
    pt_bin = array('f', [25, 40, 60, 80, 100, 150, 200, 500])
    if plots2D:
        hist = ROOT.TH2F("h_SF_" + channel + "_" + year, "", len(pt_bin) - 1, pt_bin, len(pt_bin) - 1, pt_bin)
    else:
        hist = ROOT.TH1F("h_SF_" + channel + "_" + year, "", len(pt_bin) - 1, pt_bin)

    if plots2D:
        for i in range(len(pt_bin)):
            for j in range(len(pt_bin)):
                value1 = eff1.GetEfficiency(eff1.GetGlobalBin(i+1,j+1))
                value2 = eff2.GetEfficiency(eff2.GetGlobalBin(i+1,j+1))
                if value1 == 0 or value2 == 0:
                    continue
                value = value1/value2

                errorUp1 = eff1.GetEfficiencyErrorUp(eff1.GetGlobalBin(i+1,j+1))
                errorUp2 = eff2.GetEfficiencyErrorUp(eff2.GetGlobalBin(i+1,j+1))
                errorDown1 = eff1.GetEfficiencyErrorLow(eff1.GetGlobalBin(i+1,j+1))
                errorDown2 = eff2.GetEfficiencyErrorLow(eff2.GetGlobalBin(i+1,j+1))
                if(errorUp1 > errorDown1):
                    error1 = errorUp1
                else:
                    error1 = errorDown1

                if(errorUp2 > errorDown2):
                    error2 = errorUp2
                else:
                    error2 = errorDown2

                error = value * math.sqrt((error1/value1)**2 + (error2/value2)**2)
                hist.SetBinContent(i+1, j+1, value)
                hist.SetBinError(i+1, j+1, error)
    else:
        for i in range(len(pt_bin)):
            value1 = eff1.GetEfficiency(i+1)
            value2 = eff2.GetEfficiency(i+1)
            #print(i, value1, value2)
            value = value1/value2
        
            errorUp1 = eff1.GetEfficiencyErrorUp(i+1)
            errorUp2 = eff2.GetEfficiencyErrorUp(i+1)
            errorDown1 = eff1.GetEfficiencyErrorLow(i+1)
            errorDown2 = eff2.GetEfficiencyErrorLow(i+1)
            if(errorUp1 > errorDown1):
                error1 = errorUp1
            else:
                error1 = errorDown1
                
            if(errorUp2 > errorDown2):
                error2 = errorUp2
            else:
                error2 = errorDown2

            error = value * math.sqrt((error1/value1)**2 + (error2/value2)**2)
            hist.SetBinContent(i+1, value)
            hist.SetBinError(i+1, error)

    return hist

#------------------------------------- Main--------------------------------------------
if __name__ == '__main__':

    parser = OptionParser(usage="%prog --help")
    parser.add_option("-y","--year",       dest="year",        help="Year",            default='2016',                  type='string')
    parser.add_option("-t","--tag",        dest="tag",         help="Tag",             default='',                      type='string')
    parser.add_option("-l","--isLatino",   dest="isLatino",    help="isLatino?",       default=0,                       type=int)

    (options, args) = parser.parse_args()
    year = options.year
    tag = options.tag 
    isLatino = options.isLatino

    if isLatino == 1:
        suffix = "_latino"
    else:
        suffix = ""

    if tag == "":
        tag = year

    if tag != "":
        tag = "_" + tag

    plots2D = True
    try:
        os.remove("SF_" + options.year + options.tag + ".root")
    except:
        pass

    for channel in ["ee", "em", "mm"]:
        ###################################### Open file ##################################################
        fMC = ROOT.TFile("Efficiency_pt_" + channel + "_" + year + "_MC" + suffix + ".root")
        evMC = fMC.Get('Efficiency_' + channel + '_pt_' + year + "_MC" + suffix)
        fData = ROOT.TFile("Efficiency_pt_" + channel + "_" + year + tag + suffix + ".root")
        evData = fData.Get('Efficiency_' + channel + '_pt_' + year + tag + suffix)
        
        h_SF = divideEfficiencies(evData, evMC, plots2D, channel, options.year)
        
        ########################################## Drawing ###############################################
        can = ROOT.TCanvas("eff" + channel, "")
        can.cd()

        h_SF.SetTitle("Trigger SF (" + channel + " channel, " + year + ")")
        h_SF.GetZaxis().SetRangeUser(0.8, 1.05)
        h_SF.SetStats(False)
        if plots2D:
            h_SF.Draw("COLZ,TEXT,ERROR")
            ROOT.gPad.Update()
            ROOT.gStyle.SetPaintTextFormat("4.3f")
        else:
            h_SF.Draw()
        
        can.SaveAs("SF_pt_" + channel + "_" + year + tag + ".png")
        #can.SaveAs("SF_pt_" + channel + "_" + year + tag + ".root")

        ########################################## Write ###############################################
        outputFile = ROOT.TFile.Open("SF_" + options.year + options.tag + ".root", "UPDATE")
        evMC.Write()
        evData.Write()
        h_SF.Write()
        outputFile.Close()
