#!/usr/bin/env python

import optparse
import json
import ROOT
import LatinoAnalysis.Gardener.hwwtools as hwwtools
import os.path

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--tag'            , dest='tag'            , help='Tag used for the shape file name'           , default=None)
    parser.add_option('--years'          , dest='years'          , help='Years'                                      , default='all')
    parser.add_option('--sigset'         , dest='sigset'         , help='Signal samples [SM]'                        , default='SM')
    parser.add_option('--outputDir'      , dest='outputDir'      , help='output directory'                           , default='./Shapes')
    parser.add_option('--saveNuisances'  , dest='saveNuisances'  , help='save file with merged nuisances'            , default=False, action='store_true')
    parser.add_option('--nuisancesFile'  , dest='nuisancesFile'  , help='file with nuisances configurations'         , default=None)
    parser.add_option('--verbose'        , dest='verbose'        , help='activate print for debugging'               , default=False, action='store_true')
    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()
   
    if opt.years=='-1' or opt.years.lower()=='all':
        years = [ '2016', '2017', '2018' ]
    elif opt.years=='0':
        years = [ '2016' ]
    elif opt.years=='1':
        years = [ '2017' ]
    elif opt.years=='2':
        years = [ '2018' ]
    else:
        years = opt.years.split('-')
   
    if len(years)==1:
        print 'Nothing to do with one year (for the moment?)'
        exit()

    localnuisancesFile = opt.nuisancesFile.replace('.py', '_'+'-'.join(years)+'_'+opt.tag+'_'+opt.sigset+'.py')

    localtag = opt.tag
    opt.tag = years[0] + localtag
 
    samples = {}
    if os.path.exists(opt.samplesFile) :
      handle = open(opt.samplesFile,'r')
      exec(handle)
      handle.close()

    variables = {}
    if os.path.exists(opt.variablesFile) :
      handle = open(opt.variablesFile,'r')
      exec(handle)
      handle.close()

    cuts = {}
    if os.path.exists(opt.cutsFile) :
      handle = open(opt.cutsFile,'r')
      exec(handle)
      handle.close()

    allnuisances = {}
    if os.path.exists(localnuisancesFile) :
        nuisances = {}
        handle = open(localnuisancesFile,'r')
        exec(handle)
        handle.close()
        allnuisances = nuisances
    else:
        for localyear in years:
           nuisances = {}
           opt.tag = localyear + localtag
           handle = open(opt.nuisancesFile,'r')
           exec(handle)
           handle.close()
           for nuisance in nuisances:
               if nuisance!='stat':
                   if nuisances[nuisance]['name'] not in allnuisances:
                       allnuisances[nuisances[nuisance]['name']] = nuisances[nuisance]
                   if 'type' in nuisances[nuisance] and nuisances[nuisance]['type']=='lnN':
                       allnuisances[nuisances[nuisance]['name']]['samples_'+localyear] = nuisances[nuisance]['samples']
               elif 'stat' not in allnuisances:
                   allnuisances['stat'] = nuisances[nuisance]

    outDirName = opt.outputDir + '/' + '-'.join(years) + '/' + localtag
    os.system ('mkdir -p ' + outDirName)

    outFileName = outDirName + '/plots_' + localtag + '_' + opt.sigset + '.root'
    outFile = ROOT.TFile.Open(outFileName, 'recreate') 

    inFiles = [ ]
    for year in years:
        inFileName = outFileName
        if year!='2017': inFileName = inFileName.replace('EENoiseDPhi', '')
        if year!='2018': inFileName = inFileName.replace('HEM', '')
        inFiles.append([ ROOT.TFile(inFileName.replace('-'.join(years), year), 'READ') , year ])

    for cutName in cuts:

        outFile.mkdir(cutName)

        for variableName in variables:
            if 'cuts' not in variables[variableName] or cutName in variables[variableName]['cuts']:

                folderName = cutName + '/' + variableName
                outFile.mkdir(folderName)

                if opt.verbose: print '################################', folderName

                inDirs = [ ] 
                for infile in inFiles:
                    inDirs.append([ infile[0].Get(folderName), infile[1] ])
 
                for sample in samples:
                    for nuisance in allnuisances:
                        if (sample in allnuisances[nuisance]['samples'] or nuisance=='stat') and ('cuts' not in allnuisances[nuisance] or cutName in allnuisances[nuisance]['cuts']):   

                            if nuisance!='stat' and 'type' not in allnuisances[nuisance]:
                                print 'Warning: nuisance without type -> ', nuisance
                                continue

                            elif nuisance!='stat':
                                if allnuisances[nuisance]['type']!='shape' and allnuisances[nuisance]['type']!='lnN':
                                    if allnuisances[nuisance]['type']!='rateParam':
                                        print 'Warning: unknown nuisance type -> ', allnuisances[nuisance]['type']
                                    continue

                            shapeName = 'histo_' + sample

                            for var in [ 'Up', 'Down' ]:

                                if nuisance=='stat' and var=='Down': continue 
                                 
                                shapeVar = shapeName if nuisance=='stat' else shapeName + '_' + allnuisances[nuisance]['name'] + var
                                 
                                for idir, indir in enumerate(inDirs):

                                    if indir[0].GetListOfKeys().Contains(shapeVar):
                                        tmpHisto = indir[0].Get(shapeVar)
                                        tmpHisto.SetDirectory(0)   

                                    else:
                                        tmpHisto = indir[0].Get(shapeName)
                                        tmpHisto.SetDirectory(0)

                                        if opt.verbose: print sample, nuisance,  var, tmpHisto.Integral()
                                        if allnuisances[nuisance]['type']=='lnN' or 'waslnN' in allnuisances[nuisance]:
                                            if 'samples_'+indir[1] in allnuisances[nuisance]:
                                                systNorm = float(allnuisances[nuisance]['samples_'+indir[1]][sample])
                                                if var=='Down':
                                                    systNorm = 2. - systNorm
                                                tmpHisto.Scale(systNorm)
                                                if opt.verbose: print 'samples_'+indir[1], tmpHisto.Integral()

                                    if idir==0:
                                        sumHisto = tmpHisto.Clone()
                                        sumHisto.SetDirectory(0)
                                        sumHisto.SetTitle(shapeVar)
                                        sumHisto.SetName(shapeVar)
                                    else:
                                        sumHisto.Add(tmpHisto)

                                outFile.cd(folderName)
                                sumHisto.Write()                         

                                # ...    
 
    if not os.path.exists(localnuisancesFile) and opt.saveNuisances:     
        with open(localnuisancesFile , 'w') as file:
            for nuisance in allnuisances:
                if allnuisances[nuisance]['type']=='lnN':
                    allnuisances[nuisance]['type'] = 'shape'
                    allnuisances[nuisance]['waslnN'] = True
                #file.write('nuisances[\''+nuisance+'\'] = '+json.dumps(allnuisances[nuisance])+'\n\n')
                file.write('nuisances[\''+nuisance+'\'] = '+repr(allnuisances[nuisance])+'\n\n')

