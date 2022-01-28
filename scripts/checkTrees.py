#Script to check whether the files in a directory are zombies, and eventually delete them
from os import listdir, remove
from os.path import isfile, join

import optparse
import ROOT as r

########################## Main program #####################################                                         
if __name__ == "__main__":

    # ===========================================                                                                     
    # Argument parser                                                                                                 
    # ===========================================                                                                     
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-i', '--inputDir', action='store', type=str, dest='inputDir', default="")
    parser.add_option('-d', '--delete', action='store_true', dest='actuallyDeleteFiles', default=False)
    (opts, args) = parser.parse_args()

    actuallyDeleteFiles = opts.actuallyDeleteFiles
    inputDir = opts.inputDir

    filesToDelete = []
    onlyFiles = [f for f in listdir(inputDir) if isfile(join(inputDir, f))]
    
    for fileFound in onlyFiles:
        print(fileFound)
        try:
            f = r.TFile.Open(inputDir + fileFound)
            tree = f.Get("Events")
            if not f.GetListOfKeys().Contains("Events"):
                filesToDelete.append(inputDir + fileFound)
        except Exception as e:
            filesToDelete.append(inputDir + fileFound)

    if(len(filesToDelete) == 0):
        print("No files to matching the requirement have been found.")
    else:
        #print(filesToDelete)
        print(str(len(filesToDelete)) + " files matching the requirement have been found.")

        if(actuallyDeleteFiles):
            for fileToDelete in filesToDelete:
                remove(fileToDelete)
