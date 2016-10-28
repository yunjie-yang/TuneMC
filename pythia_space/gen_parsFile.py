import os
import numpy as np
import csv

def gen_parsFile(inputFile,outputFile):
    
    with open(inputFile, 'rb') as f:
        reader = csv.reader(f)
        pars = []
        for row in reader:
            pars.append([float(i) for i in row])
        pars = np.squeeze(pars)
    
    if os.path.exists(outputFile):
        os.remove(outputFile)
    
    output = open(outputFile,'a')
    
    basic_info = [
        "Tune:ee = 7",
        "Beams:idA = 11",
        "Beams:idB = -11",
        "Beams:eCM = 91.2",
        "WeakSingleBoson:ffbar2gmZ = on",
        "23:onMode = off",
        "23:onIfMatch = 1 -1",
        "23:onIfMatch = 2 -2",
        "23:onIfMatch = 3 -3",
        "23:onIfMatch = 4 -4",
        "23:onIfMatch = 5 -5"
    ]
    
    for info_line in basic_info:
        output.write("{}\n".format(info_line))

    par_names = [
        "TimeShower:alphaSvalue",
        "TimeShower:pTmin",
        "TimeShower:pTminChgQ"
    ]
        
    for index, par in enumerate(pars):
        output.write("{} = {}\n".format(par_names[index],par))
        
    output.close()
    
    print pars
