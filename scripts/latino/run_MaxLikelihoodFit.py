#!/usr/bin/env python
import timeit
import optparse
import sys  
import os
import LatinoAnalysis.Gardener.hwwtools as hwwtools

PWD     = os.getenv('PWD')
CMSSW_v = 'CMSSW_'+PWD.split('CMSSW_')[1].split('/')[0]
COMBINE = PWD.split('CMSSW_')[0]+CMSSW_v
if os.path.isdir(COMBINE) is False: COMBINE=PWD.split('CMSSW_')[0]+'CMSSW_8_1_0/src/'

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--outputDirDatacard' , dest='outputDirDatacard' , help='output directory for datacards'           , default='Datacards')
    parser.add_option('--outputDirMaxFit'   , dest='outputDirMaxFit'   , help='output directory for fit '                , default='MaxLikelihoodFits')
    parser.add_option('--combineLocation'   , dest='combineLocation'   , help='Combine CMSSW Directory'                  , default=COMBINE)
    parser.add_option('--tag'               , dest='tag'               , help='Tag used for the tag file name'           , default='')
    parser.add_option('--masspoint'         , dest='masspoint'         , help='Mass point to be fitted'                  , default='')
    parser.add_option('--years'             , dest='years'             , help='Year to be processed. Default: all'       , default='all')
    parser.add_option('--fileset'           , dest='fileset'           , help='Fileset with the shapes'                  , default='')
    parser.add_option('--skipBOnlyFit'      , dest='skipBOnlyFit'      , help='Skip B only fit'                          , default=False, action='store_true')
    parser.add_option('--saveCovMatrix'     , dest='saveCovMatrix'     , help='Save overall covariance matrix'           , default=False, action='store_true')
    parser.add_option('--nododatacards'     , dest='nododatacards'     , help='Do not make datacaards'                   , default=False, action='store_true')
 
    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    if opt.years=='-1' or opt.years=='all':
        yearset='2016-2017-2018'
    elif opt.years=='0':
        yearset='2016'
    elif opt.years=='1':
        yearset='2017'
    elif opt.years=='2':
        yearset='2018'
    else:
        yearset=opt.years

    opt.sigset = opt.masspoint

    if 'SM-' not in opt.fileset:
        opt.fileset = 'SM-' + opt.fileset

    if not opt.nododatacards:
        os.system('./run_mkDatacards.py '+yearset+' '+opt.tag+' '+opt.masspoint+' '+opt.fileset)

    tag = opt.tag
    opt.tag = yearset.split('-')[0] + opt.tag

    samples = { }
    variables = { }
    cuts = { }

    exec(open(opt.samplesFile).read())
    exec(open(opt.variablesFile).read())
    exec(open(opt.cutsFile).read())

    maxFitCommand = 'cd '+COMBINE+' ;  eval `scramv1 runtime -sh` ; cd - ; combineCards.py '

    for year in yearset.split('-'):
        for cut in cuts:
            for variable in variables:
                datacardName = PWD+'/'+opt.outputDirDatacard+'/'+year+'/'+tag+'/'+opt.masspoint+'/'+cut+'/'+variable+'/datacard.txt'
                if os.path.isfile(datacardName):
                    maxFitCommand += cut+'_'+year+'='+datacardName + ' ' 
                else:
                   print 'Missing datacard:', datacardName 
                   exit()

    outputDir = PWD+'/'+opt.outputDirMaxFit+'/'+yearset+'/'+tag+'/'+opt.masspoint+'/'    
    os.system('mkdir -p '+outputDir)
            
    maxFitCommand += ' > ' + outputDir+'datacardFinal.txt ; '

    maxFitCommand += 'cd ' + outputDir + ' ; '

    skipBOnlyFit = '--skipBOnlyFit' if opt.skipBOnlyFit else ''
    saveCovMatrix = ' --saveOverallShapes' if opt.saveCovMatrix else ''
    maxFitCommand += 'combine -M FitDiagnostics --saveShapes --saveWithUncertainties ' + skipBOnlyFit + saveCovMatrix + ' -n ' + tag + ' ' + outputDir+'datacardFinal.txt'
 
    os.system(maxFitCommand)

    for year in yearset.split('-'):
        os.system('rm -r '+opt.outputDirDatacard+'/'+year+'/'+tag+'/'+opt.masspoint) 
   
