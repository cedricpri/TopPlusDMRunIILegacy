import ROOT as r

#massPoints = ["scalar100", "scalar500", "pseudo100", "pseudo500"]
massPoints = ["scalar100"]

for massPoint in massPoints:
    variables = ["ST_BDT_output_" + massPoint.replace("pseudo", "pseudoscalar") + "_customBinsAttempt3", "TTbar_BDT_output_" + massPoint.replace("pseudo", "pseudoscalar") + "_customBinsAttempt3", "METcorrected_pt", "mt2ll"]
    #variable = "METcorrected_pt"
    for variable in variables:
        variableShort = variable.split("_")[0]

        inputDir = "/afs/cern.ch/user/c/cprieels/work/public/Latinos/TopPlusDMRunIILegacy/Luca/CMSSW_10_2_5/src/PlotsConfigurations/Configurations/TTDM/Datacards/"
        inputFile = "2016/SmearSR-ttDM-" + massPoint + "/" + massPoint + "/topCR_ll/" + variable + "/shapes/histos_topCR_ll.root"

        #processes = ["tDM-" + massPoint, "STtW", "DY"]
        processes = ["ttDM-" + massPoint, "ttbar", "DY", "STtW", "ttZ"]
        #processes = ["ttbar"]
        #systematics = ["CMS_MET_2016", "CMS_JES_2016"]
        systematics = ["CMS_pileup"]

        fileOpened = r.TFile.Open(inputDir + inputFile)

        for process in processes:
            for systematic in systematics:
                nominal = fileOpened.Get("histo_" + process)
                up = fileOpened.Get("histo_" + process + "_" + systematic + "Up")
                down = fileOpened.Get("histo_" + process + "_" + systematic + "Down")

                canvas = r.TCanvas('c_' + process + "_" + variableShort + "_" + systematic + "_" + massPoint, 'c_' + process + variableShort + "_" + systematic + "_" + massPoint)
                canvas.SetGrid()
                canvas.cd()

                pad = r.TPad('p_' + process + "_" + variableShort + "_" + systematic + "_" + massPoint, 'p_' + process + variableShort + "_" + systematic + "_" + massPoint, 0, 0.3, 1, 1.0)
                pad.SetGrid()
                pad.Draw()
                pad.cd()
            
                nominal.SetLineWidth(2)
                nominal.SetLineColor(r.kBlack)
                #nominal.Scale(1./nominal.Integral())
            
                up.SetLineWidth(2)
                up.SetLineColor(r.kGreen)
                #up.Scale(1./up.Integral())
                down.SetLineWidth(2)
                down.SetLineColor(r.kRed)
                #down.Scale(1./down.Integral())

                nominal.Draw()
                up.Draw("SAME")
                down.Draw("SAME")
                
                legend = r.TLegend(0.1,0.7,0.48,0.9)
                legend.AddEntry(nominal, "Nominal")
                legend.AddEntry(up, "Up")
                legend.AddEntry(down, "Down")

                #Ratio plot
                canvas.cd()
                
                padratio = r.TPad('pr_' + process + "_" + variableShort + "_" + systematic + "_" + massPoint, 'pr_' + process + variableShort + "_" + systematic + "_" + massPoint, 0, 0.05, 1, 0.3)
                padratio.SetGrid()
                padratio.Draw()
                padratio.cd()
                
                nominalCopy = nominal.Clone()
                upCopy = up.Clone()
                downCopy = down.Clone()
                
                upCopy.Divide(nominalCopy)
                upCopy.SetLineWidth(2)
                upCopy.SetLineColor(r.kGreen)
                upCopy.SetStats(0)
                upCopy.SetTitle("")
                upCopy.Draw()
                upCopy.GetYaxis().SetRangeUser(0, 2.0)

                downCopy.Divide(nominalCopy.Clone())
                downCopy.SetLineWidth(2)
                downCopy.SetLineColor(r.kRed)
                downCopy.SetStats(0)
                downCopy.SetTitle("")
                downCopy.Draw("SAME")
                downCopy.GetYaxis().SetRangeUser(0, 2.0)

                canvas.SaveAs("systematic_" + variableShort + "_" + process + "_" + systematic + "_" + massPoint + ".png")
fileOpened.Close()
