import ROOT

shape = ROOT.TFile.Open("Shapes/2018/GroupedBkg-SmearSR-ttDM-scalar500/plots_GroupedBkg-SmearSR-ttDM-scalar500_SM-ttDM-scalar500.root", "UPDATE")
shape.cd("topCR_ll/TTbar_BDT_output_scalar500_customBinsAttempt2/")

h_ttbar = shape.Get("topCR_ll/TTbar_BDT_output_scalar500_customBinsAttempt2/histo_ttbar")
h_DY = shape.Get("topCR_ll/TTbar_BDT_output_scalar500_customBinsAttempt2/histo_DY")
h_Others = shape.Get("topCR_ll/TTbar_BDT_output_scalar500_customBinsAttempt2/histo_Others")
h_STtW = shape.Get("topCR_ll/TTbar_BDT_output_scalar500_customBinsAttempt2/histo_STtW")
h_data = shape.Get("topCR_ll/TTbar_BDT_output_scalar500_customBinsAttempt2/histo_DATA")

h_data.SetBinContent(10, h_ttbar.GetBinContent(10) + h_STtW.GetBinContent(10) + h_DY.GetBinContent(10) + h_Others.GetBinContent(10))
h_data.Write()
shape.Close()
