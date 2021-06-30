from optparse import OptionParser
import ROOT as ROOT
from array import * 


#------------------------------------- MAIN --------------------------------------------
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

for channel in ["ee", "em", "mm"]:
    ###################################### Open file ##################################################
    fMC = ROOT.TFile("Efficiency_pt_" + channel + "_" + year + "_MC" + suffix + ".root")
    evMC = fMC.Get('Efficiency_' + channel + '_pt_' + year + "_MC" + suffix)
    fData = ROOT.TFile("Efficiency_pt_" + channel + "_" + year + tag + suffix + ".root")
    evData = fData.Get('Efficiency_' + channel + '_pt_' + year + tag + suffix)
        
    ########################################## Divide histograms ###############################################
    hDataNum = evData.GetCopyPassedHisto()
    hMCNum = evMC.GetCopyPassedHisto()
    hDataDen = evData.GetCopyTotalHisto()
    hMCDen = evMC.GetCopyTotalHisto()

    hDataNum.Divide(hDataDen)
    hMCNum.Divide(hMCDen)
    h_SF = hDataNum.Clone()
    h_SF.Sumw2()

    ########################################## DrAwing ###############################################
    can = ROOT.TCanvas("eff" + channel, "")
    can.cd()

    h_SF.SetTitle("Trigger SF (" + channel + " channel, " + year + ")")
    h_SF.Divide(hMCNum)
    h_SF.GetYaxis().SetRangeUser(0, 1.2)
    h_SF.Draw()

    can.SaveAs("Efficiency_comparison_pt_" + channel + "_" + year + tag + "_SF.png")
        
    del hDataNum
    del hDataDen
    del hMCNum
    del hMCDen
