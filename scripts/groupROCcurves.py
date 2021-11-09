import ROOT as r

inputDir = "../neuralNetwork/2018/"
massPoints = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
#massPoints = ["step1", "step2", "step3", "step4", "step5"]#, "500_training4", "500_training5", "500_training6", "500_training7", "500_training8", "500_training9", "500_training10", "500_training11"]
mediator = "scalar"
signal="TTbar"
colors = [636, 635, 634, 633, 632, 807, 802, 801, 800, 798]

hists = []
for i, massPoint in enumerate(massPoints):
    #tmvaFile = r.TFile.Open(inputDir + mediator + "_LO_Mchi_1_Mphi_" + str(massPoint) + "/training/TMVA.root")
    tmvaFile = r.TFile.Open(inputDir + "DMpseudoscalar_Dilepton_top_tWChan_Mchi1_Mphi" + str(massPoint) + "_" + signal + "/training/TMVA.root")
 
    hist = tmvaFile.Get("dataset/Method_PyKeras/PyKeras/MVA_PyKeras_rejBvsS")
    hist.SetDirectory(0)
    hist.SetStats(0)
    hist.SetLineColor(colors[i])
    #hist.SetLineWidth(2)
    hist.SetTitle("ROC curves for several trainings")
    hists.append(hist)

    tmvaFile.Close()

canvas = r.TCanvas('c1', 'c1')
canvas.SetGrid()
canvas.cd()

legend = r.TLegend(0.15, 0.15, 0.36, 0.5)

for i, hist in enumerate(hists):
    hist.Draw('same')

    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetTextAlign(12)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)
    legend.AddEntry(hist, mediator + str(massPoints[i]).replace("step", "set"), "l")

legend.Draw()
canvas.SaveAs("groupedROC_" + mediator.replace("pseudoscalar", "pseudo") + "_" + signal + ".png")
