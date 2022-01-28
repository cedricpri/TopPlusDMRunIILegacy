from optparse import OptionParser
import glob
import os
import stat


###########################################################################################
theExecutable = """#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /gpfs/users/parbol/LucaTest/ProductionRelease/CMSSW_10_2_15/src/ 
eval `scramv1 runtime -sh`
cd OUTPUTDIRECTORY
hadd OUTPUTNAME INPUT
"""
###########################################################################################


def prepareCommand(index, outputdir, block):

    nameOfSample = block[0][block[0].find('nanoLatino'):block[0].find('__part')]
    text = theExecutable
    text = text.replace('OUTPUTDIRECTORY', outputdir)
    text = text.replace('OUTPUTNAME', nameOfSample + '__part' + str(index) + '.root')
    inputstr = ''
    for f in block:
        inputstr = inputstr + f + ' '
    text = text.replace('INPUT', inputstr)
        
    exename = nameOfSample + '__part' + str(index) + '.sh'
    logname = nameOfSample + '__part' + str(index) + '.log'
    errname = nameOfSample + '__part' + str(index) + '.err'
    fexe = open(exename, 'w')
    fexe.write(text)
    fexe.close()
    st = os.stat(exename)
    os.chmod(exename, st.st_mode | stat.S_IEXEC)
    addendum = 'sbatch ' + ' -o ' + logname + ' -e ' + errname + ' --qos=gridui_medium --partition=cloudcms ' + exename + '\n'
    thefile = open('run.sh', 'a+')
    thefile.write(addendum)
    thefile.close()


#------------------------------------- MAIN --------------------------------------------
if __name__ == '__main__':

    parser = OptionParser(usage="%prog --help")
    parser.add_option("-s","--sample",       dest="sample",      help="Sample name",     default='2016',     type='string')
    parser.add_option("-d","--directory",    dest="directory",   help="Directory",       default='dir',      type='string')
    parser.add_option("-o","--output",       dest="outputdir",   help="Output",          default='output',   type='string')
    parser.add_option("-n","--number",       dest="number",      help="Number",          default=20,         type=int)

    (options, args) = parser.parse_args()

    #Check that there are enough files to hadd

    inputFolder = options.directory
    model = options.sample
    output = options.outputdir
    n = options.number

    files = glob.glob(inputFolder + '/' + model + '__part*.root')
    m = len(files)
    step = int(m / n) + 1
    listOfFiles = []

    print('Sample ' + model)
    print('Asked to produce ' + str(n) + ' files')
    print('There are ' + str(m) + ' files')
    print('The step is ' + str(step))

    counter = 0
    thefiles = []
    for i in files:
        if counter == step:
            listOfFiles.append(thefiles)
            thefiles = []
            counter = 0
        thefiles.append(i)
        counter = counter + 1
    listOfFiles.append(thefiles)

    totalfiles = 0
    for i, block in enumerate(listOfFiles):
        command = prepareCommand(i, output, block)




