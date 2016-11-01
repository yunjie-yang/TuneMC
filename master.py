import os
import json
from utils.general_utils import load_config,str_to_bool,params_to_tune,generate_pars_dict
from utils.spearmint_utils import start_spearmint_tune

def main():
    config = load_config('tune_config.json') 
    WorkHOME = config['WorkHOME']
    
    os.environ['WorkHOME'] = WorkHOME

    generate_pars_dict()    

    print 'WorkHOME = {}'.format(WorkHOME)

    blocks = []
    for i in range(1,4):
	blocks.append(str_to_bool(config['block{}'.format(i)]))

    params_to_tune(blocks)

    new_expt = str_to_bool(config['new_expt'])

    spearmint_dir = config['spearmint_dir']
    start_spearmint_tune(spearmint_dir,WorkHOME,new_expt)

if __name__ == '__main__':
    main()
