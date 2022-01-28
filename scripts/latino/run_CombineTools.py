#!/usr/bin/env python
import timeit
import optparse
import LatinoAnalysis.Gardener.hwwtools as hwwtools

# functions used in everyday life ...
from LatinoAnalysis.Tools.commonTools import *

COMBINE = os.getenv('COMBINE')
PWD     = os.getenv('PWD')
CMSSW_v = PWD.split("CMSSW_")[1].split("/")[0]
if(COMBINE is None): 
    COMBINE = PWD.split('CMSSW_')[0]+'CMSSW_10_2_14/src/'#'CMSSW_8_1_0/src/' # So ugly ... :p
    if os.path.isdir(COMBINE) is False: COMBINE=PWD.split('CMSSW_')[0]+'CMSSW_8_1_0/src/'
 
#if(type(PWD) is None): PWD = " "

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--outputDirDatacard' , dest='outputDirDatacard' , help='output directory for datacards'           , default='Datacards')  
    parser.add_option('--outputDirLimit'    , dest='outputDirLimit'    , help='output directory for limits'              , default='Limits')   
    parser.add_option('--combineLocation'   , dest='combineLocation'   , help='Combine CMSSW Directory'                  , default=COMBINE)   
    parser.add_option('--combcfg'           , dest='combcfg'           , help='Combination dictionnary'                  , default='combineCards.py') 
    parser.add_option('--tag'               , dest='tag'               , help='Tag used for the tag file name'           , default='Test')
    parser.add_option('--sigset'            , dest='sigset'            , help='Tag used for the sigset file name'        , default="")
    parser.add_option('--years'             , dest='years'             , help='Year to be processed. Default: all'       , default="all")
    parser.add_option('--nomerge'           , dest='nomerge'           , help='Merge Datacards. Default=True'            , default=True, action='store_false')
    parser.add_option('--nolimits'          , dest='nolimits'          , help='Use higgs combine to calculate limits. Default=True' , default=True, action='store_false')
    parser.add_option('--limrun'            , dest='limrun'            , help='Type of limit to be calculated. Default=Blind'       , default='Blind')
    parser.add_option('--test'              , dest='test'              , help='Run on test mode'                         , default=False, action='store_true')
    parser.add_option('--sigmp'             , dest='signalMPcfg'       , help='Signal Mass Point cfg file'               , default='signalMassPoints.py')
    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    years = []
    if   opt.years == '2016':
        years = ["2016"]
    elif opt.years == '2017':
        years = ["2017"]
    elif opt.years == '-1'  :
        years = ["2016","2017","2018"]
        opt.years = "2016-2017-2018"
    else:
        years = opt.years.split('-')

    doTest   = opt.test
    doMerge  = opt.nomerge
    doLimits = opt.nolimits

    print "\n\t Optional arguments"
    print " tag                = ", opt.tag
    print " sigset             = ", opt.sigset
    print " Years              = ", years
    print " outputDirDatacard  = ", opt.outputDirDatacard
    print " outputDirLimit     = ", opt.outputDirLimit
    print " combineLocation    = ", opt.combineLocation  
    print " Combination Cfg    = ", opt.combcfg
    print " Run on test mode   = ", doTest
    print " Merge Datacards    = ", doMerge
    print " Calculate limits   = ", doLimits
    print "\n"
    
    if(doTest):
        print "On Test mode"
        opt.sigset = 'T2tt_mS-450_mX-350'

    opt.tag = opt.years+opt.tag

    # Check whether any of the input config files exist
    isVarsF = os.path.exists(opt.variablesFile)
    isSamsF = os.path.exists(opt.samplesFile)
    isCutsF = os.path.exists(opt.cutsFile)
    isSignF = os.path.exists(opt.signalMPcfg)

    fIsMiss = False
    fMiss   = ''
    allcfgs = {"Variables": isVarsF, "Samples": isSamsF,
               "Cuts"     : isCutsF, "Signal" : isSignF}

    for cfg_f in allcfgs:
        if allcfgs[cfg_f] is False:
            fMiss  += cfg_f
            fIsMiss = True

    #Stop the program if some file is missing
    if(fIsMiss is True):
        error = fMiss+"file Missing, check the input"
        raise NameError(error)

    #Generate dictionaries with variables and cuts
    variables = {}
    samples   = {}
    cuts      = {}
    if (isSamsF):  exec(open(opt.samplesFile).read())
    if (isVarsF):  exec(open(opt.variablesFile).read())
    if (isCutsF):  exec(open(opt.cutsFile).read())
    if (isCutsF):  exec(open(opt.cutsFile).read())
    if (isSignF):  exec(open(opt.signalMPcfg).read())
    
    opt.tag = opt.tag.replace(opt.years, '')

    #Loop over Signal mass points year cuts and variables, to get all Datacards
    cmsenv       = ' eval `scramv1 runtime -sh` '
    tagDC        = ''
    thereIsDC    = False
    doCombcmsenv = ''
    if CMSSW_v not in opt.combineLocation: doCombcmsenv='cd '+opt.combineLocation+ ';'+cmsenv+'; cd -; '

    

    for model in signalMassPoints:
        print "Model:", model,"\tSignal set", opt.sigset
        if model not in opt.sigset:  continue
        for massPoint in signalMassPoints[model]:
            dirDC      = ''
            dirDClocal = ''
            if not massPointInSignalSet(massPoint, opt.sigset): continue
            for year in years:
                mpLoc = PWD+'/'+opt.outputDirDatacard+'/'+year+'/'+opt.tag+'/'+massPoint
                if(os.path.exists(mpLoc) is not True):
                    print mpLoc
                    if(doTest is True): print "\n Folder for MassPoint", massPoint," does not exist:"
                    continue
                print "Mass Point:", massPoint,"\t Year:",  year
                for cut in cuts:
                    cutLoc = mpLoc+'/'+cut
                    #print os.path.exists(mpLoc), mpLoc, "cuts", cuts, variables
                    if(os.path.exists(cutLoc) is not True):
                        print "Folder for ", cut, "Does not exist"
                        continue
                    for variable in variables:
                        thisDC      = cutLoc+'/'+variable+"/datacard.txt"
                        tagDC       = cut #Could be changed to more complex in the future
                        dirDC      += tagDC+year+'='+thisDC+' '
                        dirDClocal += tagDC+year+'='+thisDC.split('/Datacards/')[1]+' '
                        
                        if(os.path.exists(thisDC) is True):
                            thereIsDC = True
#                            print "Datacard: ", thisDC, "dirDC="
                        else:
                            if(doTest):print "DC", thisDC, "does not exist"
            #Do not combine DC nor calculate limits if no DC is found
            mergeCommand = ''
            combCommand  = ''
            if(thereIsDC is False):
                print "there are no Datacards in the folder under the input parameters"
            else:
                #Actually merge the DC
                dcLoc   = PWD+'/'+opt.outputDirLimit+'/'+opt.years+'/'+opt.tag+'/'+massPoint
                finalDC = dcLoc+'/'+opt.tag+'.txt'
                os.system('mkdir -p '+dcLoc)                
                #print "FINAL DC:", finalDC
                if(doMerge is True and thereIsDC is True):
                    mergeCommand = opt.combcfg+' '+dirDC+">"+finalDC+";"
                    mergePrint   = ''
                    if(doTest): 
                        mergePrint   = mergeCommand
                    else: mergePrint = opt.combcfg+' '+dirDClocal+">"+finalDC+";"
                    print "Combining Datacards"
                    os.system(doCombcmsenv+mergeCommand)
                    print "FINAL DATACARD:\t:", finalDC
                else:
                    print "\n Data card merging option set to false: no DC combination is done"

                #Calculate the limits
                if(doLimits is True and thereIsDC is True):
                    outLoc = PWD+'/'+opt.outputDirLimit+'/'+opt.years+'/'+opt.tag+'/'+massPoint
                    os.system('mkdir -p '+outLoc)
                    
                    combCommand = 'cd '+outLoc+'; combine -M AsymptoticLimits --run '+opt.limrun.lower() +' ' +finalDC+' -n _'+opt.tag+'_'+opt.limrun
                    print "Sending combination", combCommand
                    os.system(doCombcmsenv+combCommand)
                else:
                    print "Limit option set to false: no limits were calculated"

                #os.system(doCombcmsenv+mergeCommand+combCommand)

        os.system('cd '+PWD+'; '+cmsenv)
