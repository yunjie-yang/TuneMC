import os
WorkHOME = os.environ['WorkHOME']
import sys
sys.path.append(WorkHOME)

import numpy as np
import csv
import subprocess
import json
from time import time
from pythia_space.pythia_functions import get_objective_func


def main(job_id, params):
    print 'Anything printed here will end up in the output directory for job #%d' % job_id
    print params

    timeStamp = float(time())

    print "job id = {0:d}, time stamp = {1:.2f}".format(job_id,timeStamp)

    param_names = ['alphaSvalue','pTmin','pTminChgQ']

    n_params = len(param_names)

    next_point_raw=[]
    for i in range(n_params):
	next_point_raw.append(params[param_names[i]][0])

    next_point = np.array(next_point_raw).copy()

    Parfile  = open('{}/interface/next_point_to_sample.csv'.format(WorkHOME),'wb')
    writer = csv.writer(Parfile, delimiter =',',quotechar=" ",lineterminator="\n",quoting=csv.QUOTE_ALL)
    writer.writerow(next_point)
    Parfile.close()

    parm_start = time()
    obj_func = get_objective_func(job_id)
    parm_end   = time()
    parm_time  = float(round(parm_end - parm_start,2))

    TimeStampFile  = open('{}/interface/time_stamps.csv'.format(WorkHOME),'a')
    writer_time = csv.writer(TimeStampFile, delimiter =',',quotechar=" ",lineterminator="\n",quoting=csv.QUOTE_ALL)
    writer_time.writerow([job_id,timeStamp,parm_time])
    TimeStampFile.close()

    resultsfile  = open('{}/interface/results.csv'.format(WorkHOME),'a')
    resultsWriter = csv.writer(resultsfile, delimiter =',',quotechar=" ",lineterminator="\n",quoting=csv.QUOTE_ALL)
    resultrow = []
    resultrow.append(obj_func)
    for value in next_point:
	resultrow.append(value)
    resultrow.append(job_id)
    resultsWriter.writerow(resultrow)
    resultsfile.close()

    print "Sampled f({0:s})      = {1:.7f}".format(str(next_point), float(obj_func))

    return obj_func
