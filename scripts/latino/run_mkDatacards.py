#!/usr/bin/env python

import sys
import os

if len(sys.argv)<4:
    print 'Please, specify year, tag and sigset values!'
    sys.exit()

if sys.argv[1]=='-1':
    yearset='2016-2017-2018'
elif sys.argv[1]=='0':
    yearset='2016'
elif sys.argv[1]=='1':
    yearset='2017'
elif sys.argv[1]=='2':
    yearset='2018'
else:
    yearset=sys.argv[1]

if   sys.argv[2]== '0':
    tag='Preselection'                                                                         
elif sys.argv[2]== '1':
    tag='ValidationRegions'                                                                    
elif sys.argv[2]=='2':
    tag='StopSignalRegions'                                                                    
else: 
    tag=sys.argv[2]

sigset=sys.argv[3]

if len(sys.argv)==5:
    fileset=sys.argv[4]
else:
    fileset=sigset
if 'SM-' not in fileset:
    fileset = 'SM-' + fileset

#exec(open('./signalMassPoints.py').read())

years = yearset.split('-')

inputtag = tag.replace('StatZero', '')
inputtag = tag.replace('NoStat0', '')

exec(open('./signalMassPoints.py').read())
for year in years:
    os.system('mkdir -p ./Datacards/'+year+'/'+tag)

    for massPoint in signalMassPoints:
        if massPointInSignalSet(massPoint, sigset):
        
            options = massPoint.split("-")
            modelSelected = options[0]
            massPointSelected = options[1]

            os.system('mkDatacards.py --pycfg=configuration.py --tag='+year+tag+' --sigset='+sigset+' --outputDirDatacard=./Datacards/'+year+'/'+tag+'/'+massPointSelected+' --inputFile=./Shapes/'+year+'/'+inputtag+'/plots_'+inputtag+'_'+fileset+'.root')
