import os
import subprocess
import json
from general_utils import load_config

def write_spearmint_config():
    WorkHOME = os.environ['WorkHOME']
    with open('{}/pythia_space/pars_to_tune.txt'.format(WorkHOME),'r') as parsList:
        pars = parsList.read().splitlines()
        
    tune_config = load_config('tune_config.json')
    pars_info   = load_config('{}/utils/all_pars_dict.json'.format(WorkHOME))       
 
    config = {}
    config['language']  ='PYTHON'
    config['main-file'] ='Spearmint-Pythia-Tune.py'
    config['experiment-name'] = tune_config['spearmint_expt_name']
    config['likelihood'] = 'NOISELESS'
    var_info = {}
    for par in pars:
        par_info = {'type':'FLOAT','size':1,'min':pars_info[par]['min'],'max':pars_info[par]['max']}
        var_info[par]=par_info
    config['variables'] = var_info
    with open('{}/spearmint_space/config.json'.format(WorkHOME),'w') as spearmint_config:
        json.dump(config,spearmint_config,sort_keys=True, indent=4)

def start_spearmint_tune(spearmint_dir,WorkHOME,New_Tune):

    record_files = ['{}/interface/results.csv'.format(WorkHOME),
                    '{}/interface/time_stamps.csv'.format(WorkHOME),
                    '{}/interface/objectives.csv'.format(WorkHOME)]

    write_spearmint_config()

  
    if not New_Tune:
        cont_command = 'python {}/main.py {}/spearmint_space 2>&1 |tee -a {}/interface/spearmint_output.txt'.format(
            spearmint_dir,WorkHOME,WorkHOME)
        subprocess.call([cont_command],shell=True)
    if New_Tune:
        subprocess.call(['{}/cleanup.sh {}/spearmint_space'.format(spearmint_dir,WorkHOME)],shell=True)

	output_dir = '{}/spearmint_space/output'.format(WorkHOME)
        if not os.path.exists(output_dir):
	    os.makedirs(output_dir)
	with open('{}/.gitkeep'.format(output_dir),'w') as gitkeep_file:
	    gitkeep_file.write("spearmint output dir")

        for ifile in record_files:
            if os.path.exists(ifile):
                os.remove(ifile)
        new_command = 'python {}/main.py {}/spearmint_space 2>&1 | tee {}/interface/spearmint_output.txt'.format(
            spearmint_dir,WorkHOME,WorkHOME)
        subprocess.call([new_command],shell=True)
