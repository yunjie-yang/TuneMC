import os
import subprocess

def start_spearmint_tune(spearmint_dir,WorkHOME,New_Tune):

    record_files = ['{}/interface/results.csv'.format(WorkHOME),
                    '{}/interface/time_stamps.csv'.format(WorkHOME),
                    '{}/interface/objectives.csv'.format(WorkHOME)]


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
