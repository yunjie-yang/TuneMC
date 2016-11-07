import os
import numpy as np
import csv
import subprocess
import multiprocessing
import sys
import json
from math import sqrt

WorkHOME = os.environ['WorkHOME']

def get_objective_func(params):

    bin_widths_block1 = [0.025,0.025,0.05,0.05,0.032,0.032,0.015,0.015,0.02,0.02]
    bin_widths_block2 = [0.2,0.2,0.05,0.05]

    csv_Dir = '{}/pythia_space/Output_csv'.format(WorkHOME)

    outputFile_bin_contents = '{}/output_bin_contents.csv'.format(csv_Dir)
    outputFile_bin_errors   = '{}/output_bin_errors.csv'.format(csv_Dir)

    object_contents = '{}/output_bin_contents_Monash.csv'.format(csv_Dir)
    object_errors   = '{}/output_bin_errors_Monash.csv'.format(csv_Dir)

    tune_contents   = '{}/output_bin_contents.csv'.format(csv_Dir)
    tune_errors     = '{}/output_bin_errors.csv'.format(csv_Dir)

    obj_file        = '{}/interface/objectives.csv'.format(WorkHOME)

    pars_outputFile = '{}/pythia_space/pythia_input.txt'.format(WorkHOME)

    gen_pythia_input_from_dict(params,pars_outputFile)

    config_file = '{}/tune_config.json'.format(WorkHOME)

    config = load_config(config_file)

    n_cores = config['n_cores']

    N_events = config['N_events']

    Nevents, remainder = divmod(N_events,n_cores)
    if remainder != 0:
        Nevents += 1

    MultiProc_Gen(n_cores,Nevents,WorkHOME)

    combine_output(n_cores,csv_Dir,bin_widths_block1,bin_widths_block2,outputFile_bin_contents,outputFile_bin_errors)

    blocks = []
    for i in range(1,4):
        blocks.append(str_to_bool(config['block{}'.format(i)]))

    #if os.path.exists(obj_file):
    #    os.remove(obj_file)

    chi2 = get_chi2(blocks,object_contents,object_errors,tune_contents,tune_errors,obj_file)

    result = float(round(chi2,3))

    print 'Result = %f' % result
    return result


def gen_pythia_input_from_file(inputFile,outputFile):
    
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
    

def gen_pythia_input_from_dict(params,outputFile):

    WorkHOME = os.environ['WorkHOME']
    
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

    with open('{}/pythia_space/pars_to_tune.txt'.format(WorkHOME),'r') as parsList:
        param_names = parsList.read().splitlines()
        
    pars_info = load_config('{}/utils/all_pars_dict.json'.format(WorkHOME))

    for index, param_name in enumerate(param_names):
        category = pars_info[param_name]['category']
        value = params[param_name][0]
        output.write("{}:{} = {}\n".format(category,param_name,value))

    output.close()


def GenPythia(job_id,Nevents,WorkHOME):
    PythiaSpaceDir=WorkHOME+'/pythia_space'
    PythiaInputFile=PythiaSpaceDir+'/pythia_input.txt'
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

def Get_Ratio_Error_Numbers(num,denom):
    num=float(num)
    denom=float(denom)
    value = num/denom
    error = 0.
    if num == 0 and denom != 0:
        error = value * sqrt(1./denom)
    else:
        error = value * sqrt(1./num + 1./denom)
    return error

def check_one_percent(error,value):

    if value != 0.:
        if error/value <= 0.01:
            return value*0.01
        else:
            return error
    else:
        return error

def compute_chi2(o_value,o_error,t_value,t_error):
    error2 = o_error**2 + t_error**2
    if error2 != 0.:
        return (o_value-t_value)**2/error2
    else:
        return 0.

def combine_output(n_cores,csv_Dir,bin_widths_block1,bin_widths_block2,outputFile_bin_contents,outputFile_bin_errors):
    input_files = []
    for i_job in range(n_cores):
        input_files.append('{}/out_bin_content_{}.csv'.format(csv_Dir,i_job))

    combined_bin_content = []

    for index,iFile in enumerate(input_files):
        with open(iFile, 'rb') as f:
            reader = csv.reader(f)
            data_list = []
            for row in reader:
                data_list.append([float(i) for i in row])
            data_array = np.array(data_list)
        if index == 0:
            combined_bin_content = data_array.copy()
        else:
            for irow, row in enumerate(combined_bin_content):
                combined_bin_content[irow] = np.add(row,data_array[irow])

    output_bin_contents = []
    output_bin_errors   = []

    N_total   = 0
    N_udsc    = 0
    N_bTagged = 0
    
    #first 10: block1
    for ihist, hist in enumerate(combined_bin_content[0:10]):
        content_row = []
        error_row = []
        row_sum = 0
        
        if ihist == 0:
            for ibin in hist:
                N_total += ibin
                N_udsc  += ibin

        if ihist == 1:
            for ibin in hist:
                N_total   += ibin
                N_bTagged += ibin

        for ibin in range(1,len(hist)-1):
            row_sum += bin_widths_block1[ihist]*hist[ibin]
        
        bin_by_bin_normalize(combined_bin_content[ihist],row_sum,output_bin_contents,output_bin_errors)
    
    #next 6: block2
    
    bin_by_bin_normalize(combined_bin_content[10],float(N_udsc),output_bin_contents,output_bin_errors)
    bin_by_bin_normalize(combined_bin_content[11],float(N_bTagged),output_bin_contents,output_bin_errors)
        
    for ihist,hist in enumerate(combined_bin_content[12:16]):
        row_sum = 0
        
        for ibin in range(1,len(hist)-1):
            row_sum += bin_widths_block2[ihist]*hist[ibin]
        
        bin_by_bin_normalize(combined_bin_content[ihist+12],row_sum,output_bin_contents,output_bin_errors)

    
    #final 4: block3
    nCh_total = float(combined_bin_content[20][0])   
    
    #mesons
    mesons_content_row = []
    mesons_error_row   = []
    for ibin in combined_bin_content[16]:
        mesons_content_row.append(ibin/nCh_total)
        mesons_error_row.append(Get_Ratio_Error_Numbers(ibin,nCh_total))
    
    n_pi    = float(combined_bin_content[16][0])
    n_K     = float(combined_bin_content[16][2])
    n_Kstar = float(combined_bin_content[16][7])
    n_phi   = float(combined_bin_content[16][9])
    
    mesons_content_row.append(n_Kstar/n_K)
    mesons_error_row.append(Get_Ratio_Error_Numbers(n_Kstar,n_K))
    
    mesons_content_row.append(n_phi/n_Kstar)
    mesons_error_row.append(Get_Ratio_Error_Numbers(n_phi,n_Kstar))

    mesons_content_row.append(n_phi/n_K)
    mesons_error_row.append(Get_Ratio_Error_Numbers(n_phi,n_K))

    mesons_content_row.append(n_phi/n_pi)
    mesons_error_row.append(Get_Ratio_Error_Numbers(n_phi,n_pi))
            
    output_bin_contents.append(mesons_content_row)
    output_bin_errors.append(mesons_error_row)
    
    #baryons
    baryons_content_row = []
    baryons_error_row   = []

    for ibin in combined_bin_content[17]:
        baryons_content_row.append(ibin/nCh_total)
        baryons_error_row.append(Get_Ratio_Error_Numbers(ibin,nCh_total))

    n_p      = float(combined_bin_content[17][0])
    n_Lambda = float(combined_bin_content[17][1])
    
    baryons_content_row.insert(2,n_Lambda/n_p)
    baryons_error_row.insert(2,Get_Ratio_Error_Numbers(n_Lambda,n_p))
    
    baryons_content_row.insert(3,n_Lambda/n_K)
    baryons_error_row.insert(3,Get_Ratio_Error_Numbers(n_Lambda,n_K))

    output_bin_contents.append(baryons_content_row)
    output_bin_errors.append(baryons_error_row)
    
    #charm and beauty
    combined_bin_content[19][7] *= 10
    for ihist,hist in enumerate(combined_bin_content[18:20]):
        bin_by_bin_normalize_rates(combined_bin_content[ihist+18],float(N_total),output_bin_contents,output_bin_errors)
    
    
    content_file = open(outputFile_bin_contents,'w')
    content_file_writer = csv.writer(content_file,delimiter =',',
                                     quotechar=" ",lineterminator="\n",quoting=csv.QUOTE_ALL)
    error_file = open(outputFile_bin_errors,'w')
    error_file_writer = csv.writer(error_file,delimiter =',',
                                   quotechar=" ",lineterminator="\n",quoting=csv.QUOTE_ALL)

    for ihist in range(len(output_bin_contents)):
        content_file_writer.writerow(output_bin_contents[ihist])
        error_file_writer.writerow(output_bin_errors[ihist])

    content_file.close()
    error_file.close()

def bin_by_bin_normalize(hist,norm,output_content,output_error):
    content_row = []
    error_row   = []

    for ibin in range(1,len(hist)-1):
        content = hist[ibin]/norm
        content_row.append(content)
        error = Get_Ratio_Error_Numbers(hist[ibin],norm)
        error_row.append(error) 

    output_content.append(content_row)
    output_error.append(error_row)

def bin_by_bin_normalize_rates(hist,norm,output_content,output_error):
    content_row = []
    error_row   = []

    for ibin in range(len(hist)):
        content = hist[ibin]/norm
        content_row.append(content)
        error = Get_Ratio_Error_Numbers(hist[ibin],norm)
        error_row.append(error) 

    output_content.append(content_row)
    output_error.append(error_row)

def get_chi2(blocks,object_contents,object_errors,tune_contents,tune_errors,output_file):
    
    input_files = [object_contents,object_errors,tune_contents,tune_errors]

    lists = []

    for index,iFile in enumerate(input_files):
        with open(iFile, 'rb') as f:
            reader = csv.reader(f)
            data_list = []
            for row in reader:
                data_list.append([float(i) for i in row])
            lists.append(np.array(data_list))

    chi2s    = []

    ofile = open(output_file,'a')
    ofile_writer = csv.writer(ofile,delimiter =',',
                              quotechar=" ",lineterminator="\n",quoting=csv.QUOTE_ALL)

    for ihist in range(len(lists[0])):

        ihist_chi2 = 0

        for ibin in range(len(lists[0][ihist])):
            o_value = lists[0][ihist][ibin]
            o_error = lists[1][ihist][ibin]
            t_value = lists[2][ihist][ibin]
            t_error = lists[3][ihist][ibin]

            o_error = check_one_percent(o_error,o_value)
            t_error = check_one_percent(t_error,t_value)

            chi2 = compute_chi2(o_value,o_error,t_value,t_error)

            ihist_chi2 += chi2

        chi2s.append(ihist_chi2)
        
        
    result_chi2 = 0.
    for index,chi2 in enumerate(chi2s):
        if blocks[0] and index >= 0  and index < 10:
            result_chi2 += chi2
        if blocks[1] and index >= 10 and index < 16:
            result_chi2 += chi2
        if blocks[2] and index >= 16 and index < 19:
            result_chi2 += chi2
        
    
        
    ofile_writer.writerow(chi2s)
    ofile.close()

    return result_chi2

def load_config(config_file):
    try:
        with open(config_file,'r') as json_file:
            json_data = json.load(json_file)
            return json_data
    except:
        raise Exception('json file loading failed. Please check commas or parentheses?')

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError("Cannot covert string {} to a bool.".format(s))

