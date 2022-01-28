#!/usr/bin/env python
import os,sys
from datetime import datetime
import numpy as np

PWD = os.getenv('PWD')+'/'
    
nMPs    = 3
server  = os.uname()[1]
flavour = "\"workday\""
if 'ifca' in server.lower():
    flavour = "gridui_sort"
#write header to logfile
def logtitle(filename,sigset):
    if(os.path.exists(filename) is False):  print "creating log file"
    f = open(filename,"a")
    # Textual month, day and year
    now = datetime.now()
    d2  = now.strftime("%d %B, %Y, at %H:%M:%S")
    f.write(d2+"\nCALCULATING LIMITS FOR:\t "+ sigset+"\n")
    f.close()


#Create log file
def writetolog(filename,line):
    f = open(filename,"a")
    f.write(line+'\n')
    f.close()
    #print "line", line

#Function to create sub file                                                              
def makeSubFile(filename,folder,sigset,arguments,flavour):
    f = open(filename,"w+")
    jobsent= '$('+sigset+')'
    #print "creating "+filename+" \t ARGUMENTS:\n ",arguments, "\n"                       
    f.write("executable            = "+PWD+"run_AnalysisMP.py \n")
    f.write("arguments             = "+arguments+"\n")
    f.write("output                = "+folder+"/"+jobsent+".$(ClusterId).out\n")
    f.write("error                 = "+folder+"/"+jobsent+".$(ClusterId).err\n")
    f.write("log                   = "+folder+"/"+jobsent+".$(ClusterId).log\n")
    #f.write("+JobFlavour           = nextweek\n")
    f.write("+JobFlavour           = "+flavour+"\n")
    #f.write("+JobFlavour           = testmatch\n")
    #f.write("+JobFlavour           = tomorrow\n")
    f.write("queue "+sigset+' from '+folder+'/joblist.txt \n')
    f.close()



#Remove duplicated substrings in a string
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

args=sys.argv
if len(args)<4:      
    print 'Please, specify year, tag and sigset values, in that order'
    sys.exit() 

#Take args
if   args[1] == '-1':
    year = '2016-2017-2018'
    if(nMPs >= 3):  nMPs = nMPs//3
    if(nMPs <  3):  nMPs = 1
elif args[1] == '0':
    year = '2016'
elif args[1] == '1':
    year = '2017'
elif args[1] == '2':
    year = '2018'
else:
    year = args[1]
if   args[2] == '0':                                                             
    tag ='Preselection'                                                             
elif args[2] == '1':                                                            
    tag ='ValidationRegions'                                                        
elif args[2] =='2':                                                             
    tag ='StopSignalRegions'                                                        
else:                                                                              
    tag = args[2]
 
sigset    = args[3]
signm     = sigset.split('_')[0]
fileset   = sigset
allMP     = False
allMPopts = ['doallmp', 'doall','allmp', 'allmasspoints', 'alllims']
doDCopts  = ["dodatacards","dodc", "mkdc","makedatacards"]
flavopts  = {"0" : "espresso", "1" : "microcentury", "2" : "longlunch", 
             "3" : "workday" , "4" : "tomorrow"    , "5" : "testmatch", 
             "7" : "nextweek"}
 
doDC      = ' '
argfloc   = 0
print "before the loop"
for arg in args[4:]:
    print arg, sigset.split('_')[0]
    if arg.lower() in doDCopts : doDC    = arg
    if arg.lower() in allMPopts: allMP   = True
    if signm       in arg      : fileset = arg
    if "nmp=" in arg.lower():
        nMPi= arg.split("=")[1]
        if nMPi.isdigit():
            nMPs = nMPi
            print "JOBS SPLIT EACH "+nMPi+" MASSPOINTS"
        else:
            print "MASSPOINT NUMBER NOT VALID"
            exit()
    if "fl=" in arg.lower():
        flvi=arg.split("=")[1]
        print "FLVI", flvi
        if   flvi in flavopts:
            flavour = "\"" + flavopts[flvi] + "\""
        elif flvi in flavopts.values():
            flavour = "\"" + flvi           + "\""
        else:
            print "flavour not recognised"
            exit()



'''
if(len(args)>4):
    if   args[4].lower() in allMPopts:
        allMP = True
    
    elif args[4].lower()in doDCopts  :
        print "in here"
        doDC    = args[4]
        fileset = sigset
    else:
        fileset = args[4]
        
    if len(args) > 5:
        if args[5].lower() in allMPopts:
            allMP = True
        else:
            doDC = args[5]
            if len(args)>6 and args[6].lower() in allMPopts:
                allMP = True
else: fileset = sigset

nMPi=None
if "nmp=" in args[len(args)-1].lower():
    nMPi = args[len(args)-1].split("=")[1]
    if nMPi.isdigit():
        nMPs = nMPi
        print "JOBS SPLIT EACH "+nMPi+" MASSPOINTS"
    else: 
        print "MASSPOINT NUMBER NOT VALID"
        exit()
flloc=len(args)-1
if nMPi: flloc=len(args)-2 
if "fl=" in args[flloc]:
    flvi = args[flloc].split("=")[1]
    if   flvi in flavopts:
        flavour = "\"" + flavopts[flvi] + "\""
    elif flvi in flavopts.values():
        flavour = "\"" + flvi           + "\"" 
    else:
        print "flavour not recognised"
        exit()


if args[flloc] in flavopts:
    flavour = "\""+args[flloc]+"\""
'''


print flavour, "MP", nMPs
print year, tag, sigset,"\n MISSING ARGUMENTS:", doDC, fileset, flavour
#exit()


exec(open("signalMassPoints.py").read())
dcyears = year.split('-')
for dcyear in dcyears:
    print dcyears, dcyear
    str_SM = '_'
    if 'SM-' not in fileset: str_SM = '_SM-' 
    inputfile='./Shapes/'+dcyear+'/'+tag+'/plots_'+tag+str_SM+fileset+'.root'
    if os.path.exists(inputfile) is False:
        print "ROOT File",inputfile," doesn't exist, exiting"
        exit()
    else:
        print "Reading:",inputfile

#Look for masspoints in the sigset
missDCfolder = []
mpInSigset   = []
emptyDC      = []
missDC       = []

            
for model in signalMassPoints:
    print "Model:", model,"\tSignal set", sigset
    if model not in sigset:  continue
    for massPoint in signalMassPoints[model]:
        if(massPointInSignalSet(massPoint,sigset)):

            submitThis = True
	    rootname   = './Limits/' + year + '/' + tag + '/' + massPoint + '/higgsCombine_' + tag + '_Blind.AsymptoticLimits.mH120.root'
            #Only do empty files unless otherwise implied
            if os.path.isfile(rootname) and allMP is False:  
                if os.path.getsize(rootname)>6500:
                    submitThis = False
                    print "ignored", massPoint
            if submitThis is False: continue
            mpInSigset.append(massPoint)
            #print massPoint, dcyear#, os.listdir(dclocs)
            
            #Pick datacards if necessary 
            if(doDC.lower() in doDCopts): continue
            print '#####################\nDC', 
            for dcyear in year.split('-'):
                dcfolder = './Datacards/'+dcyear+'/'+tag+'/'+massPoint+'/'
                if(os.path.exists(dcfolder) is False): 
                    missDCfolder.append(dcfolder) 
                    continue
                dclocs = os.listdir(dcfolder)
                print dcfolder
                for dcloc in dclocs:
                    whichdc = dcfolder+'/'+dcloc+'/mt2ll/'
                    if(os.path.exists(whichdc+'datacard.txt') is False):
                        missDC.append(whichdc)
                        continue
                    dcsize = os.path.getsize(whichdc+'datacard.txt')
                    if(dcsize<5000 and doDC not in doDCopts): emptyDC.append(whichDC)
                                                
            print "missing datacards:", len(missDC)+len(emptyDC)
            
        if massPoint not in sigset: continue
        print "Mass Point:", massPoint 

#Print missing MP/DC
print "Total datacards missing", len(missDC)
if len(mpInSigset) == 0: 
    print "no masspoints in the given sigset. Exiting"
    exit()
missDCmessage="please use the doDC option, or check the DC themselves"
if len(missDCfolder) > 0:
    print "missing datacard folders:"
    for dcfolder in missDCfolder: print dcfolder
    print missDCmessage
if len(missDC)  > 0:
    print "missing datacards:"
    for dc in missDC: print dc
    print missDCmessage
if len(emptyDC) > 0:
    print "unfilled datacards:"
    for dc in emptyDC: print dc
    print missDCmessage
if len(missDCfolder) > 0 or len(missDC) > 0 or len(emptyDC) > 0:
    print "exiting..."
    exit()


#Make a more human-readable logfile if necessary
sigsets     = sigset.split(',')
firstsigset = sigsets[0].split('_')
writesigset = firstsigset    
for i in range(0,len(sigsets)):
    if i is 0: continue
    diffmp = ''
    thissigset  = sigsets[i].split('_')    
    if(len(firstsigset) is not len(thissigset)): continue
    for j in range(0,len(thissigset)):
        if(firstsigset[j] != thissigset[j]):
            if(j<len(thissigset)-1): diffmp='-'
            firstpart       = (firstsigset[j]+'_').split('-')
            thispart        = (thissigset[j]+'_').split('-')
            writesigset[j] += diffmp+'-'+thissigset[j]

#remove duplicate mS and similars            
try:
    nmS = writesigset[1].count('mS')
    nmX = writesigset[2].count('mX')
except IndexError:
    nmS = 0
    nmX = 0
    print "either no mS or mX specified"

    if   nmS>1: writesigset[1] = rreplace(writesigset[1] , 'mS', '', nmS - 1)
    elif nmX>1: writesigset[2] = rreplace(writesigset[2] , 'mX', '', nmX - 1)



#divide masspoints in sets of nMPs and send jobs
lognm       = '_'.join(writesigset)
jobfolder   = "./Condor/"+year+'/'+tag
logfile     = jobfolder + '/'+lognm+".log"
subfilename = jobfolder + '/'+lognm+".sub"
flistname   = jobfolder+'/joblist.txt'


os.system("mkdir -p "+jobfolder)
logtitle(logfile,fileset)
logline  =   "Input arguments:\t"+ year + ' ' + tag + ' ' + fileset + ' ' + doDC
logline += "\nSample list    :\t" + flistname
logline += "\nSubmission file:\t"+ subfilename
writetolog(logfile, logline)

jobs     = [sorted(mpInSigset)[x:x+nMPs] for x in xrange(0, len(mpInSigset), nMPs)]
flist    = open(flistname,"w+")
gridui   = False

if 'gpfs' in PWD: 
    gridui  = True
    gridfol = 'Limits/Jobs/'+fileset+'/'
    os.system('mkdir -p '+gridfol) 
for ijob,job in enumerate(jobs):
    argsigset = ",".join(job)
    flist.write(argsigset+'\n')
    #    submit="condor_submit "+subfilename+" >>"+logfile
    
    if gridui is True:
        arguments = year+' '+tag+' '+argsigset+ ' ' +PWD+' '+fileset+' '+str(doDC)
        gridnm    = gridfol+argsigset
        gridcomm  = 'sbatch -o '+gridnm+'.out -e '+gridnm+'.err --qos=gridui_sort --partition=cloudcms '+gridnm+'.sh>'+gridnm+'.jid'
        f2 = open(gridnm+".sh","w+")
        f2.write("#!/bin/bash")
        f2.write("\npython run_AnalysisMP.py "+arguments)
        f2.close()
        os.system(gridcomm)
        #print gridcomm
    print "sending job",str(ijob)+":", argsigset# arguments  
flist.close()


print PWD
#exit()
if 'cern.ch' in PWD: 
    jobsent      = 'MPs'#Works since files MPs are already in joblist.txt
    argsent      = '$('+jobsent+')'
    arguments    = year+' '+tag+' '+argsent+ ' ' +PWD+' '+fileset+' '+str(doDC)
    commandtorun = "condor_submit "+subfilename+">>"+logfile
    makeSubFile(subfilename,jobfolder,jobsent, arguments, flavour)
    os.system(commandtorun)
    print "jobs sent:\n", commandtorun
    writetolog(logfile,"----------------------------------")

print "LIMITS SENT\nlog file:\t"+logfile,"\nsub file:\t"+subfilename,"\njob list:\t"+flistname 

