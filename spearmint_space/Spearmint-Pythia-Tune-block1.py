import os
WorkHOME = os.environ['WorkHOME']
import sys
sys.path.append(WorkHOME)

import numpy as np
import csv
import subprocess
from time import time
from pythia_space.gen_parsFile import gen_parsFile
from pythia_space.MultiProc_GenPythia import MultiProc_Gen
from pythia_space.output_tasks import combine_output,get_chi2

n_cores = 7
Nevents = 142858

bin_widths = [0.025,0.025,0.05,0.05,0.032,0.032,0.015,0.015,0.02,0.02]

csv_Dir = '{}/pythia_space/Output_csv'.format(WorkHOME)

outputFile_bin_contents = '{}/output_bin_contents.csv'.format(csv_Dir)
outputFile_bin_errors   = '{}/output_bin_errors.csv'.format(csv_Dir)

object_contents = '{}/output_bin_contents_Monash.csv'.format(csv_Dir)
object_errors   = '{}/output_bin_errors_Monash.csv'.format(csv_Dir)

tune_contents   = '{}/output_bin_contents.csv'.format(csv_Dir)
tune_errors     = '{}/output_bin_errors.csv'.format(csv_Dir)

obj_file        = '{}/interface/objectives.csv'.format(WorkHOME)

def get_objective_func(job_id):

    pars_inputFile = '{}/interface/next_point_to_sample.csv'.format(WorkHOME)
    pars_outputFile = '{}/pythia_space/parsFile.txt'.format(WorkHOME)
    gen_parsFile(pars_inputFile,pars_outputFile)

    MultiProc_Gen(n_cores,Nevents,WorkHOME)

    combine_output(n_cores,csv_Dir,bin_widths,outputFile_bin_contents,outputFile_bin_errors)

    chi2 = get_chi2(object_contents,object_errors,tune_contents,tune_errors,obj_file)

    result = float(round(chi2,3))

    print 'Result = %f' % result
    return result

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
