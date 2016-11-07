import csv
import subprocess

import matplotlib.pyplot as plt
import numpy as np

import pandas as pd

import os
import shutil

from utils.general_utils import load_config,str_to_bool


config = load_config('tune_config.json')
WorkHOME = config['WorkHOME']

all_pars_dict = load_config('{}/utils/all_pars_dict.json'.format(WorkHOME))

blocks = []
for i in range(1,4):
    blocks.append(str_to_bool(config['block{}'.format(i)]))

with open('{}/pythia_space/pars_to_tune.txt'.format(WorkHOME),'r') as parsList:
     param_names = parsList.read().splitlines()

n_cores = config['n_cores']

TextsDir = '{}/interface'.format(WorkHOME)
PlotsDir = '{}/spearmint_space/Plots'.format(WorkHOME)

TimeIndexRemoval = [519]

NEW = True
#NEW = False

#FileKey = ''
WriteBest = 0
GenBest   = 0 

if NEW:
	results_FILE          = '{}/results.csv'.format(TextsDir)
	time_stamps_FILE      = '{}/time_stamps.csv'.format(TextsDir)
	objectives_FILE       = '{}/objectives.csv'.format(TextsDir)
	Spearmint_output_FILE = '{}/spearmint_output.txt'.format(TextsDir)

if not NEW:
        results_FILE          = '{}/Tune_Results/{}/results_{}.csv'.format(WorkHOME,FileKey,FileKey)
        time_stamps_FILE      = '{}/Tune_Results/{}/time_stamps_{}.csv'.format(WorkHOME,FileKey,FileKey)
        objectives_FILE       = '{}/Tune_Results/{}/objectives_{}.csv'.format(WorkHOME,FileKey,FileKey)
        spearmint_output_FILE = '{}/Tune_Results/{}/spearmint_output_{}.txt'.format(WorkHOME,FileKey,FileKey)


def getKey(item):
    return item[0]

def main():

    param_order = find_order()

    MonashValues = [] 
    param_ranges = []
    for par in param_names:
        MonashValues.append(all_pars_dict[par]['Monash'])
	param_ranges.append((all_pars_dict[par]['min'],all_pars_dict[par]['max']))

    MonashValues = np.array(MonashValues)

    header = ['obj'] + param_names + ['job_id']

    spectra_names_block1  =  ["hThrusts_udsc", "hThrusts_b",
                              "hC_param_udsc", "hC_param_b",
                              "hD_param_udsc", "hD_param_b",
                              "hB_W_udsc","hB_W_b",
                              "hB_T_udsc","hB_T_b"]

    spectra_names_block2  =  ["hChargeMulti_udsc","hChargeMulti_b",
                              "hMomentFrac_udsc","hMomentFrac_b",
                              "hMomentFrac_Dstar","hMomentFrac_bWeak"]

    spectra_names_block3  =  ["hMesonFrac","hBaryonFrac",
                              "hCharmRates","hBeautyRates"]

    spectra = [spectra_names_block1,spectra_names_block2,spectra_names_block3]

    spectra_names = []

    for index,block in enumerate(blocks):
	if block:
	    spectra_names += spectra[index]

    param_nRows,param_nCols,spectra_nRows,spectra_nCols = nRows_nCols(blocks)

    #################################################################
    ############      Reading in results       ######################
    #################################################################

    results = pd.read_csv(results_FILE,names=header)
  
    objs=results['obj'].values
    occurrence=results['job_id'].values

    #################################################################
    ############      Generating time profile  ######################
    #################################################################

    time_stamps = []
    GenerationTime = []
    TimeStampFile   = open(time_stamps_FILE,'rb')
    TimeReader = csv.reader(TimeStampFile)
    for line in TimeReader:
	time_stamps.append(float(line[1]))
	GenerationTime.append(float(line[2]))

    for idx, time_index in enumerate(TimeIndexRemoval):
	GenerationTime.remove(GenerationTime[int(time_index)-idx])


    TimeInterval = []
    for i in range(len(time_stamps)-1):
	TimeInterval.append(time_stamps[i+1]-time_stamps[i])

    print 'Time Info (per query):'
    for time in TimeInterval:
	print "index = ", TimeInterval.index(time), "   , value = ", time

    for idx, time_index in enumerate(TimeIndexRemoval):
	TimeInterval.remove(TimeInterval[int(time_index)-idx])

    Grand_Total_time = round(float(np.sum(np.array(TimeInterval))/3600.),1)
 
    Time_outputFile = '{}/Time.pdf'.format(PlotsDir)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(TimeInterval,'b',label='Total Time')
    plt.plot(GenerationTime,'r', label='Generation Time')
    plt.legend(loc='best')
    time_text='Grand Total Time = {} hours'.format(str(Grand_Total_time))
    ax.text(0.25, 0.75,time_text, ha='center', va='center', transform=ax.transAxes)
    plt.xlabel("Query Number")
    plt.ylabel("Seconds")
    fig.savefig(Time_outputFile)


    wall_25 = round(np.sum(np.array(TimeInterval[0:25*len(param_names)]))/3600.,1)
    wall_50 = round(np.sum(np.array(TimeInterval[0:50*len(param_names)]))/3600.,1)

    length_to_use = np.min([len(TimeInterval),len(GenerationTime)])

    Spearmint_time = np.array(np.array(TimeInterval[0:length_to_use]) - np.array(GenerationTime[0:length_to_use])) 
    GenerationTime = np.array(GenerationTime[0:length_to_use])

    cpu_25 = round(np.sum(np.array(GenerationTime[0:25*len(param_names)]*n_cores+Spearmint_time[0:25*len(param_names)]))/3600.,1)
    cpu_50 = round(np.sum(np.array(GenerationTime[0:50*len(param_names)]*n_cores+Spearmint_time[0:50*len(param_names)]))/3600.,1)

    print "wall_25 = {}".format(wall_25)
    print "wall_50 = {}".format(wall_50)
    print "cpu_25  = {}".format(cpu_25)
    print "cpu_50  = {}".format(cpu_50)

    #################################################################
    ########      Generating total obj evolution   ##################
    #################################################################

    obj_evolv_outputFile = '{}/obj_evolv.pdf'.format(PlotsDir)
    
    expected_objs = []

    expected_best_params = [[] for i in range(len(param_names))]
    for iparam in range(len(param_names)):
        expected_best_params[iparam].append(param_ranges[iparam][0])
        expected_best_params[iparam].append((param_ranges[iparam][1]+param_ranges[iparam][0])/2.)

    param_dict = {}

    param_index = 0
    inFile = open(Spearmint_output_FILE)
    lines = list(inFile)
    inFile.seek(0)
   
    for index, line in enumerate(inFile):
        lo_index = line.find("Minimum expected objective value under model is")
        str_len  = len("Minimum expected objective value under model is")
        up_index = line.find("(+/-")
        if lo_index != -1 and up_index !=-1:
                expected_objs.append(float(line[lo_index+str_len:up_index]))
                param_index = index+3
    
                current_param_index = index+3
                value_start_index=lines[current_param_index-1].rfind("-----")
                value_end_index = value_start_index+10
                for ind,line in enumerate(lines[current_param_index:current_param_index+len(param_names)]):
                    param_dict[param_order[ind]]=float(line[value_start_index:value_end_index])
                for idx,param_name in enumerate(param_names):
                    expected_best_params[idx].append(param_dict[param_name])

    inFile.seek(0)
    lines = list(inFile)
    value_start_index = lines[param_index-1].rfind("-----")
    value_end_index   = value_start_index+10

    for index,line in enumerate(lines[param_index:param_index+len(param_names)]):
        param_dict[param_order[index]]=float(line[value_start_index:value_end_index])

    Best_Model_Param = []
    for param_name in param_names:
        Best_Model_Param.append(param_dict[param_name])


    fig = plt.figure()
    plt.plot(objs,color='b',label="Observed")
    plt.plot(expected_objs,color='r',label="Model")
    plt.yscale('log')
    plt.xlabel('Query Number')
    plt.ylabel('obj')
    plt.legend(loc='best')
    plt.title('Spearmint e+e- Tune')
    fig.savefig(obj_evolv_outputFile)

    #################################################################
    ########   Generating individual obj evolution   ################
    #################################################################

    IndChi2_header = []
    for name in spectra_names:
	IndChi2_header.append(name)
    objectives = pd.read_csv(objectives_FILE,names=IndChi2_header)

    IndChi2_evolv_outputFile = '{}/ind_chi2_evolv.pdf'.format(PlotsDir)
    plt.figure(figsize=[16,20])
    for index, spectrum in enumerate(spectra_names):
        plt.subplot(spectra_nRows,spectra_nCols,index+1)
        plt.xlabel('Query Number')
        plt.plot(objectives[spectrum].values,label=spectrum)
	plt.yscale('log')
        plt.legend(loc='best', bbox_to_anchor=(0.5, 1.1),fancybox=True, shadow=True)
    plt.savefig(IndChi2_evolv_outputFile)


    #################################################################
    ##########      Generating Parameter evolution     ##############
    #################################################################

    
    param_evolv_outputFile = '{}/param_evolv.pdf'.format(PlotsDir)
    plt.figure(figsize=[16,20])
    for index, param in enumerate(param_names):
    	plt.subplot(param_nRows,param_nCols,index+1)
    	plt.xlabel('Query Number')
    	plt.plot(results[param].values,label=param)
        plt.plot(expected_best_params[index],label='model',color='r')
    	plt.ylim(results[param].values.min()-0.1,results[param].values.max()*1.1)
        plt.axhline(y=MonashValues[index],linestyle='--',color='g',label='Monash')
        plt.legend(loc='best', fancybox=True, shadow=True,title=param)
    plt.savefig(param_evolv_outputFile)


    #################################################################
    ##########    Getting Best Parameters found     #################
    #################################################################

    n_top = 10
    sorted_results = pd.DataFrame(sorted(results.values,key=getKey,reverse=False)[:n_top])
    sorted_results.columns=header
 
    BestFile  = open('{}/best.csv'.format(TextsDir),'wb')
    BestWriter = csv.writer(BestFile, delimiter =',',quotechar=" ",lineterminator="\n",quoting=csv.QUOTE_ALL)
    BestWriter.writerows(sorted_results.values)
    BestFile.close()
    
    BestRow = sorted_results[param_names].iloc[0].values


    #################################################################
    ##########      Generating Parameter Ratio plot     #############
    #################################################################

    ParamRanges = []
    for i in range(len(param_names)):
        ParamRanges.append(param_ranges[i][1]-param_ranges[i][0])
    ParamRanges = np.array(ParamRanges).astype(float)

    BestParsComb = np.array(BestRow).astype(float)

    Ratios = np.divide(BestParsComb, MonashValues)
    Diffs       = np.array(BestParsComb - MonashValues)
    Diffs_Model = np.array(Best_Model_Param - MonashValues)
    RelDiffs       = np.divide(Diffs,ParamRanges)*100
    RelDiffs_Model = np.divide(Diffs_Model,ParamRanges)*100

    n_params = len(param_names)
    pseudo_y_values = list(range(n_params))
 
    Best_params_all_outputFile = '{}/Best_params_all.pdf'.format(PlotsDir)
   
    fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,sharey='row',figsize=[10,10])

    ax1.set_xlabel('Best Found / Monash')
    ax1.scatter(Ratios, pseudo_y_values)
    ax1.set_yticks(list(range(n_params)))
    ax1.set_yticklabels(param_names,fontsize=8)
    ax1.tick_params(axis='x',labelsize=8)
    ax1.set_ylim(-1,len(param_names))
    ax1.set_xlim(0.25,2)
    ax1.axvline(x=1.0, linestyle='--',color='k')
    ax1.grid()

    ax3.set_xlabel('Best Found / Monash')
    ax3.set_yticks(list(range(n_params)))
    ax3.set_yticklabels(param_names,fontsize=8)
    ax3.set_ylim(-1,len(param_names))
    ax3.scatter(Ratios, pseudo_y_values)
    ax3.set_xscale('log')
    ax3.set_xlim(0.001,10000)
    ax3.grid()


    ax2.scatter(Diffs,pseudo_y_values)
    ax2.set_xlabel('Best Found - Monash')
    ax2.set_xlim(-1.0,1.0)
    ax2.axvline(x=0.0, linestyle='--',color='k')
    ax2.set_xscale('linear')
    ax2.grid()

    ax4.scatter(RelDiffs,pseudo_y_values,label='Observed',color='r')
    ax4.scatter(RelDiffs_Model,pseudo_y_values,label='Model',color='b')
    ax4.set_xlabel('(Best Found - Monash) / Range (%)')
    ax4.set_xlim(-50,50)
    ax4.axvline(x=0.0, linestyle='--',color='k')
    ax4.set_xscale('linear')
    ax4.legend(loc='best')
    ax4.grid()

    fig.tight_layout()
    fig.savefig(Best_params_all_outputFile)

    Best_params_RelDiff_outputFile = '{}/Best_params_RelDiff.pdf'.format(PlotsDir)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.scatter(RelDiffs,pseudo_y_values,label='Observed',color='b',s=20)
    ax.scatter(RelDiffs_Model,pseudo_y_values,label='Model',color='r',s=10)
    ax.set_xlabel('(Best Found - Monash) / Range (%)')
    ax.set_xlim(-50,50)
    ax.set_yticks(list(range(n_params)))
    ax.set_yticklabels(param_names,fontsize=8)
    ax.set_ylim(-1,n_params)
    ax.axvline(x=0.0, linestyle='--',color='k')
    ax.set_xscale('linear')
    ax.legend(loc='best')
    ax.grid()
    fig.tight_layout()
    fig.savefig(Best_params_RelDiff_outputFile)

def find_order():
    
    inFile = open(Spearmint_output_FILE)
    lines = list(inFile)
    inFile.seek(0)

    param_order = []
    found = False
    index = 0
    
    while not found:
        line = lines[index]
        lo_index = line.find("Minimum expected objective value under model is")
        str_len  = len("Minimum expected objective value under model is")
        up_index = line.find("(+/-")
        
        if lo_index != -1 and up_index !=-1:
                current_param_index = index+3
                value_start_index=lines[current_param_index-1].find("----")
                value_end_index = value_start_index+13
                for ind,line in enumerate(lines[current_param_index:current_param_index+len(param_names)]): 
                    string = str(line[value_start_index:value_end_index])
                    string = string.replace(" ","")
                    for param in param_names:
                        if string in param:
                            param_order.append(param)
                found = True
                    
        index += 1
        
    return param_order

def nRows_nCols(blocks):
    if blocks == [True,False,False]:
        return 3,1,5,2

    elif blocks == [False,True,False]:
        return 3,2,3,2
    
    elif blocks == [False,False,True]:
        return 4,3,2,2
    else:
        return 5,4,5,4

if __name__=='__main__':
    main()
