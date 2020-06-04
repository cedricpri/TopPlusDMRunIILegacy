import os
import ROOT as r
import numpy as np
from optparse import OptionParser


if __name__ == "__main__":

    parser = OptionParser(usage="%prog --help")
    parser.add_option("-i", "--input",     dest="input",       type="string",   default='afile.root',     help="Input root directory")
    parser.add_option("-o", "--output",    dest="output",      type="string",   default='anotherfile.root',     help="output file")
    (options, args) = parser.parse_args()

    
    if not os.path.isfile(options.input):
        print('Input file does not exist')
        quit()
    
    name = options.output

        
    f = r.TFile(options.input)
    listOfEvents = []
    for ev in f.Events:
        events = []
        events.append(ev.PuppiMET_pt)
        events.append(ev.mt2ll)
        events.append(ev.dphillmet)
        events.append(ev.dark_pt)
        events.append(ev.nbJet)
        events.append(ev.mblt)
        listOfEvents.append(events)

    numpyarray = np.asarray(listOfEvents)
    np.savetxt(name, numpyarray, delimiter=',')

    f.Close()


            
