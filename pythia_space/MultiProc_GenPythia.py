import numpy as np
import csv
import subprocess
import multiprocessing
import sys

def GenPythia(job_id,Nevents,WorkHOME):    
    PythiaSpaceDir=WorkHOME+'/pythia_space'
    PythiaInputFile=PythiaSpaceDir+'/parsFile.txt'
    Dir_OutputText=PythiaSpaceDir+'/Output_text'
    Dir_OutputCSV=PythiaSpaceDir+'/Output_csv'
    shell_command = '{}/pythia_gen {} {} {} {}/out_bin_content_{}.csv > {}/Output_{}.txt 2>&1'.format(PythiaSpaceDir,int(job_id),Nevents,
                                                                            PythiaInputFile,
									    Dir_OutputCSV,int(job_id),
									    Dir_OutputText,int(job_id))
    print shell_command
    subprocess.call([shell_command],shell=True)


def MultiProc_Gen(n_cores,Nevents,WorkHOME):
    n_procs = n_cores
    jobs = [] 

    for i_job in range(n_procs):
        process = multiprocessing.Process(target=GenPythia,args=(i_job,Nevents,WorkHOME))
        jobs.append(process)

    for j in jobs: # Start the processes
        j.start()

    for j in jobs:
        j.join()

if __name__=="__main__":
    WorkHOME='/Users/Yunjie/Documents/TuneMC'
    MultiProc_Gen(7,142858,WorkHOME)
    print "Generation Finished!"
