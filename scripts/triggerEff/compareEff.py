from optparse import OptionParser
import ROOT as ROOT
from array import * 


#------------------------------------- MAIN --------------------------------------------
if __name__ == '__main__':

    parser = OptionParser(usage="%prog --help")
    parser.add_option("-y","--year",       dest="year",        help="Year",            default='2016',                  type='string')
    parser.add_option("-t","--tag",        dest="tag",         help="Tag",             default='',                  type='string')

    (options, args) = parser.parse_args()
    year = options.year
    tag = options.tag 
    if tag == "":
        tag = year
    if tag != "":
        tag = "_" + tag

    for channel in ["ee", "em", "mm"]:
        ###################################### Open file ##################################################
        fSUSY = ROOT.TFile("Efficiency_pt_" + channel + "_" + year + tag + ".root")
        evSUSY = fSUSY.Get('Efficiency_' + channel + '_pt_' + year + tag)
        evSUSY.SetLineColor(632)
        
        fLatino = ROOT.TFile("Efficiency_pt_" + channel + "_" + year + tag + "_latino.root")
        evLatino = fLatino.Get('Efficiency_' + channel + '_pt_' + year + tag)
        evLatino.SetLineColor(636)
        
        ########################################## DrAwing ###############################################
        can = ROOT.TCanvas("eff" + channel, "")
        can.cd()

        evLatino.SetTitle("Trigger efficiences (" + channel + " channel, " + year + ")")
        evLatino.Draw()
        evSUSY.Draw("SAME")

        ROOT.gPad.Update()
        evSUSY.GetPaintedGraph().GetHistogram().SetLineColor(632)
        evSUSY.GetPaintedGraph().GetHistogram().SetMinimum(0)
        evSUSY.GetPaintedGraph().GetHistogram().SetMaximum(1.2)

        ROOT.gPad.Update()
        evLatino.GetPaintedGraph().GetHistogram().SetLineColor(632)
        evLatino.GetPaintedGraph().GetHistogram().SetMinimum(0)
        evLatino.GetPaintedGraph().GetHistogram().SetMaximum(1.2)

        legend = ROOT.TLegend(0.70, 0.20, 0.90, 0.30)
        legend.SetBorderSize(0)
        legend.SetFillColor(0)
        legend.SetTextAlign(12)
        legend.SetTextFont(42)
        legend.SetTextSize(0.035)
        legend.AddEntry(evLatino, "Old objects", "l")
        legend.AddEntry(evSUSY, "New objects", "l")
        legend.Draw("SAME")
        
        can.SaveAs("Efficiency_comparison_pt_" + channel + "_" + options.year + options.tag + ".png")

