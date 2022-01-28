#!/usr/bin/env python
import timeit
import optparse
import json
import LatinoAnalysis.Gardener.hwwtools as hwwtools

# functions used in everyday life ...
from LatinoAnalysis.Tools.commonTools import *

expectedScaleWeights  =   9
expectedMinPdfWeights =  33

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--sigset'  , dest='sigset'  , help='Tag used for the sigset file name'  , default='Backgrounds')
    parser.add_option('--year'    , dest='year'    , help='Year to be processed. Default: all' , default='2016')
    parser.add_option('--verbose' , dest='verbose' , help='Verbose level. Default: 0'          , default=0)

    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    if opt.year=='0':
        year = '2016'
    elif opt.year=='1':
        year = '2017'
    elif opt.year=='2':
        year = '2018'
    else:
        year = opt.year
    
    opt.tag = year

    samples = { }

    exec(open(opt.samplesFile).read())

    theoryNormalizations = { }
             
    for sam_k, sam_v in samples.iteritems():

        if not sam_v['isSignal']: # Background samples

            if opt.verbose>=1:
                print 'Deriving theory normalizations for sample', sam_k

            qcdStatus = 3
            pdfStatus = 3

            chain = ROOT.TChain('Runs')

            for treeName in sam_v['name']:
                if 'rootd' not in treeName:
                    treeName = treeName.replace('###', '')
                chain.Add(treeName)
       
            genWeight = 0.
            qcdWeights, pdfWeights = [ ], [ ] 

            expectedPdfWeights = expectedMinPdfWeights
	    pdfWeightWarning = False
            lastnLHEPdfSumw_ = -999

            for ev in range(chain.GetEntries()):

                chain.GetEntry(ev)

                if hasattr(chain, 'nLHEPdfSumw_'):
                    if ev>0 and lastnLHEPdfSumw_!=chain.nLHEPdfSumw_ and not pdfWeightWarning:
                        if opt.verbose>=2:
                            print 'Warning', sam_k, 'trees have different PDF sets'
                        pdfWeightWarning = True
                    expectedPdfWeights = max(expectedPdfWeights, chain.nLHEPdfSumw_)
                    lastnLHEPdfSumw_ = chain.nLHEPdfSumw_

            for ev in range(chain.GetEntries()):

                chain.GetEntry(ev)

                if not hasattr(chain, 'genEventSumw_'):
                    if opt.verbose>=2:
                        print 'Error:', sam_k, ' tree does not have gen event weight information'
                    qcdStatus = 0
                    pdfStatus = 0
                    break

                if not hasattr(chain, 'nLHEScaleSumw_'):
                    if opt.verbose>=2:
                        print 'Error:', sam_k, ' tree does not have qcd scale information'
	            qcdStatus = 0
                
                if not hasattr(chain, 'nLHEPdfSumw_'):
                    if opt.verbose>=2:                                                                                                          print 'Error:', sam_k, 'tree does not have pdf scale information'
                    pdfStatus = 0

                genWeight += chain.genEventSumw_

                LHECentralSumw = -1.

                if qcdStatus and (chain.nLHEScaleSumw_==0 or chain.nLHEScaleSumw_==expectedScaleWeights): 

                    if ev==0:
                        for iqcd in range(expectedScaleWeights):
                            qcdWeights.append(0.)

                    if chain.nLHEScaleSumw_==expectedScaleWeights:

                        LHECentralSumw = chain.LHEScaleSumw_[4]

                        for iqcd in range(chain.nLHEScaleSumw_):
                            qcdWeights[iqcd] += chain.LHEScaleSumw_[iqcd]/LHECentralSumw*chain.genEventSumw_
 
                    else: 

                        for iqcd in range(expectedScaleWeights):                                                                                                   qcdWeights[iqcd] += chain.genEventSumw_
 
                        qcdStatus = 1

                else: 
                    qcdStatus = 0

		if pdfStatus and (chain.nLHEPdfSumw_==0 or chain.nLHEPdfSumw_>=expectedMinPdfWeights):  
                                                
                    if ev==0: 
                        for ipdf in range(expectedPdfWeights):
                            pdfWeights.append(0.)

                    if chain.nLHEPdfSumw_>=expectedMinPdfWeights and LHECentralSumw>0.:
                       
                        for ipdf in range(expectedPdfWeights):
                            if ipdf<chain.nLHEPdfSumw_:
                                pdfWeights[ipdf] += chain.LHEPdfSumw_[ipdf]/LHECentralSumw*chain.genEventSumw_
                            else:
                                pdfWeights[ipdf] += chain.genEventSumw_
                                if pdfStatus>2:
                                    pdfStatus = 2

                    else:

                        for ipdf in range(expectedPdfWeights):
                            pdfWeights[ipdf] += chain.genEventSumw_

                        pdfStatus = 1

                else:
                    pdfStatus = 0

            theoryNormalizations[sam_k] = { }

            theoryNormalizations[sam_k]['qcdScaleStatus'] = qcdStatus
            theoryNormalizations[sam_k]['pdfStatus'] = pdfStatus

            if qcdStatus:
                for iqcd in range(len(qcdWeights)):                                                                                                        qcdWeights[iqcd] /= genWeight
                theoryNormalizations[sam_k]['qcdScale'] = qcdWeights   
            elif opt.verbose:                                                     
                print 'Error: no qcd scale weights for sample', sam_k

            if pdfStatus:		
                for ipdf in range(len(pdfWeights)):
                    pdfWeights[ipdf] /= genWeight
                theoryNormalizations[sam_k]['pdf'] = pdfWeights
            elif opt.verbose:                                                                                                             print 'Error: no pdf weights for sample', sam_k

        else: # Signal samples

            sam_j = sam_k.split('_')[0] + '_' + sam_k.split('_')[1].split('-')[1] + '_' + sam_k.split('_')[2].split('-')[1]

            qcdStatus = 0

            genWeight = 0.
            qcdWeights = [ ]

            for iqcd in range(expectedScaleWeights):
		qcdWeights.append(0.)

            for treeName in sam_v['name']:

		chain = ROOT.TChain('Runs')		
                chain.Add(treeName)

                for ev in range(chain.GetEntries()):

                    chain.GetEntry(ev)
                    
                    if hasattr(chain, 'nLHEScaleSumw_'+sam_j):
                        if getattr(chain, 'nLHEScaleSumw_'+sam_j)==expectedScaleWeights:

                            LHEScaleSumw_ = getattr(chain, 'LHEScaleSumw_'+sam_j)
                            
                            if not isinstance(LHEScaleSumw_, float):

                                genWeight += getattr(chain, 'genEventSumw_'+sam_j)

                                for iqcd in range(expectedScaleWeights):                                                                                    qcdWeights[iqcd] += LHEScaleSumw_[iqcd]*getattr(chain, 'genEventSumw_'+sam_j)

                                qcdStatus = 3

            theoryNormalizations[sam_k] = { }

            theoryNormalizations[sam_k]['qcdScaleStatus'] = qcdStatus
                                                                
            if qcdStatus:
                for iqcd in range(len(qcdWeights)):  
                    qcdWeights[iqcd] /= genWeight
                theoryNormalizations[sam_k]['qcdScale'] = qcdWeights   
                if opt.verbose>=2:             
                    print sam_k, genWeight 
            else:
                print 'Error: no qcd scale weights for sample', sam_k 
                  
    with open('./theoryNormalizations_'+opt.year+'_'+opt.sigset+'.py', 'w') as file:
        if opt.sigset=='Backgrounds':
            file.write('theoryNormalizations = { }\n\n')
        for sample in theoryNormalizations:
            file.write('theoryNormalizations[\''+sample+'\'] = '+json.dumps(theoryNormalizations[sample])+'\n\n')




