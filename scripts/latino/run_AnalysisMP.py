#!/usr/bin/env python
import timeit
import optparse
import sys, os

gridui=True
#To be updated to a more general option
#if gridui is True:
#    SUS19='/gpfs/users/pmatorra/CMSSW_10_2_14/src/PlotsConfigurations/Configurations/SUS-19-XXX/'
#else:
cmsenv=' eval `scramv1 runtime -sh` '
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
SUS19 = dname

if __name__ == '__main__':
    doDC=False
    if len(sys.argv)<4:
        print 'Please, specify year, tag and sigset values, in that order'
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

    #    tag=sys.argv[2]

    sigset=sys.argv[3]

    dcIdx = 4
    if len(sys.argv)>=5:
        if os.getenv('USER') in sys.argv[4]:
            SUS19 = sys.argv[4]
            dcIdx = 5
                                         
    if len(sys.argv)==dcIdx+1:
        if(sys.argv[dcIdx].lower()in ["dodatacards","dodc","mkdc","makedatacards"]):
            doDC=True
            fileset=sigset
        else:
            fileset=sys.argv[dcIdx]
    elif len(sys.argv)==dcIdx+2:
        fileset=sys.argv[dcIdx] 
        if(sys.argv[dcIdx+1].lower()in ["dodatacards","dodc", "mkdc","makedatacards"]):
            doDC=True
    else:
        fileset=sigset

    if 'SM-' not in fileset:
        fileset = 'SM-' + fileset
    #print sys.argv[4].lower()
    opts= "--years="+yearset+" --tag="+tag+" --sigset="+sigset 
    cmdDatacards =' '
    if(doDC is True):    cmdDatacards += './run_mkDatacards.py '+yearset+' '+tag+ ' '+ sigset+' '+ fileset + ' ;'
    name='python run_CombineTools.py'
    command= ' '+name+' '+opts
    print "Command sent:\t", command,'\n','CWD:', os.getcwd()
    if doDC: print " datacards:\n", cmdDatacards
    else: print "datacards are not made"
    os.system('cd '+ SUS19+ '; '+cmsenv+';'+ cmdDatacards +command)
    if doDC:
        for year in yearset.split('-'):
            for masspoint in sigset.split(','):
                os.system('cd '+SUS19+'; rm -r ./Datacards/'+year+'/'+tag+'/'+masspoint)

    years = yearset.split('-')
